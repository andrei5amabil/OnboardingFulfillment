-- Migration unit 1: schema_changes
-- Transaction mode: transactional
-- Boundary reason: default

ALTER TABLE public.onboarding_requests
  ADD COLUMN extraction_time_seconds numeric(6,2) DEFAULT 0.0;

ALTER TABLE public.onboarding_requests
  ADD COLUMN total_lead_time_seconds numeric(8,2) DEFAULT 0.0;

ALTER TABLE public.onboarding_requests
  ADD COLUMN finalized_at timestamp with time zone;

ALTER TABLE public.workflow_runs
  ADD COLUMN execution_time_seconds numeric(6,2) DEFAULT 0.0;

ALTER TABLE public.workflow_runs
  ADD COLUMN tokens_prompt integer DEFAULT 0;

ALTER TABLE public.workflow_runs
  ADD COLUMN tokens_completion integer DEFAULT 0;

ALTER TABLE public.workflow_runs
  ADD COLUMN tokens_total integer DEFAULT 0;

ALTER TABLE public.workflow_runs
  ADD COLUMN attempt_number integer DEFAULT 1;

ALTER TABLE public.workflow_runs
  ADD COLUMN review_action text;

ALTER TABLE public.workflow_runs
  ADD COLUMN reviewed_at timestamp with time zone;

CREATE INDEX idx_workflow_runs_analytics ON public.workflow_runs (created_at, review_action);