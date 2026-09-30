-- Migration unit 1: schema_changes
-- Transaction mode: transactional
-- Boundary reason: default

SET check_function_bodies = false;

CREATE TYPE public.user_role AS ENUM (
  'admin',
  'hr_manager',
  'it_manager',
  'new_hire'
);

CREATE FUNCTION public.handle_new_auth_user()
  RETURNS TRIGGER
  LANGUAGE plpgsql
  SECURITY DEFINER
  AS $function$
BEGIN
  INSERT INTO public.users (user_id, email, role)
  VALUES (
    NEW.id,
    NEW.email,
    COALESCE((NEW.raw_user_meta_data->>'role')::public.user_role, 'new_hire'::public.user_role)
  );
  RETURN NEW;
END;
$function$;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW
  EXECUTE FUNCTION public.handle_new_auth_user();

CREATE FUNCTION public.handle_updated_at()
  RETURNS TRIGGER
  LANGUAGE plpgsql
  AS $function$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$function$;

ALTER TABLE public.onboarding_requests
  ADD CONSTRAINT onboarding_requests_hr_manager_id_fkey FOREIGN KEY (hr_manager_id) REFERENCES public.employees(employee_id) ON UPDATE CASCADE ON DELETE SET NULL;

CREATE TABLE public.users (
  user_id     uuid                     NOT NULL,
  email       character varying        NOT NULL,
  role        public.user_role         DEFAULT 'new_hire'::public.user_role NOT NULL,
  employee_id character varying,
  is_active   boolean                  DEFAULT true NOT NULL,
  created_at  timestamp with time zone DEFAULT now() NOT NULL,
  updated_at  timestamp with time zone DEFAULT now() NOT NULL
);

ALTER TABLE public.users
  ENABLE ROW LEVEL SECURITY;

ALTER TABLE public.users
  ADD CONSTRAINT users_auth_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;

ALTER TABLE public.users
  ADD CONSTRAINT users_email_key UNIQUE (email);

ALTER TABLE public.users
  ADD CONSTRAINT users_employee_id_fkey FOREIGN KEY (employee_id) REFERENCES public.employees(employee_id) ON DELETE SET NULL;

ALTER TABLE public.users
  ADD CONSTRAINT users_employee_id_key UNIQUE (employee_id);

ALTER TABLE public.users
  ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);

GRANT MAINTAIN, REFERENCES, TRIGGER, TRUNCATE ON public.users TO anon;

GRANT MAINTAIN, REFERENCES, SELECT, TRIGGER, TRUNCATE, UPDATE ON public.users TO authenticated;

GRANT ALL ON public.users TO service_role;

CREATE INDEX idx_users_employee_id ON public.users (employee_id);

CREATE INDEX idx_users_role ON public.users (ROLE);

CREATE TRIGGER set_users_updated_at
  BEFORE UPDATE ON public.users
  FOR EACH ROW
  EXECUTE FUNCTION public.handle_updated_at();

CREATE POLICY "Allow authenticated users to read their own profile" ON public.users
  FOR SELECT
  TO authenticated
  USING ((auth.uid() = user_id));

CREATE POLICY "Allow users to update own profile" ON public.users
  FOR UPDATE
  TO authenticated
  USING ((auth.uid() = user_id));