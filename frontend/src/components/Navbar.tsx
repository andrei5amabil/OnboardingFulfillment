import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import {
  FileText,
  CheckSquare,
  BarChart3,
  UserCheck,
  LogOut,
  ShieldAlert,
  Copy,
  Check,
} from 'lucide-react';

export type NavTab = 'hr' | 'it' | 'kpi' | 'portal';

interface NavbarProps {
  currentTab: NavTab;
  onTabChange: (tab: NavTab) => void;
}

export const Navbar: React.FC<NavbarProps> = ({ currentTab, onTabChange }) => {
  const { user, role, signOut } = useAuth();
  const [copiedEmail, setCopiedEmail] = useState(false);

  const handleCopyEmail = () => {
    if (user?.email) {
      navigator.clipboard.writeText(user.email);
      setCopiedEmail(true);
      setTimeout(() => setCopiedEmail(false), 2000);
    }
  };

  const handleLogout = async () => {
    await signOut();
  };

  return (
    <header className="border-b border-slate-800 bg-slate-900/50 backdrop-blur sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-2 font-bold text-slate-100 tracking-tight">
            <div className="p-1.5 bg-indigo-600 rounded-lg text-white">
              <ShieldAlert className="w-4 h-4" />
            </div>
            <span>AutoOnboard</span>
          </div>

          <nav className="flex items-center gap-1">
            {/* HR Intake Tab */}
            {(role === 'admin' || role === 'hr_manager') && (
              <button
                onClick={() => onTabChange('hr')}
                className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                  currentTab === 'hr'
                    ? 'bg-indigo-600/10 text-indigo-400 border border-indigo-500/30'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                }`}
              >
                <FileText className="w-3.5 h-3.5" />
                <span>HR Intake</span>
              </button>
            )}

            {/* IT Approvals Tab */}
            {(role === 'admin' || role === 'it_manager') && (
              <button
                onClick={() => onTabChange('it')}
                className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                  currentTab === 'it'
                    ? 'bg-indigo-600/10 text-indigo-400 border border-indigo-500/30'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                }`}
              >
                <CheckSquare className="w-3.5 h-3.5" />
                <span>IT Approvals</span>
              </button>
            )}

            {/* KPI Telemetry Tab */}
            {(role === 'admin' || role === 'hr_manager' || role === 'it_manager') && (
              <button
                onClick={() => onTabChange('kpi')}
                className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                  currentTab === 'kpi'
                    ? 'bg-indigo-600/10 text-indigo-400 border border-indigo-500/30'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                }`}
              >
                <BarChart3 className="w-3.5 h-3.5" />
                <span>Telemetry</span>
              </button>
            )}

            {/* New Hire Hub Tab */}
            {(role === 'admin' || role === 'new_hire') && (
              <button
                onClick={() => onTabChange('portal')}
                className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
                  currentTab === 'portal'
                    ? 'bg-indigo-600/10 text-indigo-400 border border-indigo-500/30'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                }`}
              >
                <UserCheck className="w-3.5 h-3.5" />
                <span>New Hire Hub</span>
              </button>
            )}
          </nav>
        </div>

        <div className="flex items-center gap-3">
          {/* Clickable Corporate Email with Copy Feedback */}
          <button
            type="button"
            onClick={handleCopyEmail}
            title="Click to copy work email"
            className="group flex flex-col text-right hover:opacity-95 transition-opacity focus:outline-none"
          >
            <span className="text-xs font-medium text-slate-200 group-hover:text-indigo-400 flex items-center justify-end gap-1.5 transition-colors">
              <span>{user?.email}</span>
            </span>
            <span className="text-[10px] font-mono uppercase tracking-wider text-indigo-400">
              {copiedEmail ? (
                <span className="text-emerald-400 font-sans normal-case">Copied to clipboard</span>
              ) : (
                role
              )}
            </span>
          </button>

          <button
            onClick={handleLogout}
            title="Sign Out"
            className="p-2 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800 border border-slate-800 transition-colors"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </header>
  );
};