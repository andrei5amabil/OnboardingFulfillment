import React, { useState } from 'react';
import { DocumentIngestion } from '../components/DocumentIngestion';
import { fetchWithAuth } from '../lib/api';
import {
  DEPARTMENTS,
  DEPARTMENT_ROLE_MAPPING,
  LOCATION_OPTIONS,
  WORK_LOCATION_OPTIONS,
  EMPLOYMENT_TYPE_OPTIONS,
} from '../constants/onboarding';
import {
  formatName,
  validateCrossDocuments,
  matchOption,
  type ValidationAlert,
} from '../utils/validation';
import type { DocumentType, ExtractionResponse, ContractData, NationalIDData, MedicalClearanceData } from '../types/extraction';
import {
  User,
  Briefcase,
  HeartPulse,
  Send,
  Loader2,
  AlertCircle,
  AlertTriangle,
  Info,
  CheckCircle,
} from 'lucide-react';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const generateRunId = (): string => {
  if (typeof crypto !== 'undefined' && crypto.randomUUID) {
    return `run-${crypto.randomUUID().substring(0, 12)}`;
  }
  return `run-${Math.random().toString(36).substring(2, 14)}`;
};

const getInitialFormData = () => ({
  first_name: '',
  last_name: '',
  national_id: '',
  department: DEPARTMENTS[0] as string,
  role: DEPARTMENT_ROLE_MAPPING[DEPARTMENTS[0]][0],
  start_date: new Date().toISOString().split('T')[0],
  employment_type: EMPLOYMENT_TYPE_OPTIONS[0],
  location: LOCATION_OPTIONS[0],
  work_location: WORK_LOCATION_OPTIONS[0],
  manager_id: '',
  shipping_address: '',
  contact_phone: '',
  medical_clearance_status: false,
  medical_clearance_date: new Date().toISOString().split('T')[0],
  notes: '',
  hr_manager_id: 'EMP-0042',
});

const INITIAL_SCANNED_DOCS = {
  contract: {},
  national_id: {},
  medical_clearance: {},
};

