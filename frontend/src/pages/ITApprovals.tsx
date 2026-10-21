import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { fetchWithAuth } from '../lib/api';
import {
  RotateCw,
  CheckCircle,
  AlertCircle,
  Laptop,
  ShieldAlert,
  Loader2,
  FileCheck2,
  XCircle,
  Server,
  Radio,
} from 'lucide-react';
import { supabase } from '../lib/supabase';
import type { OnboardingRequest, ReviewPayload } from '../types/provisioning';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const ITApprovalsPage: React.FC = () => {
  const [tasks, setTasks] = useState<OnboardingRequest[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isSyncing, setIsSyncing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [selectedDiscretionary, setSelectedDiscretionary] = useState<Record<string, string[]>>({});
  const [reviewNotes, setReviewNotes] = useState<Record<string, string>>({});
  const [actionLoading, setActionLoading] = useState<Record<string, boolean>>({});

  const fetchTasks = useCallback(async (silent = false) => {
    if (!silent) setIsLoading(true);
    else setIsSyncing(true);
    setError(null);

    try {
      const res = await fetchWithAuth(`${API_BASE_URL}/onboarding/requests`);
      if (!res.ok) throw new Error(`HTTP error: ${res.status}`);
      const data: OnboardingRequest[] = await res.json();

      const pending = data.filter((t) => t.status !== 'completed');
      setTasks(pending);

      setSelectedDiscretionary((prev) => {
        const next = { ...prev };
        pending.forEach((task) => {
          const plan = task.workflow_runs?.[0];
          if (plan?.discretionary_licenses && !next[task.request_id]) {
            next[task.request_id] = plan.discretionary_licenses.map((d) => d.product_id);
          }
        });
        return next;
      });
    } catch (err: any) {
      setError(err.message || 'Could not load tasks.');
    } finally {
      setIsLoading(false);
      setIsSyncing(false);
    }
  }, []);

  useEffect(() => {
    fetchTasks(false);
  }, [fetchTasks]);

  const hasProcessingTasks = useMemo(
    () => tasks.some((t) => t.status === 'processing_rules'),
    [tasks]
  );

  useEffect(() => {
    if (!hasProcessingTasks) return;
    const interval = setInterval(() => {
      fetchTasks(true);
    }, 2500);
    return () => clearInterval(interval);
  }, [hasProcessingTasks, fetchTasks]);

  useEffect(() => {
    const channel = supabase
      .channel('schema-db-changes')
      .on(
        'postgres_changes',
        { event: '*', schema: 'public', table: 'onboarding_requests' },
        () => fetchTasks(true)
      )
      .on(
        'postgres_changes',
        { event: 'INSERT', schema: 'public', table: 'workflow_runs' },
        () => fetchTasks(true)
      )
      .subscribe();

    return () => {
      supabase.removeChannel(channel);
    };
  }, [fetchTasks]);

  const handleToggleDiscretionary = (requestId: string, productId: string) => {
    setSelectedDiscretionary((prev) => {
      const current = prev[requestId] || [];
      const updated = current.includes(productId)
        ? current.filter((id) => id !== productId)
        : [...current, productId];
      return { ...prev, [requestId]: updated };
    });
  };

  const handleGeneratePlan = async (requestId: string) => {
    setActionLoading((prev) => ({ ...prev, [requestId]: true }));
    try {
      const res = await fetchWithAuth(`${API_BASE_URL}/onboarding/requests/${requestId}/generate-plan`, {
        method: 'POST',
      });
      if (!res.ok) throw new Error('Failed to start plan generation.');
      await fetchTasks(true);
    } catch (err: any) {
      alert(err.message);
    } finally {
      setActionLoading((prev) => ({ ...prev, [requestId]: false }));
    }
  };

  const handleReviewAction = async (requestId: string, action: 'approve' | 'regenerate') => {
    setActionLoading((prev) => ({ ...prev, [requestId]: true }));
    const payload: ReviewPayload = {
      action,
      note: (reviewNotes[requestId] || '').trim(),
      reviewed_by: 'EMP-IT-01',
      approved_discretionary_ids: selectedDiscretionary[requestId] || [],
    };

    try {
      const res = await fetchWithAuth(`${API_BASE_URL}/onboarding/requests/${requestId}/review`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || 'Review submission failed');
      }

      await fetchTasks(true);
    } catch (err: any) {
      alert(`Action error: ${err.message}`);
    } finally {
      setActionLoading((prev) => ({ ...prev, [requestId]: false }));
    }
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-300 pb-4">
        <div>
          <h1 className="text-2xl font-black tracking-tight text-slate-900">
            IT Approvals
          </h1>
          <p className="text-xs text-slate-700 mt-1">
            Review access entitlements and authorize provisioning pipelines.
          </p>
        </div>

        <div className="flex items-center gap-2 self-start sm:self-auto">
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-white border border-slate-300 text-xs font-mono font-semibold text-slate-800 shadow-sm">
            <Radio
              className={`w-3.5 h-3.5 ${
                hasProcessingTasks || isSyncing
                  ? 'text-amber-600 animate-pulse'
                  : 'text-emerald-600'
              }`}
            />
            <span>
              {hasProcessingTasks ? 'Processing' : isSyncing ? 'Syncing' : 'Connected'}
            </span>
          </div>

          <button
            type="button"
            onClick={() => fetchTasks(false)}
            disabled={isLoading}
            className="flex items-center gap-2 px-3 py-1.5 text-xs font-bold rounded-lg bg-white hover:bg-slate-100 text-slate-800 border border-slate-300 disabled:opacity-50 transition-colors shadow-sm"
          >
            <RotateCw className={`w-3.5 h-3.5 ${isLoading ? 'animate-spin' : ''}`} />
            <span>Refresh</span>
          </button>
        </div>
      </div>

      {error && (
        <div className="p-3 bg-rose-50 border border-rose-300 rounded-xl flex items-center gap-2.5 text-xs font-bold text-rose-950">
          <AlertCircle className="w-4 h-4 shrink-0 text-rose-700" />
          <span>{error}</span>
        </div>
      )}

      {tasks.length === 0 && !isLoading ? (
        <div className="p-12 text-center border border-slate-300 bg-white rounded-2xl shadow-sm">
          <CheckCircle className="w-8 h-8 text-emerald-600 mx-auto mb-2" />
          <h3 className="text-sm font-bold text-slate-900">Queue Clear</h3>
          <p className="text-xs text-slate-700 mt-0.5">No tasks awaiting approval.</p>
        </div>
      ) : (
        <div className="space-y-6">
          {tasks.map((task) => {
            const reqId = task.request_id;
            const plan = task.workflow_runs?.[0];
            const hasPlan = Boolean(plan);
            const isProcessing = actionLoading[reqId];

            return (
              <div
                key={reqId}
                className="bg-white border border-slate-300 rounded-xl p-5 shadow-sm space-y-5"
              >
                {/* Task Details Header */}
                <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-3 border-b border-slate-200 gap-2">
                  <div>
                    <h2 className="text-base font-bold text-slate-900">
                      {task.first_name} {task.last_name}
                    </h2>
                    <p className="text-xs text-slate-700 mt-0.5">
                      {task.department} • <span className="font-semibold text-blue-700">{task.role}</span>
                    </p>
                  </div>
                  <div className="flex items-center gap-2.5 text-xs font-mono">
                    <span className="text-slate-600 font-bold">{reqId}</span>
                    <span
                      className={`px-2.5 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider border ${
                        task.status === 'pending_approval'
                          ? 'bg-amber-50 border-amber-300 text-amber-900'
                          : task.status === 'processing_rules'
                          ? 'bg-blue-50 border-blue-300 text-blue-900'
                          : task.status === 'failed'
                          ? 'bg-rose-50 border-rose-300 text-rose-900'
                          : 'bg-slate-100 border-slate-300 text-slate-800'
                      }`}
                    >
                      {task.status.replace(/_/g, ' ')}
                    </span>
                  </div>
                </div>

                {task.status === 'processing_rules' && (
                  <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg flex items-center gap-2 text-xs font-semibold text-blue-950">
                    <Loader2 className="w-4 h-4 animate-spin text-blue-700 shrink-0" />
                    <span>Evaluating rules and generating plan...</span>
                  </div>
                )}

                {task.status === 'failed' && (
                  <div className="p-3 bg-rose-50 border border-rose-200 rounded-lg flex items-center justify-between">
                    <div className="flex items-center gap-2 text-xs font-bold text-rose-950">
                      <XCircle className="w-4 h-4 text-rose-700" />
                      <span>Generation failed.</span>
                    </div>
                    <button
                      onClick={() => handleGeneratePlan(reqId)}
                      disabled={isProcessing}
                      className="px-3 py-1 bg-rose-600 hover:bg-rose-700 text-white rounded text-xs font-bold"
                    >
                      Retry
                    </button>
                  </div>
                )}

                {task.status === 'pending_onboarding' && !hasPlan && (
                  <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg flex items-center justify-between">
                    <span className="text-xs font-semibold text-slate-800">
                      Plan generation pending.
                    </span>
                    <button
                      onClick={() => handleGeneratePlan(reqId)}
                      disabled={isProcessing}
                      className="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white rounded text-xs font-bold"
                    >
                      Generate Plan
                    </button>
                  </div>
                )}

                {hasPlan && plan && (
                  <div className="space-y-5">
                    {/* Mandatory Licenses */}
                    <div className="space-y-2">
                      <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider flex items-center gap-1.5">
                        <Server className="w-3.5 h-3.5 text-blue-700" />
                        <span>Mandatory Licenses</span>
                      </h3>

                      {plan.suggested_licenses.length === 0 ? (
                        <p className="text-xs text-slate-700 bg-slate-50 p-2.5 rounded border border-slate-200">
                          No mandatory rules found.
                        </p>
                      ) : (
                        <div className="overflow-x-auto rounded-lg border border-slate-300">
                          <table className="w-full text-left text-xs">
                            <thead className="bg-slate-100 text-slate-800 border-b border-slate-300 font-bold uppercase tracking-wider text-[11px]">
                              <tr>
                                <th className="p-2.5">Product</th>
                                <th className="p-2.5">Vendor</th>
                                <th className="p-2.5">Type</th>
                                <th className="p-2.5">Level</th>
                                <th className="p-2.5">Mandatory</th>
                                <th className="p-2.5">Approval</th>
                              </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-200 bg-white text-slate-900 font-medium">
                              {plan.suggested_licenses.map((lic, idx) => (
                                <tr key={idx} className="hover:bg-slate-50">
                                  <td className="p-2.5 font-bold text-slate-900">
                                    {lic.software_products?.name || 'Unknown'}
                                  </td>
                                  <td className="p-2.5 text-slate-700">
                                    {lic.software_products?.vendor || 'N/A'}
                                  </td>
                                  <td className="p-2.5 text-slate-700">
                                    {lic.software_products?.license_type || 'N/A'}
                                  </td>
                                  <td className="p-2.5 capitalize">{lic.access_level || 'standard'}</td>
                                  <td className="p-2.5 font-bold text-emerald-700">
                                    {lic.is_mandatory ? 'Yes' : 'No'}
                                  </td>
                                  <td className="p-2.5 text-slate-700">
                                    {lic.requires_approval ? 'Yes' : 'No'}
                                  </td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      )}
                    </div>

                    {/* Discretionary Licenses */}
                    {plan.discretionary_licenses?.length > 0 && (
                      <div className="space-y-2">
                        <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider flex items-center gap-1.5">
                          <FileCheck2 className="w-3.5 h-3.5 text-blue-700" />
                          <span>Discretionary Recommendations</span>
                        </h3>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                          {plan.discretionary_licenses.map((item) => {
                            const isChecked = (selectedDiscretionary[reqId] || []).includes(item.product_id);
                            return (
                              <label
                                key={item.product_id}
                                className={`p-3 rounded-lg border flex items-start gap-2.5 cursor-pointer text-xs transition-colors ${
                                  isChecked
                                    ? 'bg-blue-50 border-blue-400 text-blue-950'
                                    : 'bg-white border-slate-300 text-slate-800'
                                }`}
                              >
                                <input
                                  type="checkbox"
                                  checked={isChecked}
                                  onChange={() => handleToggleDiscretionary(reqId, item.product_id)}
                                  className="mt-0.5 rounded border-slate-300 text-blue-600 focus:ring-blue-600 w-4 h-4"
                                />
                                <div>
                                  <div className="font-bold text-slate-900 text-xs">
                                    {item.name}{' '}
                                    <span className="font-mono text-[10px] text-slate-600">
                                      ({item.product_id})
                                    </span>
                                  </div>
                                  <div className="text-[11px] text-slate-700 italic mt-0.5">
                                    "{item.justification || 'No justification'}"
                                  </div>
                                </div>
                              </label>
                            );
                          })}
                        </div>
                      </div>
                    )}

                    {/* Hardware & Policies */}
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                      <div className="p-3 rounded-lg border border-slate-300 bg-slate-50 space-y-1.5">
                        <h4 className="text-xs font-bold text-slate-900 flex items-center gap-1 uppercase tracking-wider">
                          <Laptop className="w-3.5 h-3.5 text-blue-700" />
                          <span>Hardware</span>
                        </h4>
                        <pre className="text-xs font-mono text-slate-900 overflow-x-auto p-2 bg-white border border-slate-200 rounded">
                          {JSON.stringify(plan.suggested_hardware, null, 2)}
                        </pre>
                      </div>

                      <div className="p-3 rounded-lg border border-slate-300 bg-slate-50 space-y-1.5">
                        <h4 className="text-xs font-bold text-slate-900 flex items-center gap-1 uppercase tracking-wider">
                          <ShieldAlert className="w-3.5 h-3.5 text-blue-700" />
                          <span>Policy Citations</span>
                        </h4>
                        <pre className="text-xs font-mono text-slate-900 overflow-x-auto p-2 bg-white border border-slate-200 rounded">
                          {JSON.stringify(plan.policy_citations, null, 2)}
                        </pre>
                      </div>
                    </div>

                    {/* Action Decision */}
                    {task.status === 'pending_approval' && (
                      <div className="pt-3 border-t border-slate-200 space-y-2.5">
                        <textarea
                          rows={2}
                          placeholder="Revision feedback or manual override details..."
                          value={reviewNotes[reqId] || ''}
                          onChange={(e) =>
                            setReviewNotes({ ...reviewNotes, [reqId]: e.target.value })
                          }
                          className="w-full bg-white border border-slate-300 rounded-lg p-2 text-xs text-slate-900 placeholder:text-slate-400 focus:outline-none focus:border-blue-600 focus:ring-1 focus:ring-blue-600 resize-none"
                        />

                        <div className="flex items-center gap-3">
                          <button
                            type="button"
                            onClick={() => handleReviewAction(reqId, 'regenerate')}
                            disabled={isProcessing}
                            className="flex-1 py-2 px-3 rounded-lg border border-slate-300 hover:bg-slate-100 text-xs font-bold text-slate-800 disabled:opacity-50 transition-colors"
                          >
                            {isProcessing ? 'Processing...' : 'Request Revision'}
                          </button>

                          <button
                            type="button"
                            onClick={() => handleReviewAction(reqId, 'approve')}
                            disabled={isProcessing}
                            className="flex-1 py-2 px-3 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold disabled:opacity-50 transition-colors"
                          >
                            {isProcessing ? 'Executing...' : 'Approve & Provision'}
                          </button>
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};