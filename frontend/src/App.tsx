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

  useEffect(() => {
    if (role === 'new_hire') {
      setCurrentTab('portal');
    } else if (role === 'it_manager') {
      setCurrentTab('it');
    } else if (role === 'hr_manager' || role === 'admin') {
      setCurrentTab('hr');
    }
  }, [role]);

  const handleTabChange = (tab: NavTab) => {
    if (role === 'new_hire' && tab !== 'portal') return;
    if (role !== 'new_hire' && tab === 'portal') return;
    setCurrentTab(tab);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center text-slate-500">
        <Loader2 className="w-7 h-7 animate-spin text-blue-600" />
      </div>
    );
  }

  if (!user) {
    return <LoginPage />;
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col font-sans selection:bg-blue-600 selection:text-white antialiased">
      <Navbar currentTab={currentTab} onTabChange={handleTabChange} />

      <main className="flex-1 pb-16">
        {currentTab === 'hr' && (role === 'admin' || role === 'hr_manager') && <HrIntakePage />}
        {currentTab === 'it' && (role === 'admin' || role === 'it_manager') && <ITApprovalsPage />}
        {currentTab === 'kpi' && (role === 'admin' || role === 'hr_manager' || role === 'it_manager') && <KPIDashboard />}
        {currentTab === 'portal' && role === 'new_hire' && <NewHirePortal />}
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