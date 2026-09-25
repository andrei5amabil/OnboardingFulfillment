export interface SoftwareProduct {
  name: string;
  vendor: string;
  license_type: string;
  requires_approval?: boolean;
  product_id?: string;
}

export interface SuggestedLicense {
  software_products?: SoftwareProduct;
  product_id?: string;
  access_level?: string;
  is_mandatory?: boolean;
  requires_approval?: boolean;
}

export interface DiscretionaryLicense {
  product_id: string;
  name: string;
  justification?: string;
}

export interface WorkflowRun {
  run_id?: string;
  request_id: string;
  created_at?: string;
  suggested_licenses: SuggestedLicense[];
  discretionary_licenses: DiscretionaryLicense[];
  suggested_hardware: Record<string, any>;
  policy_citations: Array<{
    tags?: string[];
    flagged_exceptions?: string[];
    [key: string]: any;
  }>;
}

export interface OnboardingRequest {
  request_id: string;
  created_at: string;
  employee_id: string;
  first_name: string;
  last_name: string;
  national_id?: string | null;
  department: string;
  role: string;
  start_date: string;
  employment_type: string;
  location: string;
  work_location: string;
  manager_id?: string | null;
  shipping_address?: string | null;
  contact_phone?: string | null;
  medical_clearance_status?: boolean | null;
  medical_clearance_date?: string | null;
  hr_manager_id: string;
  notes?: string | null;
  status:
    | 'processing_rules'
    | 'pending_approval'
    | 'pending_onboarding'
    | 'requires_manual_intervention'
    | 'completed'
    | 'failed'
    | string;
  workflow_runs?: WorkflowRun[];
}

export interface ReviewPayload {
  action: 'approve' | 'regenerate';
  note: string;
  reviewed_by: string;
  approved_discretionary_ids: string[];
}