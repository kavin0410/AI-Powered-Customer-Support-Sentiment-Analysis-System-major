import React from 'react';
import { AlertCircle, RefreshCw } from 'lucide-react';

export function LoadingSpinner({ message = 'Loading live analytics...' }) {
  return (
    <div className="flex flex-col items-center justify-center p-12 text-center">
      <div className="w-10 h-10 border-4 border-indigo-200 dark:border-indigo-950 border-t-indigo-600 rounded-full animate-spin" />
      <p className="mt-4 text-sm font-medium text-slate-500 dark:text-slate-400">
        {message}
      </p>
    </div>
  );
}

export function ErrorState({ message, onRetry }) {
  return (
    <div className="p-8 rounded-2xl bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900/60 text-center max-w-lg mx-auto my-8">
      <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-rose-100 dark:bg-rose-900/40 text-rose-600 dark:text-rose-400 mb-3">
        <AlertCircle className="w-6 h-6" />
      </div>
      <h4 className="text-base font-bold text-rose-900 dark:text-rose-200">
        Unable to load data
      </h4>
      <p className="mt-1 text-sm text-rose-700 dark:text-rose-300">
        {message || 'An error occurred while communicating with the backend.'}
      </p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="mt-4 inline-flex items-center px-4 py-2 text-xs font-semibold rounded-xl bg-rose-600 hover:bg-rose-700 text-white transition-colors shadow-sm"
        >
          <RefreshCw className="w-3.5 h-3.5 mr-1.5" />
          Retry Request
        </button>
      )}
    </div>
  );
}

export const ErrorAlert = ErrorState;

