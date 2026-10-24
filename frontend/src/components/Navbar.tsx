import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import {
  FileText,
  CheckSquare,
  BarChart3,
  UserCheck,
  LogOut,
  ShieldCheck,
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

  const navButtonClass = (tab: NavTab) =>
    `flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
      currentTab === tab
        ? 'bg-blue-50 text-blue-700 font-semibold border border-blue-200'
        : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
    }`;

  return (
    <header className="border-b border-slate-200 bg-white/95 backdrop-blur-sm sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-2.5 font-bold text-slate-900 tracking-tight">
            <div className="p-1.5 bg-blue-600 rounded-lg text-white shadow-sm">
              <ShieldCheck className="w-4 h-4" />
            </div>
            <span>AutOnboard</span>
          </div>

          <nav className="flex items-center gap-1">
            {(role === 'admin' || role === 'hr_manager') && (
              <button onClick={() => onTabChange('hr')} className={navButtonClass('hr')}>
                <FileText className="w-3.5 h-3.5" />
                <span>HR Intake</span>
              </button>
            )}

            {(role === 'admin' || role === 'it_manager') && (
              <button onClick={() => onTabChange('it')} className={navButtonClass('it')}>
                <CheckSquare className="w-3.5 h-3.5" />
                <span>IT Approvals</span>
              </button>
            )}

            {(role === 'admin' || role === 'hr_manager' || role === 'it_manager') && (
              <button onClick={() => onTabChange('kpi')} className={navButtonClass('kpi')}>
                <BarChart3 className="w-3.5 h-3.5" />
                <span>Telemetry</span>
              </button>
            )}

            {( role === 'new_hire') && (
              <button onClick={() => onTabChange('portal')} className={navButtonClass('portal')}>
                <UserCheck className="w-3.5 h-3.5" />
                <span>New Hire Hub</span>
              </button>
            )}
          </nav>
        </div>

        <div className="flex items-center gap-3">
          <button
            type="button"
            onClick={handleCopyEmail}
            title="Click to copy work email"
            className="group flex flex-col text-right hover:opacity-85 transition-opacity focus:outline-none"
          >
            <span className="text-xs font-medium text-slate-800 group-hover:text-blue-600 transition-colors">
              {user?.email}
            </span>
            <span className="text-[10px] font-mono uppercase tracking-wider text-slate-400 group-hover:text-slate-600">
              {copiedEmail ? (
                <span className="text-emerald-600 font-sans normal-case font-medium">Copied!</span>
              ) : (
                role?.replace('_', ' ')
              )}
            </span>
          </button>

          <div className="h-4 w-px bg-slate-200 mx-1" />

          <button
            onClick={() => signOut()}
            title="Sign Out"
            className="p-2 rounded-lg text-slate-500 hover:text-slate-800 hover:bg-slate-100 border border-slate-200 transition-colors"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </header>
  );
};