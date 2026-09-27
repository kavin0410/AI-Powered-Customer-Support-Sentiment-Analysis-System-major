import React from 'react';
import { Menu, Sun, Moon, CheckCircle2, AlertTriangle, ShieldCheck } from 'lucide-react';

export default function Header({ onMenuClick, isDarkMode, onToggleTheme, backendStatus }) {
  return (
    <header className="sticky top-0 z-30 flex items-center justify-between h-16 px-4 sm:px-6 bg-white/80 dark:bg-slate-900/80 backdrop-blur-md border-b border-slate-200 dark:border-slate-800 transition-colors">
      {/* Left: Mobile hamburger & title */}
      <div className="flex items-center space-x-3">
        <button
          onClick={onMenuClick}
          className="p-2 -ml-2 rounded-xl text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 lg:hidden"
          aria-label="Toggle menu"
        >
          <Menu className="w-5 h-5" />
        </button>

        <div>
          <span className="hidden sm:inline-block text-xs font-semibold tracking-wider uppercase text-indigo-600 dark:text-indigo-400">
            Enterprise Intelligence
          </span>
          <h2 className="text-base sm:text-lg font-bold text-slate-900 dark:text-white leading-tight">
            AI Customer Support & Sentiment Analysis
          </h2>
        </div>
      </div>

      {/* Right: Health badge, Theme Switcher, Profile */}
      <div className="flex items-center space-x-3">
        {/* Backend health badge */}
        <div
          className={`hidden sm:flex items-center px-2.5 py-1 rounded-full text-xs font-medium border ${
            backendStatus === 'healthy'
              ? 'bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-400 border-emerald-200 dark:border-emerald-800/60'
              : 'bg-amber-50 dark:bg-amber-950/40 text-amber-700 dark:text-amber-400 border-amber-200 dark:border-amber-800/60'
          }`}
        >
          {backendStatus === 'healthy' ? (
            <>
              <CheckCircle2 className="w-3.5 h-3.5 mr-1.5 text-emerald-500" />
              API Connected
            </>
          ) : (
            <>
              <AlertTriangle className="w-3.5 h-3.5 mr-1.5 text-amber-500" />
              Connecting...
            </>
          )}
        </div>

        {/* Theme toggle button */}
        <button
          onClick={onToggleTheme}
          className="p-2 rounded-xl text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 border border-slate-200 dark:border-slate-800 transition-all duration-200 shadow-sm"
          title={isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
          aria-label="Toggle Theme"
        >
          {isDarkMode ? (
            <Sun className="w-4 h-4 text-amber-400 animate-spin-slow" />
          ) : (
            <Moon className="w-4 h-4 text-slate-700" />
          )}
        </button>

        {/* Profile Avatar */}
        <div className="flex items-center pl-2 border-l border-slate-200 dark:border-slate-800">
          <div className="flex items-center justify-center w-8 h-8 rounded-full bg-gradient-to-tr from-indigo-600 to-violet-500 text-white font-semibold text-xs shadow-sm">
            ML
          </div>
        </div>
      </div>
    </header>
  );
}
