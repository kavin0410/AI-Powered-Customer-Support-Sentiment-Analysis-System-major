import React from 'react';

export default function ChartCard({ title, subtitle, children, action }) {
  return (
    <div className="p-5 bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm transition-colors">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h4 className="text-sm sm:text-base font-bold text-slate-900 dark:text-white leading-tight">
            {title}
          </h4>
          {subtitle && (
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
              {subtitle}
            </p>
          )}
        </div>
        {action && <div>{action}</div>}
      </div>

      <div className="w-full">
        {children}
      </div>
    </div>
  );
}
