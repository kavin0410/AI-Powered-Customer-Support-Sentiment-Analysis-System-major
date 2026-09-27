import React from 'react';

export default function MetricCard({ title, value, subtext, icon: Icon, accent = 'indigo', badge }) {
  const accentBorderColors = {
    indigo: 'border-t-indigo-500 text-indigo-600 dark:text-indigo-400 bg-indigo-50 dark:bg-indigo-950/40',
    emerald: 'border-t-emerald-500 text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/40',
    rose: 'border-t-rose-500 text-rose-600 dark:text-rose-400 bg-rose-50 dark:bg-rose-950/40',
    sky: 'border-t-sky-500 text-sky-600 dark:text-sky-400 bg-sky-50 dark:bg-sky-950/40',
    amber: 'border-t-amber-500 text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-950/40',
    purple: 'border-t-purple-500 text-purple-600 dark:text-purple-400 bg-purple-50 dark:bg-purple-950/40',
  };

  const selectedAccent = accentBorderColors[accent] || accentBorderColors.indigo;

  return (
    <div className={`relative p-5 bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 border-t-4 shadow-sm hover:shadow-md transition-all duration-200 ${selectedAccent.split(' ')[0]}`}>
      <div className="flex items-center justify-between">
        <span className="text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
          {title}
        </span>
        {Icon && (
          <div className={`p-2 rounded-xl ${selectedAccent.split(' ').slice(1).join(' ')}`}>
            <Icon className="w-4 h-4" />
          </div>
        )}
      </div>

      <div className="mt-2 flex items-baseline justify-between">
        <h3 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-slate-900 dark:text-white truncate">
          {value}
        </h3>
        {badge && (
          <span className="ml-2 px-2 py-0.5 text-xs font-semibold rounded-md bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300">
            {badge}
          </span>
        )}
      </div>

      {subtext && (
        <p className="mt-1 text-xs text-slate-500 dark:text-slate-400 font-medium truncate">
          {subtext}
        </p>
      )}
    </div>
  );
}
