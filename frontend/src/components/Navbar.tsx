import React from 'react';
import { UserCheck, ShieldAlert, Cpu, TrendingUp, Laptop, LogOut } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export type NavTab = 'hr' | 'it' | 'kpi' | 'portal';

interface NavbarProps {
  currentTab: NavTab;
  onTabChange: (tab: NavTab) => void;
  pendingCount?: number;
}

export const Navbar: React.FC<NavbarProps> = ({
  currentTab,
  onTabChange,
  pendingCount = 0,
}) => {
  const { user, role, employeeId, signOut } = useAuth();

  const showHR = role === 'admin' || role === 'hr_manager';
  const showIT = role === 'admin' || role === 'it_manager';
  const showKPI = role === 'admin' || role === 'hr_manager' || role === 'it_manager';
  const showPortal = role === 'admin' || role === 'new_hire';

  return (
    <header className="sticky top-0 z-50 border-b border-slate-800 bg-slate-900/80 backdrop-blur-md">
      <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
        {/* Brand / Logo */}
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-xl bg-indigo-600/20 border border-indigo-500/30 text-indigo-400">
            <Cpu className="w-5 h-5" />
          </div>
          <div>
            <div className="font-bold text-sm text-slate-100">
              Onboarding Fulfillment
            </div>
            <p className="text-[11px] text-slate-400">HITL Access & Hardware Provisioning</p>
          </div>
        </div>

        {/* Role-Filtered Navigation Tabs */}
        <nav className="flex items-center gap-1 bg-slate-950/60 p-1 rounded-xl border border-slate-800">
          {showHR && (
            <button
              type="button"
              onClick={() => onTabChange('hr')}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                currentTab === 'hr'
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
              }`}
            >
              <UserCheck className="w-4 h-4" />
              <span>HR Intake</span>
            </button>
          )}

          {showIT && (
            <button
              type="button"
              onClick={() => onTabChange('it')}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                currentTab === 'it'
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
              }`}
            >
              <ShieldAlert className="w-4 h-4" />
              <span>IT Approvals</span>
              {pendingCount > 0 && (
                <span className="ml-1 px-1.5 py-0.2 rounded-full bg-amber-500 text-slate-950 text-[10px] font-bold">
                  {pendingCount}
                </span>
              )}
            </button>
          )}

          {showKPI && (
            <button
              type="button"
              onClick={() => onTabChange('kpi')}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                currentTab === 'kpi'
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
              }`}
            >
              <TrendingUp className="w-4 h-4" />
              <span>KPI Analytics</span>
            </button>
          )}

          {showPortal && (
            <button
              type="button"
              onClick={() => onTabChange('portal')}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                currentTab === 'portal'
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
              }`}
            >
              <Laptop className="w-4 h-4" />
              <span>New Hire Hub</span>
            </button>
          )}
        </nav>

        <div className="flex items-center gap-3">
          <div className="hidden sm:flex flex-col items-end">
            <span className="text-xs text-slate-200 font-medium">{user?.email}</span>
            <span className="text-[10px] font-mono text-indigo-400 uppercase">
              {role?.replace('_', ' ')} {employeeId ? `• ${employeeId}` : ''}
            </span>
          </div>

          <button
            onClick={signOut}
            title="Sign Out"
            className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-rose-400 border border-slate-700 transition-colors"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </header>
  );
};