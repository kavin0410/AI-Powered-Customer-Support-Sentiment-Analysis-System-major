import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import Dashboard from './pages/Dashboard';
import Prediction from './pages/Prediction';
import FeedbackExplorer from './pages/FeedbackExplorer';
import SentimentAnalysis from './pages/SentimentAnalysis';
import IssueAnalysis from './pages/IssueAnalysis';
import BusinessInsights from './pages/BusinessInsights';
import About from './pages/About';
import { checkHealth } from './services/api';

export default function App() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [backendStatus, setBackendStatus] = useState('unknown');

  // Theme state persisted in localStorage
  const [isDarkMode, setIsDarkMode] = useState(() => {
    const saved = localStorage.getItem('theme');
    if (saved) return saved === 'dark';
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  });

  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  }, [isDarkMode]);

  // Periodic health check
  useEffect(() => {
    let isMounted = true;
    const pollHealth = async () => {
      try {
        const data = await checkHealth();
        if (isMounted) {
          setBackendStatus(data.status === 'healthy' ? 'healthy' : 'degraded');
        }
      } catch (err) {
        if (isMounted) {
          setBackendStatus('unreachable');
        }
      }
    };

    pollHealth();
    const interval = setInterval(pollHealth, 30000);
    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, []);

  const toggleTheme = () => {
    setIsDarkMode((prev) => !prev);
  };

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 flex flex-col transition-colors">
        {/* Responsive Sidebar */}
        <Sidebar
          isOpen={isSidebarOpen}
          onClose={() => setIsSidebarOpen(false)}
        />

        {/* Main Content Area */}
        <div className="flex-1 flex flex-col lg:pl-64">
          <Header
            onMenuClick={() => setIsSidebarOpen(true)}
            isDarkMode={isDarkMode}
            onToggleTheme={toggleTheme}
            backendStatus={backendStatus}
          />

          <main className="flex-1 p-4 sm:p-6 lg:p-8 max-w-7xl w-full mx-auto">
            <Routes>
              <Route path="/" element={<Navigate to="/dashboard" replace />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/prediction" element={<Prediction />} />
              <Route path="/feedback" element={<FeedbackExplorer />} />
              <Route path="/sentiment" element={<SentimentAnalysis />} />
              <Route path="/issues" element={<IssueAnalysis />} />
              <Route path="/insights" element={<BusinessInsights />} />
              <Route path="/about" element={<About />} />
              <Route path="*" element={<Navigate to="/dashboard" replace />} />
            </Routes>
          </main>
        </div>
      </div>
    </BrowserRouter>
  );
}
