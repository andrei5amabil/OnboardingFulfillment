import { useState } from 'react';
import { Navbar, type NavTab } from './components/Navbar';
import { HrIntakePage } from './pages/HRIntake';
import { ITApprovalsPage } from './pages/ITApprovals';

export default function App() {
  const [currentTab, setCurrentTab] = useState<NavTab>('hr');

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-indigo-500 selection:text-white">
      {/* Sticky Top Navigation */}
      <Navbar currentTab={currentTab} onTabChange={setCurrentTab} />

      {/* Main Page View */}
      <main className="flex-1">
        {currentTab === 'hr' ? <HrIntakePage /> : <ITApprovalsPage />}
      </main>
    </div>
  );
}