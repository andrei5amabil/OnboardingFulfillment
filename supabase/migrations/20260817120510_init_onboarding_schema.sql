-- Migration unit 1: schema_changes
-- Transaction mode: transactional
-- Boundary reason: default

CREATE TABLE public.employees (
  employee_id           character varying        NOT NULL,
  created_at            timestamp with time zone DEFAULT now() NOT NULL,
  onboarding_request_id character varying,
  first_name            character varying        NOT NULL,
  last_name             character varying        NOT NULL,
  work_email            character varying,
  department            character varying        NOT NULL,
  role                  character varying        NOT NULL,
  start_date            date                     NOT NULL,
  employment_type       character varying        NOT NULL,
  location              character varying        NOT NULL,
  work_location         character varying        NOT NULL,
  manager_id            character varying,
  status                character varying        DEFAULT 'pending_onboarding'::character varying NOT NULL,
  updated_at            timestamp with time zone DEFAULT now() NOT NULL
);

ALTER TABLE public.employees
  ADD CONSTRAINT employees_pkey PRIMARY KEY (employee_id);

ALTER TABLE public.employees
  ADD CONSTRAINT employees_work_email_key UNIQUE (work_email);

GRANT MAINTAIN, REFERENCES, TRIGGER, TRUNCATE ON public.employees TO anon;

GRANT MAINTAIN, REFERENCES, TRIGGER, TRUNCATE ON public.employees TO authenticated;

GRANT MAINTAIN, REFERENCES, TRIGGER, TRUNCATE ON public.employees TO service_role;

CREATE TABLE public.onboarding_requests (
  request_id      character varying        NOT NULL,
  created_at      timestamp with time zone DEFAULT now() NOT NULL,
  employee_id     character varying        NOT NULL,
  first_name      character varying        NOT NULL,
  last_name       character varying        NOT NULL,
  department      character varying        NOT NULL,
  role            character varying        NOT NULL,
  start_date      date                     NOT NULL,
  employment_type character varying        NOT NULL,
  location        character varying        NOT NULL,
  work_location   character varying        NOT NULL,
  hr_manager_id   character varying        NOT NULL,
  notes           text,
  status          character varying        NOT NULL
);

ALTER TABLE public.onboarding_requests
  ADD CONSTRAINT onboarding_requests_employee_id_key UNIQUE (employee_id);

ALTER TABLE public.onboarding_requests
  ADD CONSTRAINT onboarding_requests_pkey PRIMARY KEY (request_id);

ALTER TABLE public.employees
  ADD CONSTRAINT employees_onboarding_request_id_fkey FOREIGN KEY (onboarding_request_id) REFERENCES public.onboarding_requests(request_id) ON DELETE SET NULL;

GRANT ALL ON public.onboarding_requests TO anon;

GRANT ALL ON public.onboarding_requests TO authenticated;

GRANT ALL ON public.onboarding_requests TO service_role;