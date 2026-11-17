-- Migration: Jira Cloud ticketing integration
-- One onboarding request maps to exactly one parent Jira ticket, while
-- workflow_runs keeps one row per generation/regeneration attempt.
--
-- IF NOT EXISTS keeps this migration idempotent for environments where the
-- columns were already created manually (see supabase/snippets).

ALTER TABLE public.onboarding_requests
  ADD COLUMN IF NOT EXISTS jira_ticket_id character varying,
  ADD COLUMN IF NOT EXISTS jira_ticket_url text,
  ADD COLUMN IF NOT EXISTS jira_subtask_id character varying;

-- A Jira issue may only be linked to a single onboarding request. The partial
-- index keeps existing NULL rows (requests created before Jira was enabled)
-- valid while preventing duplicate links.
CREATE UNIQUE INDEX IF NOT EXISTS onboarding_requests_jira_ticket_id_idx
  ON public.onboarding_requests (jira_ticket_id)
  WHERE jira_ticket_id IS NOT NULL;

NOTIFY pgrst, 'reload schema';
