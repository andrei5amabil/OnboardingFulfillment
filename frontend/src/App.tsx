import React, { useState, useEffect } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import { Navbar, type NavTab } from './components/Navbar';
import { HrIntakePage } from './pages/HRIntake';
import { ITApprovalsPage } from './pages/ITApprovals';
import { KPIDashboard } from './pages/KPIDashboard';
import { NewHirePortal } from './pages/NewHirePortal';
import { LoginPage } from './pages/LoginPage';
import { Loader2 } from 'lucide-react';

const AppShell: React.FC = () => {
  const { user, role, loading } = useAuth();
  const [currentTab, setCurrentTab] = useState<NavTab>('hr');

  // Set default landing tab when role is resolved
  useEffect(() => {
    if (role === 'new_hire') {
      setCurrentTab('portal');
    } else if (role === 'it_manager') {
      setCurrentTab('it');
    } else if (role === 'hr_manager' || role === 'admin') {
      setCurrentTab('hr');
    }
  }, [role]);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center text-slate-400">
        <Loader2 className="w-8 h-8 animate-spin text-indigo-500" />
      </div>
    );
  }

  if (!user) {
    return <LoginPage />;
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-indigo-500 selection:text-white">
      <Navbar currentTab={currentTab} onTabChange={setCurrentTab} />

      <main className="flex-1">
        {currentTab === 'hr' && (role === 'admin' || role === 'hr_manager') && <HrIntakePage />}
        {currentTab === 'it' && (role === 'admin' || role === 'it_manager') && <ITApprovalsPage />}
        {currentTab === 'kpi' && (role === 'admin' || role === 'hr_manager' || role === 'it_manager') && <KPIDashboard />}
        {currentTab === 'portal' && (role === 'admin' || role === 'new_hire') && <NewHirePortal />}
      </main>
    </div>
  );
};

export default function App() {
  return (
    <AuthProvider>
      <AppShell />
    </AuthProvider>
  );
}