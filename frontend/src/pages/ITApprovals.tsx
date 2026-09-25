import React, { useState, useEffect, useCallback, useMemo } from 'react';
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

  // Per-task interaction states
  const [selectedDiscretionary, setSelectedDiscretionary] = useState<Record<string, string[]>>({});
  const [reviewNotes, setReviewNotes] = useState<Record<string, string>>({});
  const [actionLoading, setActionLoading] = useState<Record<string, boolean>>({});

  // Fetch tasks (silent=true avoids full-screen spinner on background sync)
  const fetchTasks = useCallback(async (silent = false) => {
    if (!silent) setIsLoading(true);
    else setIsSyncing(true);
    setError(null);

    try {
      const res = await fetch(`${API_BASE_URL}/onboarding/requests`);
      if (!res.ok) throw new Error(`HTTP error: ${res.status}`);
      const data: OnboardingRequest[] = await res.json();

      const pending = data.filter((t) => t.status !== 'completed');
      setTasks(pending);

      // Preserve existing selections or set default discretionary choices
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
      setError(err.message || 'Could not load pending tasks from backend.');
    } finally {
      setIsLoading(false);
      setIsSyncing(false);
    }
  }, []);

  // 1. Initial Load
  useEffect(() => {
    fetchTasks(false);
  }, [fetchTasks]);

  // 2. Reactive Auto-Polling: Activates ONLY when any task is actively processing
  const hasProcessingTasks = useMemo(
    () => tasks.some((t) => t.status === 'processing_rules'),
    [tasks]
  );

  useEffect(() => {
    if (!hasProcessingTasks) return;

    // Poll every 2.5s while LangGraph is running rules/retrievals
    const interval = setInterval(() => {
      fetchTasks(true);
    }, 2500);

    return () => clearInterval(interval);
  }, [hasProcessingTasks, fetchTasks]);

  // 3. Supabase Realtime Listener: Instantly refreshes on table updates
  useEffect(() => {
    const channel = supabase
      .channel('schema-db-changes')
      .on(
        'postgres_changes',
        { event: '*', schema: 'public', table: 'onboarding_requests' },
        () => {
          fetchTasks(true);
        }
      )
      .on(
        'postgres_changes',
        { event: 'INSERT', schema: 'public', table: 'workflow_runs' },
        () => {
          fetchTasks(true);
        }
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
      const res = await fetch(`${API_BASE_URL}/onboarding/requests/${requestId}/generate-plan`, {
        method: 'POST',
      });
      if (!res.ok) throw new Error('Failed to queue plan generation.');
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
      const res = await fetch(`${API_BASE_URL}/onboarding/requests/${requestId}/review`, {
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
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-100 flex items-center gap-2">
            <span>🛠️ IT Provisioning & Approvals</span>
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Review agent-generated access plans, request revisions, or commit deterministic provisioning.
          </p>
        </div>

        <div className="flex items-center gap-2 self-start sm:self-auto">
          {/* Live Sync Status Pill */}
          <div className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-[11px] font-mono text-slate-400">
            <Radio
              className={`w-3.5 h-3.5 ${
                hasProcessingTasks || isSyncing
                  ? 'text-amber-400 animate-pulse'
                  : 'text-emerald-400'
              }`}
            />
            <span>
              {hasProcessingTasks
                ? 'Agent Working...'
                : isSyncing
                ? 'Syncing...'
                : 'Realtime Connected'}
            </span>
          </div>

          <button
            type="button"
            onClick={() => fetchTasks(false)}
            disabled={isLoading}
            className="flex items-center gap-2 px-3.5 py-1.5 text-xs font-semibold rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 disabled:opacity-50 transition-colors"
          >
            <RotateCw className={`w-3.5 h-3.5 ${isLoading ? 'animate-spin' : ''}`} />
            <span>Refresh</span>
          </button>
        </div>
      </div>

      {error && (
        <div className="p-4 bg-rose-500/10 border border-rose-500/30 rounded-xl flex items-center gap-3 text-xs text-rose-300">
          <AlertCircle className="w-5 h-5 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Task Queue */}
      {tasks.length === 0 && !isLoading ? (
        <div className="p-12 text-center border border-slate-800 bg-slate-900/50 rounded-2xl">
          <CheckCircle className="w-10 h-10 text-emerald-400 mx-auto mb-3 opacity-80" />
          <h3 className="text-base font-semibold text-slate-200">No actions awaiting IT approval</h3>
          <p className="text-xs text-slate-500 mt-1">All onboarding pipelines have been finalized.</p>
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
                className="bg-slate-800/40 border border-slate-700/80 rounded-2xl p-6 space-y-5"
              >
                {/* Card Title & Meta */}
                <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-700/60 gap-2">
                  <div>
                    <h2 className="text-lg font-bold text-slate-100">
                      {task.first_name} {task.last_name}
                    </h2>
                    <p className="text-xs text-slate-400 mt-0.5">
                      {task.department} • <span className="text-indigo-400">{task.role}</span>
                    </p>
                  </div>
                  <div className="flex items-center gap-3 text-xs font-mono">
                    <span className="text-slate-400">ID: {reqId}</span>
                    <span
                      className={`px-2.5 py-1 rounded-full text-[11px] font-semibold uppercase tracking-wider ${
                        task.status === 'pending_approval'
                          ? 'bg-amber-500/10 border border-amber-500/30 text-amber-300'
                          : task.status === 'processing_rules'
                          ? 'bg-blue-500/10 border border-blue-500/30 text-blue-300'
                          : task.status === 'failed'
                          ? 'bg-rose-500/10 border border-rose-500/30 text-rose-300'
                          : 'bg-slate-700 text-slate-300'
                      }`}
                    >
                      {task.status}
                    </span>
                  </div>
                </div>

                {/* State: Processing Rules (Agent is active) */}
                {task.status === 'processing_rules' && (
                  <div className="p-4 bg-indigo-500/10 border border-indigo-500/30 rounded-xl flex items-center justify-between">
                    <div className="flex items-center gap-3 text-xs text-indigo-300">
                      <Loader2 className="w-4 h-4 animate-spin text-indigo-400 shrink-0" />
                      <span>
                        Agent is generating the plan and evaluating policies. The page will
                        update automatically when the approval gate is ready...
                      </span>
                    </div>
                  </div>
                )}

                {/* State: Failed */}
                {task.status === 'failed' && (
                  <div className="p-4 bg-rose-500/10 border border-rose-500/30 rounded-xl flex items-center justify-between">
                    <div className="flex items-center gap-2 text-xs text-rose-300">
                      <XCircle className="w-4 h-4" />
                      <span>Plan generation failed in the background.</span>
                    </div>
                    <button
                      onClick={() => handleGeneratePlan(reqId)}
                      disabled={isProcessing}
                      className="px-3 py-1.5 bg-rose-600 hover:bg-rose-500 text-white rounded text-xs font-semibold"
                    >
                      Retry Generation
                    </button>
                  </div>
                )}

                {/* State: Requires Manual Intervention */}
                {task.status === 'requires_manual_intervention' && (
                  <div className="p-4 bg-rose-500/20 border border-rose-500/40 rounded-xl flex items-center gap-2 text-xs text-rose-300">
                    <AlertCircle className="w-5 h-5 shrink-0" />
                    <span>
                      Maximum revision attempts reached (3/3). This request requires manual IT
                      handling.
                    </span>
                  </div>
                )}

                {/* State: Intake Received, No Plan Yet */}
                {task.status === 'pending_onboarding' && !hasPlan && (
                  <div className="p-4 bg-amber-500/10 border border-amber-500/30 rounded-xl flex items-center justify-between">
                    <span className="text-xs text-amber-300">
                      Request intake received, but plan has not executed.
                    </span>
                    <button
                      onClick={() => handleGeneratePlan(reqId)}
                      disabled={isProcessing}
                      className="px-3 py-1.5 bg-amber-600 hover:bg-amber-500 text-white rounded text-xs font-semibold"
                    >
                      Launch Agent Planner
                    </button>
                  </div>
                )}

                {/* State: Plan Generated & Available (HITL Approval Gate) */}
                {hasPlan && plan && (
                  <div className="space-y-5">
                    {/* Deterministic SQL Entitlements */}
                    <div className="space-y-2">
                      <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
                        <Server className="w-3.5 h-3.5 text-indigo-400" />
                        <span>Deterministic Entitlement Plan (SQL Rules)</span>
                      </h3>

                      {plan.suggested_licenses.length === 0 ? (
                        <p className="text-xs text-amber-400/80 bg-slate-900/50 p-3 rounded-lg border border-slate-800">
                          No explicit assignment rules found for this role and department.
                        </p>
                      ) : (
                        <div className="overflow-x-auto rounded-lg border border-slate-700/80">
                          <table className="w-full text-left text-xs">
                            <thead className="bg-slate-900/80 text-slate-400 border-b border-slate-700/80">
                              <tr>
                                <th className="p-2.5">Product</th>
                                <th className="p-2.5">Vendor</th>
                                <th className="p-2.5">Type</th>
                                <th className="p-2.5">Level</th>
                                <th className="p-2.5">Mandatory</th>
                                <th className="p-2.5">Approval</th>
                              </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-800 bg-slate-900/40 text-slate-200">
                              {plan.suggested_licenses.map((lic, idx) => (
                                <tr key={idx} className="hover:bg-slate-800/30">
                                  <td className="p-2.5 font-medium">
                                    {lic.software_products?.name || 'Unknown'}
                                  </td>
                                  <td className="p-2.5 text-slate-400">
                                    {lic.software_products?.vendor || 'N/A'}
                                  </td>
                                  <td className="p-2.5 text-slate-400">
                                    {lic.software_products?.license_type || 'N/A'}
                                  </td>
                                  <td className="p-2.5">{lic.access_level || 'standard'}</td>
                                  <td className="p-2.5">{lic.is_mandatory ? '✅' : '❌'}</td>
                                  <td className="p-2.5 text-slate-400">
                                    {lic.requires_approval ? 'Yes' : 'No'}
                                  </td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      )}
                    </div>

                    {/* Discretionary AI Recommendations */}
                    {plan.discretionary_licenses?.length > 0 && (
                      <div className="space-y-2">
                        <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
                          <FileCheck2 className="w-3.5 h-3.5 text-indigo-400" />
                          <span>AI Discretionary Recommendations (Based on Notes)</span>
                        </h3>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                          {plan.discretionary_licenses.map((item) => {
                            const isChecked = (selectedDiscretionary[reqId] || []).includes(
                              item.product_id
                            );
                            return (
                              <label
                                key={item.product_id}
                                className={`p-3 rounded-lg border flex items-start gap-2.5 cursor-pointer text-xs transition-colors ${
                                  isChecked
                                    ? 'bg-indigo-600/10 border-indigo-500/40 text-indigo-200'
                                    : 'bg-slate-900/40 border-slate-800 text-slate-400'
                                }`}
                              >
                                <input
                                  type="checkbox"
                                  checked={isChecked}
                                  onChange={() =>
                                    handleToggleDiscretionary(reqId, item.product_id)
                                  }
                                  className="mt-0.5 rounded border-slate-700 bg-slate-900 text-indigo-600"
                                />
                                <div>
                                  <div className="font-semibold text-slate-100">
                                    {item.name}{' '}
                                    <span className="font-mono text-[10px] text-slate-400">
                                      ({item.product_id})
                                    </span>
                                  </div>
                                  <div className="text-[11px] text-slate-400 italic mt-0.5">
                                    "{item.justification || 'No justification provided.'}"
                                  </div>
                                </div>
                              </label>
                            );
                          })}
                        </div>
                      </div>
                    )}

                    {/* Hardware & Policy Citations Split */}
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      {/* Hardware */}
                      <div className="p-3.5 rounded-xl border border-slate-700/60 bg-slate-900/40 space-y-2">
                        <h4 className="text-xs font-semibold text-slate-300 flex items-center gap-1.5">
                          <Laptop className="w-3.5 h-3.5 text-indigo-400" />
                          <span>Suggested Hardware</span>
                        </h4>
                        <pre className="text-[11px] font-mono text-slate-400 overflow-x-auto p-2 bg-slate-950/50 rounded">
                          {JSON.stringify(plan.suggested_hardware, null, 2)}
                        </pre>
                      </div>

                      {/* Policy Citations */}
                      <div className="p-3.5 rounded-xl border border-slate-700/60 bg-slate-900/40 space-y-2">
                        <h4 className="text-xs font-semibold text-slate-300 flex items-center gap-1.5">
                          <ShieldAlert className="w-3.5 h-3.5 text-indigo-400" />
                          <span>Policy Citations & Flags</span>
                        </h4>
                        <pre className="text-[11px] font-mono text-slate-400 overflow-x-auto p-2 bg-slate-950/50 rounded">
                          {JSON.stringify(plan.policy_citations, null, 2)}
                        </pre>
                      </div>
                    </div>

                    {/* HITL Review Gateway */}
                    {task.status === 'pending_approval' && (
                      <div className="pt-4 border-t border-slate-700/60 space-y-3">
                        <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider">
                          ⚖️ IT Review Decision
                        </h4>

                        <textarea
                          rows={2}
                          placeholder="Revision notes/feedback (e.g., Provide 32GB RAM model instead)..."
                          value={reviewNotes[reqId] || ''}
                          onChange={(e) =>
                            setReviewNotes({ ...reviewNotes, [reqId]: e.target.value })
                          }
                          className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-xs text-slate-100 placeholder:text-slate-500 focus:outline-none focus:border-indigo-500 resize-none"
                        />

                        <div className="flex items-center gap-3">
                          <button
                            type="button"
                            onClick={() => handleReviewAction(reqId, 'regenerate')}
                            disabled={isProcessing}
                            className="flex-1 py-2 px-3 rounded-lg border border-slate-700 hover:bg-slate-700 text-xs font-semibold text-slate-300 disabled:opacity-50 transition-colors"
                          >
                            {isProcessing ? 'Processing...' : '🔄 Regenerate Plan'}
                          </button>

                          <button
                            type="button"
                            onClick={() => handleReviewAction(reqId, 'approve')}
                            disabled={isProcessing}
                            className="flex-1 py-2 px-3 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold shadow-md shadow-emerald-600/20 disabled:opacity-50 transition-colors"
                          >
                            {isProcessing ? 'Executing...' : '🚀 Approve & Provision'}
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