export interface KPIData {
  total_onboarded: number;
  avg_tokens_per_employee: number;
  token_usage_breakdown: {
    prompt: number;
    completion: number;
    total: number;
  };
  avg_agent_execution_seconds: number;
  avg_total_lead_time_seconds: number;
  first_pass_approval_rate: number;
  escalation_rate: number;
  recent_runs: Array<{
    run_id?: string;
    request_id: string;
    execution_time_seconds: number;
    tokens_total: number;
    attempt_number: number;
    review_action: string | null;
    created_at: string;
  }>;
}