export const HrIntakePage: React.FC = () => {
  const [ingestionKey, setIngestionKey] = useState<number>(0);
  const [onboardingRunId, setOnboardingRunId] = useState<string>(generateRunId);
  const [, setScannedDocuments] = useState<{
    contract: Record<string, any>;
    national_id: Record<string, any>;
    medical_clearance: Record<string, any>;
  }>(INITIAL_SCANNED_DOCS);

  const [validationAlerts, setValidationAlerts] = useState<ValidationAlert[]>([]);
  const [formData, setFormData] = useState(getInitialFormData());
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitResponse, setSubmitResponse] = useState<{ status: 'success' | 'error'; message: string; data?: any } | null>(null);

  const handleExtractionSuccess = (docType: DocumentType, payload: ExtractionResponse) => {
    const extracted = payload.data as any;

    setScannedDocuments((prev) => {
      const updated = { ...prev, [docType]: extracted };
      const alerts = validateCrossDocuments(
        updated.contract,
        updated.national_id,
        updated.medical_clearance
      );
      setValidationAlerts(alerts);
      return updated;
    });

    setFormData((prev) => {
      const next = { ...prev };

      if (docType === 'contract') {
        const cData = extracted as ContractData;
        if (cData.department) {
          next.department = matchOption(cData.department, DEPARTMENTS, prev.department);
        }
        const availableRoles = DEPARTMENT_ROLE_MAPPING[next.department] || [];
        if (cData.role) {
          next.role = matchOption(cData.role, availableRoles, availableRoles[0] || '');
        }
        if (cData.start_date) next.start_date = cData.start_date;
        if (cData.manager_id) next.manager_id = cData.manager_id;
        if (cData.shipping_address) next.shipping_address = cData.shipping_address;
        if (cData.contact_phone) next.contact_phone = cData.contact_phone;
        if (cData.work_location) {
          next.work_location = matchOption(cData.work_location.replace('_', '-'), WORK_LOCATION_OPTIONS, prev.work_location);
        }
        if (cData.employment_type) {
          next.employment_type = matchOption(cData.employment_type.replace('_', '-'), EMPLOYMENT_TYPE_OPTIONS, prev.employment_type);
        }
      } else if (docType === 'national_id') {
        const idData = extracted as NationalIDData;
        if (idData.first_name) next.first_name = formatName(idData.first_name);
        if (idData.last_name) next.last_name = formatName(idData.last_name);
        if (idData.national_id) next.national_id = idData.national_id;
      } else if (docType === 'medical_clearance') {
        const medData = extracted as MedicalClearanceData;
        next.medical_clearance_status = Boolean(medData.medical_clearance_status);
        if (medData.issue_date) next.medical_clearance_date = medData.issue_date;
      }

      return next;
    });
  };

  const handleDepartmentChange = (newDept: string) => {
    const roles = DEPARTMENT_ROLE_MAPPING[newDept] || [];
    setFormData((prev) => ({
      ...prev,
      department: newDept,
      role: roles[0] || '',
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitResponse(null);

    if (!formData.first_name.trim() || !formData.last_name.trim() || !formData.role || !formData.start_date) {
      alert('Please fill in First Name, Last Name, Role, and Start Date.');
      return;
    }

    setIsSubmitting(true);

    const criticalNotes = validationAlerts
      .filter((a) => a.severity === 'critical')
      .map((a) => `[CRITICAL] ${a.message}`);

    let finalNotes = formData.notes.trim();
    if (criticalNotes.length > 0) {
      finalNotes += '\n\nDISCREPANCY FLAGS:\n' + criticalNotes.join('\n');
    }

    const payload = {
      onboarding_run_id: onboardingRunId,
      first_name: formatName(formData.first_name),
      last_name: formatName(formData.last_name),
      national_id: formData.national_id.trim() || null,
      department: formData.department,
      role: formData.role,
      manager_id: formData.manager_id.trim() || null,
      start_date: formData.start_date,
      employment_type: formData.employment_type,
      location: formData.location,
      work_location: formData.work_location,
      shipping_address: formData.shipping_address.trim() || null,
      contact_phone: formData.contact_phone.trim() || null,
      medical_clearance_status: formData.medical_clearance_status,
      medical_clearance_date: formData.medical_clearance_status ? formData.medical_clearance_date : null,
      hr_manager_id: formData.hr_manager_id,
      notes: finalNotes || null,
    };

    try {
      const res = await fetchWithAuth('/onboarding/requests', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Submission failed');

      setSubmitResponse({
        status: 'success',
        message: `Request ${data.data?.request_id || ''} created for ${payload.first_name} ${payload.last_name}.`,
        data: data.data,
      });

      setFormData(getInitialFormData());
      setScannedDocuments(INITIAL_SCANNED_DOCS);
      setValidationAlerts([]);
      setIngestionKey((prev) => prev + 1);
      setOnboardingRunId(generateRunId());

    } catch (err: any) {
      setSubmitResponse({
        status: 'error',
        message: err.message || 'Server connection error.',
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const availableRoles = DEPARTMENT_ROLE_MAPPING[formData.department] || [];
  const inputClass = "w-full bg-white border border-slate-300 rounded-lg px-3 py-2 text-xs text-slate-900 placeholder:text-slate-400 focus:outline-none focus:border-blue-600 focus:ring-1 focus:ring-blue-600 transition-colors";
  const labelClass = "block text-xs font-bold text-slate-900 mb-1";

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 space-y-8">
      <div>
        <h1 className="text-2xl font-black tracking-tight text-slate-900">
          Employee Intake
        </h1>
        <p className="text-xs text-slate-700 mt-1">
          Ingest documents to populate records and initiate provisioning.
        </p>
      </div>

      <DocumentIngestion
        key={ingestionKey}
        apiBaseUrl={API_BASE_URL}
        onboardingRunId={onboardingRunId}
        onExtractionSuccess={handleExtractionSuccess}
      />

      {validationAlerts.length > 0 && (
        <div className="space-y-2">
          {validationAlerts.map((alert, idx) => (
            <div
              key={idx}
              className={`p-3 rounded-lg flex items-start gap-2.5 text-xs font-semibold border ${
                alert.severity === 'critical'
                  ? 'bg-rose-50 border-rose-300 text-rose-950'
                  : alert.severity === 'warning'
                  ? 'bg-amber-50 border-amber-300 text-amber-950'
                  : 'bg-blue-50 border-blue-300 text-blue-950'
              }`}
            >
              {alert.severity === 'critical' ? (
                <AlertCircle className="w-4 h-4 shrink-0 text-rose-700 mt-0.5" />
              ) : alert.severity === 'warning' ? (
                <AlertTriangle className="w-4 h-4 shrink-0 text-amber-700 mt-0.5" />
              ) : (
                <Info className="w-4 h-4 shrink-0 text-blue-700 mt-0.5" />
              )}
              <div>
                <span className="uppercase font-bold tracking-wider mr-1.5">{alert.field}:</span>
                {alert.message}
              </div>
            </div>
          ))}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="border-b border-slate-300 pb-2">
          <h2 className="text-xs font-bold uppercase tracking-wider text-slate-900">
            Candidate Profile
          </h2>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Identity & Role */}
          <div className="bg-white border border-slate-300 rounded-xl p-5 shadow-sm space-y-4">
            <div className="flex items-center gap-2 pb-2 border-b border-slate-200 text-blue-700 font-bold text-xs uppercase tracking-wider">
              <User className="w-4 h-4" />
              <span>Identity & Organization</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label className={labelClass}>First Name *</label>
                <input
                  type="text"
                  required
                  value={formData.first_name}
                  onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
                  className={inputClass}
                />
              </div>
              <div>
                <label className={labelClass}>Last Name *</label>
                <input
                  type="text"
                  required
                  value={formData.last_name}
                  onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
                  className={inputClass}
                />
              </div>
            </div>

            <div>
              <label className={labelClass}>National ID / CNP</label>
              <input
                type="text"
                value={formData.national_id}
                onChange={(e) => setFormData({ ...formData, national_id: e.target.value })}
                className={inputClass}
              />
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label className={labelClass}>Department *</label>
                <select
                  value={formData.department}
                  onChange={(e) => handleDepartmentChange(e.target.value)}
                  className={inputClass}
                >
                  {DEPARTMENTS.map((dept) => (
                    <option key={dept} value={dept}>{dept}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className={labelClass}>Role *</label>
                <select
                  value={formData.role}
                  onChange={(e) => setFormData({ ...formData, role: e.target.value })}
                  className={inputClass}
                >
                  {availableRoles.map((role) => (
                    <option key={role} value={role}>{role}</option>
                  ))}
                </select>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label className={labelClass}>Start Date *</label>
                <input
                  type="date"
                  required
                  value={formData.start_date}
                  onChange={(e) => setFormData({ ...formData, start_date: e.target.value })}
                  className={inputClass}
                />
              </div>
              <div>
                <label className={labelClass}>Employment Type</label>
                <select
                  value={formData.employment_type}
                  onChange={(e) => setFormData({ ...formData, employment_type: e.target.value })}
                  className={inputClass}
                >
                  {EMPLOYMENT_TYPE_OPTIONS.map((type) => (
                    <option key={type} value={type}>{type}</option>
                  ))}
                </select>
              </div>
            </div>

            <div>
              <label className={labelClass}>Manager ID</label>
              <input
                type="text"
                placeholder="EMP-0010"
                value={formData.manager_id}
                onChange={(e) => setFormData({ ...formData, manager_id: e.target.value })}
                className={inputClass}
              />
            </div>
          </div>

          {/* Logistics & Compliance */}
          <div className="bg-white border border-slate-300 rounded-xl p-5 shadow-sm space-y-4">
            <div className="flex items-center gap-2 pb-2 border-b border-slate-200 text-blue-700 font-bold text-xs uppercase tracking-wider">
              <Briefcase className="w-4 h-4" />
              <span>Logistics & Compliance</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label className={labelClass}>Office Location</label>
                <select
                  value={formData.location}
                  onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                  className={inputClass}
                >
                  {LOCATION_OPTIONS.map((loc) => (
                    <option key={loc} value={loc}>{loc}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className={labelClass}>Work Arrangement</label>
                <select
                  value={formData.work_location}
                  onChange={(e) => setFormData({ ...formData, work_location: e.target.value })}
                  className={inputClass}
                >
                  {WORK_LOCATION_OPTIONS.map((wl) => (
                    <option key={wl} value={wl}>{wl}</option>
                  ))}
                </select>
              </div>
            </div>

            <div>
              <label className={labelClass}>Delivery Address</label>
              <textarea
                rows={2}
                value={formData.shipping_address}
                onChange={(e) => setFormData({ ...formData, shipping_address: e.target.value })}
                className={`${inputClass} resize-none`}
              />
            </div>

            <div>
              <label className={labelClass}>Contact Phone</label>
              <input
                type="text"
                value={formData.contact_phone}
                onChange={(e) => setFormData({ ...formData, contact_phone: e.target.value })}
                className={inputClass}
              />
            </div>

            <div className="pt-2 border-t border-slate-200 space-y-3">
              <div className="flex items-center gap-2 text-xs font-bold text-slate-900">
                <HeartPulse className="w-4 h-4 text-emerald-700" />
                <span>Medical Clearance</span>
              </div>

              <label className="flex items-center gap-2 cursor-pointer text-xs text-slate-900">
                <input
                  type="checkbox"
                  checked={formData.medical_clearance_status}
                  onChange={(e) => setFormData({ ...formData, medical_clearance_status: e.target.checked })}
                  className="rounded border-slate-300 text-blue-600 focus:ring-blue-600 w-4 h-4"
                />
                <span className="font-bold">Medical Clearance Verified</span>
              </label>

              {formData.medical_clearance_status && (
                <div>
                  <label className={labelClass}>Examination Date</label>
                  <input
                    type="date"
                    value={formData.medical_clearance_date}
                    onChange={(e) => setFormData({ ...formData, medical_clearance_date: e.target.value })}
                    className={inputClass}
                  />
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="bg-white border border-slate-300 rounded-xl p-5 shadow-sm">
          <label className={labelClass}>Additional Notes</label>
          <textarea
            rows={2}
            value={formData.notes}
            onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
            placeholder="Special provisions, access requirements, or software requests"
            className={`${inputClass} resize-none`}
          />
        </div>

        {submitResponse && (
          <div
            className={`p-4 rounded-xl border flex items-start gap-3 text-xs font-medium ${
              submitResponse.status === 'success'
                ? 'bg-emerald-50 border-emerald-300 text-emerald-950'
                : 'bg-rose-50 border-rose-300 text-rose-950'
            }`}
          >
            {submitResponse.status === 'success' ? (
              <CheckCircle className="w-5 h-5 text-emerald-700 shrink-0" />
            ) : (
              <AlertCircle className="w-5 h-5 text-rose-700 shrink-0" />
            )}
            <div className="space-y-1">
              <p className="font-bold text-sm">{submitResponse.message}</p>
              {submitResponse.data && (
                <pre className="p-3 bg-slate-900 text-slate-100 rounded-lg text-xs overflow-x-auto mt-2 font-mono">
                  {JSON.stringify(submitResponse.data, null, 2)}
                </pre>
              )}
            </div>
          </div>
        )}

        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full flex items-center justify-center gap-2 py-3 px-4 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold rounded-xl shadow-sm disabled:opacity-50 disabled:cursor-not-allowed transition-all"
        >
          {isSubmitting ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>Initiating Workflow...</span>
            </>
          ) : (
            <>
              <Send className="w-4 h-4" />
              <span>Submit Candidate</span>
            </>
          )}
        </button>
      </form>
    </div>
  );
};