import React, { useEffect, useState, useCallback } from 'react';
import { 
  Zap, 
  Timer, 
  CheckCircle2, 
  TrendingUp, 
  RotateCw, 
} from 'lucide-react';
import type { KPIData } from '../types/analytics';
import { fetchWithAuth } from '../lib/api';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const KPIDashboard: React.FC = () => {
  const [data, setData] = useState<KPIData | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchKPIs = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetchWithAuth(`${API_BASE_URL}/analytics/kpis`);
      if (res.ok) {
        setData(await res.json());
      }
    } catch (err) {
      console.error('Failed to load KPIs:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchKPIs();
  }, [fetchKPIs]);

  if (loading && !data) {
    return (
      <div className="flex h-96 items-center justify-center text-slate-700 font-bold text-sm">
        <RotateCw className="w-5 h-5 animate-spin mr-2 text-blue-600" />
        Loading telemetry...
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-300 pb-4">
        <div>
          <h1 className="text-2xl font-black tracking-tight text-slate-900">
            System Telemetry
          </h1>
          <p className="text-xs text-slate-700 mt-0.5">
            Operational latency, token consumption, and approval accuracy.
          </p>
        </div>
        <button
          onClick={fetchKPIs}
          className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-white text-xs font-bold text-slate-800 border border-slate-300 hover:bg-slate-100 shadow-sm transition-colors"
        >
          <RotateCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          Refresh
        </button>
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        <div className="bg-white border border-slate-300 rounded-xl p-5 space-y-3 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-700">Tokens / Candidate</span>
            <div className="p-2 rounded-lg bg-blue-50 text-blue-700 border border-blue-200">
              <Zap className="w-4 h-4" />
            </div>
          </div>
          <div className="text-3xl font-black text-slate-900 font-mono">
            {data?.avg_tokens_per_employee.toLocaleString()}
          </div>
          <div className="pt-2 border-t border-slate-200 flex justify-between text-xs font-bold text-slate-900 font-mono">
            <span>Prompt: {data?.token_usage_breakdown.prompt.toLocaleString()}</span>
            <span>Completion: {data?.token_usage_breakdown.completion.toLocaleString()}</span>
          </div>
        </div>

        <div className="bg-white border border-slate-300 rounded-xl p-5 space-y-3 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-700">Planning Latency</span>
            <div className="p-2 rounded-lg bg-blue-50 text-blue-700 border border-blue-200">
              <Timer className="w-4 h-4" />
            </div>
          </div>
          <div className="text-3xl font-black text-slate-900 font-mono">
            {data?.avg_agent_execution_seconds}s
          </div>
          <div className="pt-2 border-t border-slate-200 flex justify-between text-xs font-semibold text-slate-900">
            <span>Total Lead Time:</span>
            <span className="font-mono font-bold text-slate-900">{data?.avg_total_lead_time_seconds}s</span>
          </div>
        </div>

        <div className="bg-white border border-slate-300 rounded-xl p-5 space-y-3 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-700">Approval Rate</span>
            <div className="p-2 rounded-lg bg-emerald-50 text-blue-700 border border-blue-200">
              <CheckCircle2 className="w-4 h-4" />
            </div>
          </div>
          <div className="text-3xl font-black text-slate-900 font-mono">
            {data?.first_pass_approval_rate}%
          </div>
          <div className="pt-2 border-t border-slate-200 flex justify-between text-xs font-semibold text-slate-900">
            <span>Escalation Rate:</span>
            <span className="font-mono font-bold text-slate-900">{data?.escalation_rate}%</span>
          </div>
        </div>
      </div>

      {/* Benchmark Summary */}
      <div className="bg-white border border-slate-300 rounded-xl p-5 shadow-sm">
        <h2 className="text-xs font-bold text-slate-900 uppercase tracking-wider mb-3 flex items-center gap-2">
          <TrendingUp className="w-4 h-4 text-blue-700" />
          <span>Operational Benchmark</span>
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-3 rounded-lg bg-slate-50 border border-slate-200">
            <div className="text-xs font-bold text-slate-700 uppercase">Legacy Method</div>
            <div className="text-lg font-black text-slate-900 mt-1">3 - 5 Business Days</div>
          </div>
          <div className="p-3 rounded-lg bg-blue-50 border border-blue-200">
            <div className="text-xs font-bold text-blue-700 uppercase">Automated Pipeline</div>
            <div className="text-lg font-black text-slate-900 font-mono mt-1">
              ~{((data?.avg_total_lead_time_seconds || 120) / 60).toFixed(1)} Minutes
            </div>
          </div>
        </div>
      </div>

      {/* Execution Log */}
      <div className="bg-white border border-slate-300 rounded-xl p-5 shadow-sm space-y-3">
        <h2 className="text-xs font-bold text-slate-900 uppercase tracking-wider">
          Execution Log
        </h2>
        <div className="overflow-x-auto rounded-lg border border-slate-300">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-100 text-slate-800 border-b border-slate-300 font-bold uppercase tracking-wider text-[11px]">
              <tr>
                <th className="p-2.5">Request ID</th>
                <th className="p-2.5">Attempt</th>
                <th className="p-2.5">Latency</th>
                <th className="p-2.5">Tokens</th>
                <th className="p-2.5">Action</th>
                <th className="p-2.5">Timestamp</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 bg-white text-slate-900 font-mono font-medium">
              {data?.recent_runs.map((run, idx) => (
                <tr key={idx} className="hover:bg-slate-50">
                  <td className="p-2.5 font-bold text-blue-700">{run.request_id}</td>
                  <td className="p-2.5 text-slate-800">#{run.attempt_number}</td>
                  <td className="p-2.5 text-slate-800">{run.execution_time_seconds}s</td>
                  <td className="p-2.5 text-slate-800">{run.tokens_total?.toLocaleString() || '-'}</td>
                  <td className="p-2.5">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider border ${
                      run.review_action === 'approve'
                        ? 'bg-emerald-50 text-emerald-800 border-emerald-300'
                        : run.review_action === 'regenerate'
                        ? 'bg-amber-50 text-amber-800 border-amber-300'
                        : 'bg-slate-100 text-slate-800 border-slate-300'
                    }`}>
                      {run.review_action || 'pending'}
                    </span>
                  </td>
                  <td className="p-2.5 text-slate-700 text-xs font-sans">
                    {new Date(run.created_at).toLocaleTimeString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};