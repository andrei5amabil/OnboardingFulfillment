import React, { useState } from 'react';
import { DocumentIngestion } from '../components/DocumentIngestion';
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
  MapPin,
  Calendar,
  Building,
  HeartPulse,
  Send,
  Loader2,
  AlertCircle,
  AlertTriangle,
  Info,
  CheckCircle,
} from 'lucide-react';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const HrIntakePage: React.FC = () => {
  // Scanned docs cache for cross-validation
  const [scannedDocuments, setScannedDocuments] = useState<{
    contract: Record<string, any>;
    national_id: Record<string, any>;
    medical_clearance: Record<string, any>;
  }>({
    contract: {},
    national_id: {},
    medical_clearance: {},
  });

  const [validationAlerts, setValidationAlerts] = useState<ValidationAlert[]>([]);

  // Form State
  const [formData, setFormData] = useState({
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

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitResponse, setSubmitResponse] = useState<{ status: 'success' | 'error'; message: string; data?: any } | null>(null);

  // Handle Extraction Callback from DocumentIngestion
  const handleExtractionSuccess = (docType: DocumentType, payload: ExtractionResponse) => {
    const extracted = payload.data as any;

    setScannedDocuments((prev) => {
      const updated = { ...prev, [docType]: extracted };
      // Re-run Cross-Validation
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
      alert('Please fill in all mandatory fields: First Name, Last Name, Role, and Start Date.');
      return;
    }

    setIsSubmitting(true);

    const criticalNotes = validationAlerts
      .filter((a) => a.severity === 'critical')
      .map((a) => `[CRITICAL] ${a.message}`);

    let finalNotes = formData.notes.trim();
    if (criticalNotes.length > 0) {
      finalNotes += '\n\n### AUTOMATED DOCUMENT DISCREPANCY FLAGS:\n' + criticalNotes.join('\n');
    }

    const payload = {
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
      const res = await fetch(`${API_BASE_URL}/onboarding/requests`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Submission failed');

      setSubmitResponse({
        status: 'success',
        message: `Onboarding request ${data.data?.request_id || ''} created for ${payload.first_name} ${payload.last_name}! Workflow initialized.`,
        data: data.data,
      });
    } catch (err: any) {
      setSubmitResponse({
        status: 'error',
        message: err.message || 'Unable to connect to backend server.',
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const availableRoles = DEPARTMENT_ROLE_MAPPING[formData.department] || [];

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-slate-100">
          📝 Assisted Employee Onboarding Intake
        </h1>
        <p className="text-sm text-slate-400 mt-1">
          Upload candidate documents to pre-fill identity, contract, logistics, and compliance data.
        </p>
      </div>

      {/* 1. Document Ingestion Dropzones */}
      <DocumentIngestion
        apiBaseUrl={API_BASE_URL}
        onExtractionSuccess={handleExtractionSuccess}
      />

      {/* Cross-Document Validation Alerts */}
      {validationAlerts.length > 0 && (
        <div className="space-y-2">
          {validationAlerts.map((alert, idx) => (
            <div
              key={idx}
              className={`p-3 rounded-lg flex items-start gap-2.5 text-xs font-medium border ${
                alert.severity === 'critical'
                  ? 'bg-rose-500/10 border-rose-500/30 text-rose-300'
                  : alert.severity === 'warning'
                  ? 'bg-amber-500/10 border-amber-500/30 text-amber-300'
                  : 'bg-sky-500/10 border-sky-500/30 text-sky-300'
              }`}
            >
              {alert.severity === 'critical' ? (
                <AlertCircle className="w-4 h-4 shrink-0 text-rose-400 mt-0.5" />
              ) : alert.severity === 'warning' ? (
                <AlertTriangle className="w-4 h-4 shrink-0 text-amber-400 mt-0.5" />
              ) : (
                <Info className="w-4 h-4 shrink-0 text-sky-400 mt-0.5" />
              )}
              <div>
                <span className="uppercase font-bold tracking-wider mr-1.5">{alert.field}:</span>
                {alert.message}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* 2. Candidate Profile & Review Form */}
      <form onSubmit={handleSubmit} className="space-y-6">
        <h2 className="text-lg font-bold text-slate-100">2. Candidate Profile & Review</h2>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Column 1: Identity & Role */}
          <div className="bg-slate-800/40 border border-slate-700/80 rounded-xl p-5 space-y-4">
            <div className="flex items-center gap-2 pb-2 border-b border-slate-700/50 text-indigo-400 font-semibold text-sm">
              <User className="w-4 h-4" />
              <span>Identity & Role</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">First Name *</label>
                <input
                  type="text"
                  required
                  value={formData.first_name}
                  onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100 focus:outline-none focus:border-indigo-500"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">Last Name *</label>
                <input
                  type="text"
                  required
                  value={formData.last_name}
                  onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100 focus:outline-none focus:border-indigo-500"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">National ID / CNP</label>
              <input
                type="text"
                value={formData.national_id}
                onChange={(e) => setFormData({ ...formData, national_id: e.target.value })}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100 focus:outline-none focus:border-indigo-500"
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">Department *</label>
              <select
                value={formData.department}
                onChange={(e) => handleDepartmentChange(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100 focus:outline-none focus:border-indigo-500"
              >
                {DEPARTMENTS.map((dept) => (
                  <option key={dept} value={dept}>{dept}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">Role *</label>
              <select
                value={formData.role}
                onChange={(e) => setFormData({ ...formData, role: e.target.value })}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100 focus:outline-none focus:border-indigo-500"
              >
                {availableRoles.map((role) => (
                  <option key={role} value={role}>{role}</option>
                ))}
              </select>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">Start Date *</label>
                <input
                  type="date"
                  required
                  value={formData.start_date}
                  onChange={(e) => setFormData({ ...formData, start_date: e.target.value })}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100 focus:outline-none focus:border-indigo-500"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">Employment Type</label>
                <select
                  value={formData.employment_type}
                  onChange={(e) => setFormData({ ...formData, employment_type: e.target.value })}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100 focus:outline-none focus:border-indigo-500"
                >
                  {EMPLOYMENT_TYPE_OPTIONS.map((type) => (
                    <option key={type} value={type}>{type}</option>
                  ))}
                </select>
              </div>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">Manager ID (Optional)</label>
              <input
                type="text"
                placeholder="e.g. EMP-0010"
                value={formData.manager_id}
                onChange={(e) => setFormData({ ...formData, manager_id: e.target.value })}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100 focus:outline-none focus:border-indigo-500"
              />
            </div>
          </div>

          {/* Column 2: Logistics & Compliance */}
          <div className="bg-slate-800/40 border border-slate-700/80 rounded-xl p-5 space-y-4">
            <div className="flex items-center gap-2 pb-2 border-b border-slate-700/50 text-indigo-400 font-semibold text-sm">
              <Briefcase className="w-4 h-4" />
              <span>Logistics & Compliance</span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">Office Location</label>
                <select
                  value={formData.location}
                  onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100 focus:outline-none focus:border-indigo-500"
                >
                  {LOCATION_OPTIONS.map((loc) => (
                    <option key={loc} value={loc}>{loc}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">Work Arrangement</label>
                <select
                  value={formData.work_location}
                  onChange={(e) => setFormData({ ...formData, work_location: e.target.value })}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100 focus:outline-none focus:border-indigo-500"
                >
                  {WORK_LOCATION_OPTIONS.map((wl) => (
                    <option key={wl} value={wl}>{wl}</option>
                  ))}
                </select>
              </div>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">
                Delivery Address (Required for Remote/Hybrid)
              </label>
              <textarea
                rows={2}
                value={formData.shipping_address}
                onChange={(e) => setFormData({ ...formData, shipping_address: e.target.value })}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100 focus:outline-none focus:border-indigo-500 resize-none"
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">Contact Phone</label>
              <input
                type="text"
                value={formData.contact_phone}
                onChange={(e) => setFormData({ ...formData, contact_phone: e.target.value })}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100 focus:outline-none focus:border-indigo-500"
              />
            </div>

            <div className="pt-2 border-t border-slate-700/50 space-y-3">
              <div className="flex items-center gap-2 text-xs font-semibold text-slate-300">
                <HeartPulse className="w-4 h-4 text-emerald-400" />
                <span>Medical Clearance Gatekeeper</span>
              </div>

              <label className="flex items-center gap-2 cursor-pointer text-xs text-slate-300">
                <input
                  type="checkbox"
                  checked={formData.medical_clearance_status}
                  onChange={(e) => setFormData({ ...formData, medical_clearance_status: e.target.checked })}
                  className="rounded border-slate-700 bg-slate-900 text-indigo-600 focus:ring-0"
                />
                <span>Medical Clearance Confirmed (Fit for Work)</span>
              </label>

              {formData.medical_clearance_status && (
                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">Examination Date</label>
                  <input
                    type="date"
                    value={formData.medical_clearance_date}
                    onChange={(e) => setFormData({ ...formData, medical_clearance_date: e.target.value })}
                    className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100 focus:outline-none focus:border-indigo-500"
                  />
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Notes */}
        <div>
          <label className="block text-xs font-medium text-slate-300 mb-1">
            Additional Onboarding Notes (Special Software/Hardware Requests)
          </label>
          <textarea
            rows={3}
            value={formData.notes}
            onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
            className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-slate-100 focus:outline-none focus:border-indigo-500"
          />
        </div>

        {/* Feedback Alert */}
        {submitResponse && (
          <div
            className={`p-4 rounded-xl border flex items-start gap-3 text-xs ${
              submitResponse.status === 'success'
                ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300'
                : 'bg-rose-500/10 border-rose-500/30 text-rose-300'
            }`}
          >
            {submitResponse.status === 'success' ? (
              <CheckCircle className="w-5 h-5 text-emerald-400 shrink-0" />
            ) : (
              <AlertCircle className="w-5 h-5 text-rose-400 shrink-0" />
            )}
            <div className="space-y-1">
              <p className="font-semibold">{submitResponse.message}</p>
              {submitResponse.data && (
                <pre className="p-2 bg-slate-950/60 rounded text-[11px] overflow-x-auto text-slate-400">
                  {JSON.stringify(submitResponse.data, null, 2)}
                </pre>
              )}
            </div>
          </div>
        )}

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full flex items-center justify-center gap-2 py-3 px-4 bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-semibold rounded-xl shadow-lg shadow-indigo-500/20 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
        >
          {isSubmitting ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>Initiating Onboarding Workflow...</span>
            </>
          ) : (
            <>
              <Send className="w-4 h-4" />
              <span>Initiate Onboarding</span>
            </>
          )}
        </button>
      </form>
    </div>
  );
};