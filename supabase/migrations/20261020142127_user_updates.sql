-- Migration unit 1: schema_changes
-- Transaction mode: transactional
-- Boundary reason: default

ALTER TABLE public.employees
  DROP CONSTRAINT employees_onboarding_request_id_fkey;

ALTER TABLE public.users
  DROP CONSTRAINT users_employee_id_fkey;

ALTER TABLE public.software_products
  ADD COLUMN description text;

ALTER TABLE public.software_products
  ADD COLUMN access_url text;

ALTER TABLE public.software_products
  ADD COLUMN docs_url text;

ALTER TABLE public.users
  ADD CONSTRAINT users_employee_id_fkey FOREIGN KEY (employee_id) REFERENCES public.employees(employee_id) ON DELETE CASCADE;