-- Migration unit 1: schema_changes
-- Transaction mode: transactional
-- Boundary reason: default

ALTER TABLE public.employees
  ADD COLUMN national_id character varying;

ALTER TABLE public.employees
  ADD CONSTRAINT employees_national_id_key UNIQUE (national_id);

ALTER TABLE public.employees
  ADD COLUMN shipping_address text;

ALTER TABLE public.employees
  ADD COLUMN contact_phone character varying;

ALTER TABLE public.employees
  ADD COLUMN medical_clearance_status boolean DEFAULT false NOT NULL;

ALTER TABLE public.onboarding_requests
  ADD COLUMN manager_id character varying;

ALTER TABLE public.onboarding_requests
  ADD COLUMN shipping_address text;

ALTER TABLE public.onboarding_requests
  ADD COLUMN contact_phone character varying;

ALTER TABLE public.onboarding_requests
  ADD COLUMN medical_clearance_status boolean DEFAULT false NOT NULL;

ALTER TABLE public.onboarding_requests
  ADD COLUMN national_id character varying;

ALTER TABLE public.onboarding_requests
  ADD CONSTRAINT onboarding_requests_national_id_key UNIQUE (national_id);

ALTER TABLE public.onboarding_requests
  ADD COLUMN medical_clearance_date date;

ALTER TABLE public.workflow_runs
  ADD COLUMN discretionary_licenses jsonb DEFAULT '[]'::jsonb NOT NULL;

CREATE INDEX workflow_runs_request_id_idx ON public.workflow_runs (request_id);