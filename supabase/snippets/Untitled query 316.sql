ALTER TABLE public.workflow_runs 
ADD COLUMN IF NOT EXISTS discretionary_licenses jsonb NOT NULL DEFAULT '[]'::jsonb;