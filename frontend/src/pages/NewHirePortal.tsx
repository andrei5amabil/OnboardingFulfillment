import React, { useEffect, useState, useMemo } from 'react';
import { fetchWithAuth } from '../lib/api';
import {
  Laptop,
  ShieldCheck,
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
  subtitle: string;
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
        title: isTechDept ? 'Development Environment' : 'Communication Channels',
        subtitle: isTechDept
          ? 'Clone project repos, generate local SSH keys, and verify CLI tools.'
          : 'Join primary Slack channels and sync departmental calendars.',
      },
      {
        id: 'tooling_verification',
        title: 'Software Seat Activation',
        subtitle: 'Log into each provisioned application below to test SSO access.',
      },
      {
        id: 'hardware_acknowledgment',
        title: 'Equipment & Workstation Setup',
        subtitle: data?.work_location === 'remote'
          ? 'Confirm delivery tracking address for hardware kit.'
          : 'Collect your assigned laptop and peripherals from local IT storage.',
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
      <div className="flex h-96 items-center justify-center text-slate-400">
        <Loader2 className="w-6 h-6 animate-spin mr-2 text-indigo-400" />
        Loading your Day-1 workstation environment...
      </div>
    );
  }

  if (data?.status === 'pending_linking') {
    return (
      <div className="max-w-2xl mx-auto px-4 py-16 text-center space-y-4">
        <div className="p-6 bg-slate-900 border border-slate-800 rounded-2xl text-slate-300 space-y-2">
          <h2 className="text-lg font-bold text-slate-100">Profile Activation Pending</h2>
          <p className="text-xs text-slate-400">
            Your enterprise employee record is currently being verified by IT Operations.
            Please check back shortly or reach out to your HR Lead.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 space-y-8">
      {/* 1. Header Banner */}
      <div className="bg-gradient-to-r from-indigo-950/40 via-slate-900 to-slate-900 border border-indigo-500/20 rounded-2xl p-6 sm:p-8">
        <div className="space-y-2">
          <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-[11px] font-semibold mb-1">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>Active & Provisioned</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-slate-100">
            Welcome to the Team, {data?.name || 'Colleague'}!
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 max-w-2xl">
            Your digital workstation, tool authorizations, and security credentials have been configured.
            Follow the guide below to complete Day-1 activation.
          </p>
        </div>
      </div>

      {/* 2. Unified 2-Column Split (Specs on Left, Checklist on Right) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">
        {/* Left: Consolidated Identity & Workstation Specs (7 cols) */}
        <div className="lg:col-span-7 bg-slate-900/60 border border-slate-800 rounded-2xl p-6 flex flex-col justify-between space-y-6">
          <div className="space-y-5">
            {/* Spec Sheet Header */}
            <div className="flex items-center justify-between pb-3 border-b border-slate-800">
              <h2 className="text-xs font-bold text-slate-200 uppercase tracking-wider flex items-center gap-2">
                <Cpu className="w-4 h-4 text-indigo-400" />
                <span>Workstation & Role Assignment</span>
              </h2>
              <div className="flex items-center gap-2">
                <span className="font-mono text-[11px] bg-slate-950 px-2 py-0.5 rounded border border-slate-800 text-slate-400">
                  {data?.employee_id}
                </span>
                <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 uppercase tracking-wider">
                  {data?.hardware?.shipping_required ? 'Remote Delivery' : 'On-Site Pickup'}
                </span>
              </div>
            </div>

            {/* 2-Column Internal Matrix */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              {/* Identity Section */}
              <div className="space-y-3.5 text-xs">
                <div>
                  <span className="text-slate-500 block text-[11px] mb-0.5 flex items-center gap-1.5">
                    <Building2 className="w-3.5 h-3.5 text-slate-400" /> Department
                  </span>
                  <span className="font-medium text-slate-200">{data?.department}</span>
                </div>

                <div>
                  <span className="text-slate-500 block text-[11px] mb-0.5 flex items-center gap-1.5">
                    <Sparkles className="w-3.5 h-3.5 text-indigo-400" /> Assigned Role
                  </span>
                  <span className="font-semibold text-indigo-300">{data?.role}</span>
                </div>

                <div className="flex items-center justify-between sm:justify-start sm:gap-8 pt-1">
                  <div>
                    <span className="text-slate-500 block text-[11px] mb-0.5 flex items-center gap-1.5">
                      <Calendar className="w-3.5 h-3.5 text-slate-400" /> Start Date
                    </span>
                    <span className="font-mono text-slate-300">{data?.start_date}</span>
                  </div>
                  <div>
                    <span className="text-slate-500 block text-[11px] mb-0.5 flex items-center gap-1.5">
                      <MapPin className="w-3.5 h-3.5 text-slate-400" /> Model
                    </span>
                    <span className="capitalize px-2 py-0.5 rounded text-[11px] font-medium bg-slate-800 text-slate-200 border border-slate-700/60 inline-block">
                      {data?.work_location}
                    </span>
                  </div>
                </div>
              </div>

              {/* Hardware Section */}
              <div className="space-y-3.5 text-xs sm:border-l sm:border-slate-800/80 sm:pl-6">
                <div>
                  <span className="text-slate-500 block text-[11px] mb-0.5 flex items-center gap-1.5">
                    <Laptop className="w-3.5 h-3.5 text-slate-400" /> Assigned Laptop
                  </span>
                  <span className="font-semibold text-slate-100">
                    {data?.hardware?.laptop || 'Standard Corporate Workstation'}
                  </span>
                </div>

                <div>
                  <span className="text-slate-500 block text-[11px] mb-1.5">Peripherals Bundle</span>
                  <div className="flex flex-wrap gap-1.5">
                    {data?.hardware?.peripherals && data.hardware.peripherals.length > 0 ? (
                      data.hardware.peripherals.map((item, idx) => (
                        <span
                          key={idx}
                          className="px-2 py-0.5 rounded bg-slate-800/90 text-slate-300 text-[11px] border border-slate-700/80"
                        >
                          {item}
                        </span>
                      ))
                    ) : (
                      <span className="text-slate-500 italic text-[11px]">Standard peripherals bundle</span>
                    )}
                  </div>
                </div>

                <div className="text-[11px] text-slate-400 pt-1">
                  {data?.hardware?.shipping_required
                    ? '📦 Dispatched to your registered delivery address.'
                    : '🏢 Available for pickup from the local IT service desk.'}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Right: Interactive Day-1 Checklist (5 cols) */}
        <div className="lg:col-span-5 bg-slate-900/60 border border-slate-800 rounded-2xl p-6 flex flex-col justify-between space-y-4">
          <div className="space-y-4">

            {/* Progress Meter */}
            <div className="space-y-1.5">
              <div className="w-full bg-slate-950 h-2 rounded-full overflow-hidden border border-slate-800">
                <div
                  className="bg-indigo-500 h-full transition-all duration-300"
                  style={{ width: `${progressPercent}%` }}
                />
              </div>
            </div>

            {/* Checklist Items */}
            <div className="space-y-2">
              {checklistItems.map((item) => {
                const isChecked = !!completedTasks[item.id];
                return (
                  <button
                    key={item.id}
                    type="button"
                    onClick={() => toggleTask(item.id)}
                    className={`w-full text-left p-2.5 rounded-xl border flex items-start gap-3 transition-colors ${
                      isChecked
                        ? 'bg-emerald-500/10 border-emerald-500/30 text-slate-200'
                        : 'bg-slate-950/50 border-slate-800 hover:border-slate-700 text-slate-300'
                    }`}
                  >
                    <div className="mt-0.5 shrink-0">
                      {isChecked ? (
                        <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                      ) : (
                        <Circle className="w-4 h-4 text-slate-500" />
                      )}
                    </div>
                    <div className="space-y-0.5 flex-1 min-w-0">
                      <p
                        className={`text-xs font-semibold leading-snug transition-all ${
                          isChecked ? 'line-through text-slate-400' : 'text-slate-200'
                        }`}
                      >
                        {item.title}
                      </p>
                      <p className="text-[11px] text-slate-400 leading-snug">
                        {item.subtitle}
                      </p>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      </div>

      {/* 3. Software Tooling Matrix */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-base font-bold text-slate-100 flex items-center gap-2">
              <Boxes className="w-5 h-5 text-indigo-400" />
              <span>Authorized Enterprise Software ({data?.licenses?.length || 0})</span>
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">
              Seat licenses provisioned for your role. Launch web consoles or inspect setup guides.
            </p>
          </div>
        </div>

        {data?.licenses && data.licenses.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {data.licenses.map((lic) => {
              const prod = lic.software_products;
              const hasValidAccessUrl = prod.access_url && prod.access_url !== '#';

              return (
                <div
                  key={lic.assignment_id}
                  className="bg-slate-900/60 border border-slate-800 hover:border-slate-700 rounded-xl p-5 flex flex-col justify-between gap-4 transition-all shadow-sm"
                >
                  <div className="space-y-2.5">
                    <div className="flex items-start justify-between gap-2">
                      <div className="min-w-0">
                        <h3 className="text-sm font-bold text-slate-100 truncate">{prod.name}</h3>
                        <p className="text-[11px] text-slate-400">{prod.vendor || 'Internal Tool'}</p>
                      </div>
                      <span className="shrink-0 px-2 py-0.5 rounded-full text-[10px] font-semibold uppercase tracking-wider bg-indigo-500/10 border border-indigo-500/30 text-indigo-300">
                        {prod.license_type}
                      </span>
                    </div>

                    <p className="text-xs text-slate-300 leading-relaxed min-h-[40px]">
                      {prod.description || 'Enterprise tool provisioned and maintained by IT Operations.'}
                    </p>
                  </div>

                  <div className="pt-3 border-t border-slate-800 flex items-center justify-between gap-2">
                    {hasValidAccessUrl ? (
                      <a
                        href={prod.access_url}
                        target="_blank"
                        rel="noreferrer"
                        className="flex-1 inline-flex items-center justify-center gap-1.5 py-1.5 px-3 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-sm transition-colors"
                      >
                        <span>Launch App</span>
                        <ExternalLink className="w-3 h-3" />
                      </a>
                    ) : (
                      <span className="flex-1 text-center py-1.5 px-3 rounded-lg bg-slate-800/80 text-slate-400 text-xs font-medium border border-slate-700/50">
                        Managed Seat
                      </span>
                    )}

                    {prod.docs_url && (
                      <a
                        href={prod.docs_url}
                        target="_blank"
                        rel="noreferrer"
                        title="View Documentation"
                        className="inline-flex items-center gap-1.5 py-1.5 px-3 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium border border-slate-700 transition-colors"
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
          <div className="p-8 text-center bg-slate-900/50 border border-slate-800 rounded-xl text-xs text-slate-400">
            No active software licenses are associated with this profile yet.
          </div>
        )}
      </div>
    </div>
  );
};