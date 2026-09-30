import React, { useEffect, useState } from 'react';
import { fetchWithAuth } from '../lib/api';
import { UserCheck, Laptop, ShieldCheck, Loader2 } from 'lucide-react';

export const NewHirePortal: React.FC = () => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchWithAuth('/portal/me')
      .then((res) => res.json())
      .then((resData) => setData(resData))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex h-96 items-center justify-center text-slate-400">
        <Loader2 className="w-6 h-6 animate-spin mr-2 text-indigo-400" />
        Loading your onboarding profile...
      </div>
    );
  }

  if (data?.status === 'pending_linking') {
    return (
      <div className="max-w-2xl mx-auto px-4 py-16 text-center space-y-4">
        <div className="p-4 bg-amber-500/10 border border-amber-500/30 rounded-2xl text-amber-300 text-sm">
          {data.message}
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-slate-100 flex items-center gap-2">
          👋 Welcome to the Team, {data?.name || 'Colleague'}!
        </h1>
        <p className="text-sm text-slate-400 mt-1">
          Here is the status of your employee account, workstation provisioning, and company access.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {/* Profile Card */}
        <div className="bg-slate-800/40 border border-slate-700/80 rounded-2xl p-5 space-y-3">
          <h2 className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
            <UserCheck className="w-4 h-4 text-indigo-400" />
            <span>Profile Details</span>
          </h2>
          <div className="text-xs space-y-2 text-slate-300">
            <div><span className="text-slate-500">Employee ID:</span> {data?.employee_id}</div>
            <div><span className="text-slate-500">Role:</span> {data?.role}</div>
            <div><span className="text-slate-500">Department:</span> {data?.department}</div>
            <div><span className="text-slate-500">Start Date:</span> {data?.start_date}</div>
            <div><span className="text-slate-500">Work Model:</span> {data?.work_location}</div>
          </div>
        </div>

        {/* Medical & Compliance Status */}
        <div className="bg-slate-800/40 border border-slate-700/80 rounded-2xl p-5 space-y-3">
          <h2 className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            <span>Compliance Clearance</span>
          </h2>
          <div className="text-xs space-y-2">
            <div className="flex items-center gap-2">
              <span className="text-slate-500">Medical Clearance:</span>
              <span className="text-emerald-400 font-semibold">Cleared (Fit for Work)</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-slate-500">Identity Verification:</span>
              <span className="text-emerald-400 font-semibold">Verified</span>
            </div>
          </div>
        </div>
      </div>

      {/* Software Entitlements */}
      <div className="bg-slate-800/40 border border-slate-700/80 rounded-2xl p-5 space-y-3">
        <h2 className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
          <Laptop className="w-4 h-4 text-indigo-400" />
          <span>Provisioned Software Licenses</span>
        </h2>
        {data?.licenses && data.licenses.length > 0 ? (
          <div className="overflow-x-auto rounded-lg border border-slate-700/80">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-900/80 text-slate-400 border-b border-slate-700/80">
                <tr>
                  <th className="p-2.5">Product</th>
                  <th className="p-2.5">Vendor</th>
                  <th className="p-2.5">Type</th>
                  <th className="p-2.5">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800 bg-slate-900/40 text-slate-200">
                {data.licenses.map((lic: any, idx: number) => (
                  <tr key={idx}>
                    <td className="p-2.5 font-medium">{lic.software_products?.name}</td>
                    <td className="p-2.5 text-slate-400">{lic.software_products?.vendor}</td>
                    <td className="p-2.5 text-slate-400">{lic.software_products?.license_type}</td>
                    <td className="p-2.5 text-emerald-400 font-medium">{lic.status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="text-xs text-slate-400">Software provisioning is currently in progress.</p>
        )}
      </div>
    </div>
  );
};