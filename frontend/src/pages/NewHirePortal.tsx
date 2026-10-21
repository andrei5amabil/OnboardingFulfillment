import React, { useEffect, useState, useMemo } from 'react';
import { fetchWithAuth } from '../lib/api';
import {
  Laptop,
  Loader2,
  ExternalLink,
  BookOpen,
  Building2,
  Calendar,
  MapPin,
  CheckCircle2,
  Sparkles,
  Boxes,
  Circle,
  Cpu,
} from 'lucide-react';

interface SoftwareProduct {
  product_id: string;
  name: string;
  vendor?: string;
  license_type: string;
  description?: string;
  access_url?: string;
  docs_url?: string;
}

interface LicenseAssignment {
  assignment_id: string;
  status: string;
  assigned_at: string;
  software_products: SoftwareProduct;
}

interface PortalData {
  status: string;
  employee_id: string;
  name: string;
  role: string;
  department: string;
  start_date: string;
  work_location: string;
  work_email?: string;
  shipping_address?: string;
  medical_clearance?: boolean;
  hardware?: {
    laptop?: string;
    peripherals?: string[];
    shipping_required?: boolean;
  };
  licenses?: LicenseAssignment[];
}

interface ChecklistItem {
  id: string;
  title: string;
}

export const NewHirePortal: React.FC = () => {
  const [data, setData] = useState<PortalData | null>(null);
  const [loading, setLoading] = useState(true);
  const [completedTasks, setCompletedTasks] = useState<Record<string, boolean>>({});

  useEffect(() => {
    fetchWithAuth('/portal/me')
      .then((res) => res.json())
      .then((resData: PortalData) => {
        setData(resData);
        if (resData.employee_id) {
          const stored = localStorage.getItem(`onboarding_tasks_${resData.employee_id}`);
          if (stored) {
            try {
              setCompletedTasks(JSON.parse(stored));
            } catch {
              setCompletedTasks({});
            }
          }
        }
      })
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  const isTechDept = useMemo(() => {
    return ['Engineering', 'Data', 'IT', 'Software Development', 'Quality Assurance'].some((d) =>
      (data?.department || '').includes(d)
    );
  }, [data?.department]);

  const checklistItems: ChecklistItem[] = useMemo(() => {
    return [
      {
        id: 'workspace_setup',
        title: isTechDept ? 'Set up local developer environment' : 'Join Slack & sync departmental calendars',
      },
      {
        id: 'tooling_verification',
        title: 'Verify SSO login on all provisioned applications',
      },
      {
        id: 'hardware_acknowledgment',
        title: data?.work_location === 'remote'
          ? 'Confirm delivery address for hardware kit'
          : 'Collect assigned workstation from IT storage',
      },
    ];
  }, [isTechDept, data?.work_location]);

  const toggleTask = (taskId: string) => {
    if (!data?.employee_id) return;
    setCompletedTasks((prev) => {
      const updated = { ...prev, [taskId]: !prev[taskId] };
      localStorage.setItem(`onboarding_tasks_${data.employee_id}`, JSON.stringify(updated));
      return updated;
    });
  };

  const completedCount = useMemo(() => {
    return checklistItems.filter((item) => completedTasks[item.id]).length;
  }, [checklistItems, completedTasks]);

  const progressPercent = Math.round((completedCount / checklistItems.length) * 100);

  if (loading) {
    return (
      <div className="flex h-96 items-center justify-center text-slate-700 font-bold text-sm">
        <Loader2 className="w-5 h-5 animate-spin mr-2 text-blue-600" />
        Loading environment...
      </div>
    );
  }

  if (data?.status === 'pending_linking') {
    return (
      <div className="max-w-2xl mx-auto px-4 py-16 text-center">
        <div className="p-6 bg-white border border-slate-300 rounded-xl shadow-sm text-slate-800 space-y-1">
          <h2 className="text-base font-bold text-slate-900">Profile Activation Pending</h2>
          <p className="text-xs text-slate-700">Record verification in progress.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 space-y-8">
      {/* Header */}
      <div className="border-b border-slate-300 pb-4 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-black tracking-tight text-slate-900">
            Welcome, {data?.name || 'Colleague'}
          </h1>
          <p className="text-xs text-slate-700 mt-0.5">
            Workstation and tool authorizations are configured.
          </p>
        </div>
        <span className="px-3 py-1 rounded-full bg-emerald-50 border border-emerald-300 text-emerald-800 text-xs font-bold">
          Active
        </span>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">
        {/* Role & Specs */}
        <div className="lg:col-span-7 bg-white border border-slate-300 rounded-xl p-5 shadow-sm space-y-5">
          <div className="flex items-center justify-between pb-2 border-b border-slate-200">
            <h2 className="text-xs font-bold text-slate-900 uppercase tracking-wider flex items-center gap-1.5">
              <Cpu className="w-4 h-4 text-blue-700" />
              <span>Assignment</span>
            </h2>
            <div className="flex items-center gap-2">
              <span className="font-mono text-xs font-bold bg-slate-100 px-2 py-0.5 rounded border border-slate-300 text-slate-800">
                {data?.employee_id}
              </span>
              <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-50 border border-blue-200 text-blue-700 uppercase tracking-wider">
                {data?.hardware?.shipping_required ? 'Dispatch' : 'Pickup'}
              </span>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-5 text-xs">
            <div className="space-y-3">
              <div>
                <span className="text-slate-600 font-bold block text-[11px] mb-0.5 uppercase">Department</span>
                <span className="font-bold text-slate-900 text-sm">{data?.department}</span>
              </div>
              <div>
                <span className="text-slate-600 font-bold block text-[11px] mb-0.5 uppercase">Role</span>
                <span className="font-bold text-blue-700 text-sm">{data?.role}</span>
              </div>
              <div className="flex gap-4">
                <div>
                  <span className="text-slate-600 font-bold block text-[11px] mb-0.5 uppercase">Start Date</span>
                  <span className="font-mono font-bold text-slate-900">{data?.start_date}</span>
                </div>
                <div>
                  <span className="text-slate-600 font-bold block text-[11px] mb-0.5 uppercase">Arrangement</span>
                  <span className="capitalize font-bold text-slate-900">{data?.work_location}</span>
                </div>
              </div>
            </div>

            <div className="space-y-3 sm:border-l sm:border-slate-200 sm:pl-5">
              <div>
                <span className="text-slate-600 font-bold block text-[11px] mb-0.5 uppercase">Hardware</span>
                <span className="font-bold text-slate-900 text-sm">
                  {data?.hardware?.laptop || 'Standard Corporate Laptop'}
                </span>
              </div>
              <div>
                <span className="text-slate-600 font-bold block text-[11px] mb-1 uppercase">Peripherals</span>
                <div className="flex flex-wrap gap-1">
                  {data?.hardware?.peripherals?.map((item, idx) => (
                    <span
                      key={idx}
                      className="px-2 py-0.5 rounded bg-slate-100 text-slate-900 text-xs font-semibold border border-slate-300"
                    >
                      {item}
                    </span>
                  )) || <span className="text-slate-700 text-xs">Standard kit</span>}
                </div>
              </div>
              <div className="text-xs text-slate-700">
                {data?.hardware?.shipping_required
                  ? 'Dispatched to registered delivery address.'
                  : 'Collect on-site from IT.'}
              </div>
            </div>
          </div>
        </div>

        {/* Day-1 Checklist */}
        <div className="lg:col-span-5 bg-white border border-slate-300 rounded-xl p-5 shadow-sm space-y-3">
          <div className="flex items-center justify-between">
            <h2 className="text-xs font-bold text-slate-900 uppercase tracking-wider">
              Checklist
            </h2>
            <span className="text-xs font-mono font-bold text-blue-700">
              {completedCount}/{checklistItems.length} ({progressPercent}%)
            </span>
          </div>

          <div className="w-full bg-slate-100 h-1.5 rounded-full overflow-hidden border border-slate-300">
            <div
              className="bg-blue-600 h-full transition-all duration-300"
              style={{ width: `${progressPercent}%` }}
            />
          </div>

          <div className="space-y-2 pt-1">
            {checklistItems.map((item) => {
              const isChecked = !!completedTasks[item.id];
              return (
                <button
                  key={item.id}
                  type="button"
                  onClick={() => toggleTask(item.id)}
                  className={`w-full text-left p-2.5 rounded-lg border flex items-center gap-2.5 transition-colors ${
                    isChecked
                      ? 'bg-emerald-50 border-emerald-300 text-slate-900'
                      : 'bg-white border-slate-300 hover:border-blue-600 text-slate-900'
                  }`}
                >
                  <div className="shrink-0">
                    {isChecked ? (
                      <CheckCircle2 className="w-4 h-4 text-emerald-700" />
                    ) : (
                      <Circle className="w-4 h-4 text-slate-400" />
                    )}
                  </div>
                  <span
                    className={`text-xs font-semibold ${
                      isChecked ? 'line-through text-slate-600' : 'text-slate-900'
                    }`}
                  >
                    {item.title}
                  </span>
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Software List */}
      <div className="space-y-3">
        <div className="border-b border-slate-300 pb-2">
          <h2 className="text-sm font-bold text-slate-900 flex items-center gap-1.5">
            <Boxes className="w-4 h-4 text-blue-700" />
            <span>Authorized Software ({data?.licenses?.length || 0})</span>
          </h2>
        </div>

        {data?.licenses && data.licenses.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {data.licenses.map((lic) => {
              const prod = lic.software_products;
              const hasValidAccessUrl = prod.access_url && prod.access_url !== '#';

              return (
                <div
                  key={lic.assignment_id}
                  className="bg-white border border-slate-300 rounded-xl p-4 flex flex-col justify-between gap-3 shadow-sm"
                >
                  <div>
                    <div className="flex items-start justify-between gap-2">
                      <div className="min-w-0">
                        <h3 className="text-xs font-bold text-slate-900 truncate">{prod.name}</h3>
                        <p className="text-[11px] font-semibold text-slate-600">{prod.vendor || 'Internal'}</p>
                      </div>
                      <span className="shrink-0 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-blue-50 border border-blue-200 text-blue-700">
                        {prod.license_type}
                      </span>
                    </div>

                    {prod.description && (
                      <p className="text-xs text-slate-700 mt-2 line-clamp-2">
                        {prod.description}
                      </p>
                    )}
                  </div>

                  <div className="pt-2 border-t border-slate-200 flex items-center gap-2">
                    {hasValidAccessUrl ? (
                      <a
                        href={prod.access_url}
                        target="_blank"
                        rel="noreferrer"
                        className="flex-1 inline-flex items-center justify-center gap-1 py-1.5 px-3 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold transition-colors"
                      >
                        <span>Launch</span>
                        <ExternalLink className="w-3 h-3" />
                      </a>
                    ) : (
                      <span className="flex-1 text-center py-1.5 px-3 rounded-lg bg-slate-100 text-slate-700 text-xs font-bold border border-slate-300">
                        Managed
                      </span>
                    )}

                    {prod.docs_url && (
                      <a
                        href={prod.docs_url}
                        target="_blank"
                        rel="noreferrer"
                        className="inline-flex items-center gap-1 py-1.5 px-2.5 rounded-lg bg-white hover:bg-slate-100 text-slate-800 text-xs font-bold border border-slate-300 transition-colors"
                      >
                        <BookOpen className="w-3 h-3" />
                        <span>Docs</span>
                      </a>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        ) : (
          <div className="p-6 text-center bg-white border border-slate-300 rounded-xl text-xs font-bold text-slate-700">
            No active software licenses assigned.
          </div>
        )}
      </div>
    </div>
  );
};