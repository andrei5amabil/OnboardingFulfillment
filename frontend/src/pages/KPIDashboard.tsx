import React, { useEffect, useState, useCallback } from 'react';
import { 
  Zap, 
  Timer, 
  CheckCircle2, 
  AlertTriangle, 
  TrendingUp, 
  RotateCw, 
  Cpu, 
  ArrowUpRight 
} from 'lucide-react';
import type { KPIData } from '../types/analytics';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const KPIDashboard: React.FC = () => {
  const [data, setData] = useState<KPIData | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchKPIs = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE_URL}/analytics/kpis`);
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
      <div className="flex h-96 items-center justify-center text-slate-400">
        <RotateCw className="w-6 h-6 animate-spin mr-2" />
        Loading telemetry data...
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-100 flex items-center gap-2">
            <span>📈 System Efficiency & AI Telemetry</span>
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Real-time insights across LLM computational cost, latency targets, and HITL gatekeeper efficacy.
          </p>
        </div>
        <button
          onClick={fetchKPIs}
          className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-800 text-xs font-semibold text-slate-200 border border-slate-700 hover:bg-slate-700"
        >
          <RotateCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          Refresh Metrics
        </button>
      </div>

      {/* Top 3 Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        {/* KPI 1: Token Usage */}
        <div className="bg-slate-800/40 border border-slate-700/80 rounded-2xl p-5 space-y-3">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-medium uppercase tracking-wider">Avg LLM Consumption</span>
            <div className="p-2 rounded-lg bg-amber-500/10 text-amber-400">
              <Zap className="w-4 h-4" />
            </div>
          </div>
          <div>
            <div className="text-3xl font-extrabold text-slate-100 font-mono">
              {data?.avg_tokens_per_employee.toLocaleString()} <span className="text-sm font-normal text-slate-400">tokens</span>
            </div>
            <p className="text-xs text-slate-400 mt-1">Per candidate (Extraction + Agent Planner)</p>
          </div>
          <div className="pt-3 border-t border-slate-700/50 flex justify-between text-[11px] text-slate-400 font-mono">
            <span>Prompt: {data?.token_usage_breakdown.prompt.toLocaleString()}</span>
            <span>Completion: {data?.token_usage_breakdown.completion.toLocaleString()}</span>
          </div>
        </div>

        {/* KPI 2: Execution Latency */}
        <div className="bg-slate-800/40 border border-slate-700/80 rounded-2xl p-5 space-y-3">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-medium uppercase tracking-wider">Agent Planning Latency</span>
            <div className="p-2 rounded-lg bg-blue-500/10 text-blue-400">
              <Timer className="w-4 h-4" />
            </div>
          </div>
          <div>
            <div className="text-3xl font-extrabold text-slate-100 font-mono">
              {data?.avg_agent_execution_seconds}s
            </div>
            <p className="text-xs text-slate-400 mt-1">Average time to HITL gateway pause</p>
          </div>
          <div className="pt-3 border-t border-slate-700/50 flex justify-between text-[11px] text-slate-400">
            <span>Total Lead Time (End-to-End):</span>
            <span className="font-mono text-slate-200">{data?.avg_total_lead_time_seconds}s</span>
          </div>
        </div>

        {/* KPI 3: HITL Quality & Pass Rate */}
        <div className="bg-slate-800/40 border border-slate-700/80 rounded-2xl p-5 space-y-3">
          <div className="flex items-center justify-between text-slate-400">
            <span className="text-xs font-medium uppercase tracking-wider">HITL 1st-Pass Approval</span>
            <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400">
              <CheckCircle2 className="w-4 h-4" />
            </div>
          </div>
          <div>
            <div className="text-3xl font-extrabold text-emerald-400 font-mono">
              {data?.first_pass_approval_rate}%
            </div>
            <p className="text-xs text-slate-400 mt-1">Accepted without revision request</p>
          </div>
          <div className="pt-3 border-t border-slate-700/50 flex justify-between text-[11px] text-slate-400">
            <span>Escalation Rate (&gt;3 attempts):</span>
            <span className="font-mono text-rose-400">{data?.escalation_rate}%</span>
          </div>
        </div>
      </div>

      {/* Operational Efficiency Benchmark */}
      <div className="bg-slate-800/40 border border-slate-700/80 rounded-2xl p-6">
        <h2 className="text-sm font-bold text-slate-200 uppercase tracking-wider mb-4 flex items-center gap-2">
          <TrendingUp className="w-4 h-4 text-indigo-400" />
          <span>Operational Benchmark vs Traditional Process</span>
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-2">
            <span className="text-xs font-semibold text-rose-400 uppercase">Legacy Method (Manual IT/HR)</span>
            <div className="text-xl font-bold text-slate-300">3–5 Business Days (24–40h Lead Time)</div>
            <p className="text-xs text-slate-400">~3-4 hours hands-on time across 7+ manual touchpoints.</p>
          </div>
          <div className="p-4 rounded-xl bg-indigo-950/20 border border-indigo-500/30 space-y-2">
            <span className="text-xs font-semibold text-emerald-400 uppercase">AI Automated System (TO-BE)</span>
            <div className="text-xl font-bold text-slate-100 font-mono">
              ~{((data?.avg_total_lead_time_seconds || 120) / 60).toFixed(1)} Minutes Total Lead Time
            </div>
            <p className="text-xs text-slate-400">&gt;95% reduction in operational latency; 1-click HITL approval gate.</p>
          </div>
        </div>
      </div>

      {/* Recent Workflow Execution Telemetry Table */}
      <div className="bg-slate-800/40 border border-slate-700/80 rounded-2xl p-6 space-y-4">
        <h2 className="text-sm font-bold text-slate-200 uppercase tracking-wider">
          Recent Execution Log
        </h2>
        <div className="overflow-x-auto rounded-lg border border-slate-700/80">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-900/80 text-slate-400 border-b border-slate-700/80">
              <tr>
                <th className="p-3">Request ID</th>
                <th className="p-3">Attempt</th>
                <th className="p-3">Agent Latency</th>
                <th className="p-3">Tokens Total</th>
                <th className="p-3">Review Action</th>
                <th className="p-3">Timestamp</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800 bg-slate-900/40 text-slate-300 font-mono">
              {data?.recent_runs.map((run, idx) => (
                <tr key={idx} className="hover:bg-slate-800/30">
                  <td className="p-3 font-semibold text-indigo-400">{run.request_id}</td>
                  <td className="p-3">#{run.attempt_number}</td>
                  <td className="p-3">{run.execution_time_seconds}s</td>
                  <td className="p-3">{run.tokens_total?.toLocaleString() || '-'}</td>
                  <td className="p-3">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-semibold uppercase ${
                      run.review_action === 'approve'
                        ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                        : run.review_action === 'regenerate'
                        ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                        : 'bg-slate-800 text-slate-400'
                    }`}>
                      {run.review_action || 'pending'}
                    </span>
                  </td>
                  <td className="p-3 text-slate-500 text-[11px]">
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