ALTER TABLE workflow_runs
ADD COLUMN IF NOT EXISTS execution_time_seconds NUMERIC(6, 2) DEFAULT 0.0,
ADD COLUMN IF NOT EXISTS tokens_prompt INT DEFAULT 0,
ADD COLUMN IF NOT EXISTS tokens_completion INT DEFAULT 0,
ADD COLUMN IF NOT EXISTS tokens_total INT DEFAULT 0,
ADD COLUMN IF NOT EXISTS attempt_number INT DEFAULT 1,
ADD COLUMN IF NOT EXISTS review_action TEXT, -- 'approve' | 'regenerate' | NULL
ADD COLUMN IF NOT EXISTS reviewed_at TIMESTAMPTZ;

-- Add extraction and lead-time tracking to onboarding_requests
ALTER TABLE onboarding_requests
ADD COLUMN IF NOT EXISTS extraction_time_seconds NUMERIC(6, 2) DEFAULT 0.0,
ADD COLUMN IF NOT EXISTS total_lead_time_seconds NUMERIC(8, 2) DEFAULT 0.0,
ADD COLUMN IF NOT EXISTS finalized_at TIMESTAMPTZ;

-- Index for analytics aggregation queries
CREATE INDEX IF NOT EXISTS idx_workflow_runs_analytics 
ON workflow_runs(created_at, review_action);