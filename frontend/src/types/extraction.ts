export type DocumentType = 'contract' | 'national_id' | 'medical_clearance';

export interface ContractData {
  first_name?: string | null;
  last_name?: string | null;
  national_id?: string | null;
  role?: string | null;
  department?: string | null;
  start_date?: string | null;
  manager_id?: string | null;
  employment_type?: string | null;
  work_location?: string | null;
  location?: string | null;
  shipping_address?: string | null;
  contact_phone?: string | null;
}

export interface NationalIDData {
  first_name?: string | null;
  last_name?: string | null;
  national_id?: string | null;
}

export interface MedicalClearanceData {
  medical_clearance_status: boolean;
  issue_date?: string | null;
}

export type ExtractedData = ContractData | NationalIDData | MedicalClearanceData;

export interface ExtractionResponse {
  status: string;
  document_type: DocumentType;
  filename: string;
  confidence_flags: string[];
  data: ExtractedData;
}