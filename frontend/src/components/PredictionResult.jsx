import React from 'react';
import { AlertCircle, CheckCircle2, AlertTriangle, ShieldAlert, ArrowRight } from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell
} from 'recharts';

export default function PredictionResult({ result }) {
  if (!result) return null;

  const attentionConfig = {
    High: {
      badge: 'bg-rose-100 dark:bg-rose-950/60 text-rose-700 dark:text-rose-300 border-rose-300 dark:border-rose-800',
      icon: AlertCircle,
      indicator: 'bg-rose-500',
      title: 'High Attention Required',
    },
    Medium: {
      badge: 'bg-amber-100 dark:bg-amber-950/60 text-amber-700 dark:text-amber-300 border-amber-300 dark:border-amber-800',
      icon: AlertTriangle,
      indicator: 'bg-amber-500',
      title: 'Medium Attention Required',
    },
    Low: {
      badge: 'bg-emerald-100 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 border-emerald-300 dark:border-emerald-800',
      icon: CheckCircle2,
      indicator: 'bg-emerald-500',
      title: 'Low Attention Required',
    },
  };

  const att = attentionConfig[result.attention_level] || attentionConfig.Medium;
  const AttIcon = att.icon;

  // Prepare probability data for charts
  const sentimentProbData = Object.entries(result.sentiment_probabilities || {}).map(
    ([name, val]) => ({ name, value: Math.round(val * 100) })
  );

  const issueProbData = Object.entries(result.issue_probabilities || {})
    .map(([name, val]) => ({ name, value: Math.round(val * 100) }))
    .sort((a, b) => b.value - a.value);

  const getSentimentBarColor = (name) => {
    if (name === 'Positive') return '#22c55e';
    if (name === 'Negative') return '#ef4444';
    return '#0ea5e9';
  };

  return (
    <div className="mt-8 space-y-6 animate-fade-in">
      {/* Primary Classification Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Sentiment Card */}
        <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm border-t-4 border-t-indigo-500">
          <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
            PREDICTED SENTIMENT
          </span>
          <div className="mt-2 flex items-baseline justify-between">
            <h4
              className={`text-2xl font-black ${
                result.sentiment === 'Positive'
                  ? 'text-emerald-600 dark:text-emerald-400'
                  : result.sentiment === 'Negative'
                  ? 'text-rose-600 dark:text-rose-400'
                  : 'text-sky-600 dark:text-sky-400'
              }`}
            >
              {result.sentiment}
            </h4>
            <span className="text-sm font-bold text-slate-700 dark:text-slate-300">
              {(result.sentiment_confidence * 100).toFixed(1)}%
            </span>
          </div>
          <div className="mt-2 w-full bg-slate-100 dark:bg-slate-800 h-2 rounded-full overflow-hidden">
            <div
              className={`h-full rounded-full ${
                result.sentiment === 'Positive'
                  ? 'bg-emerald-500'
                  : result.sentiment === 'Negative'
                  ? 'bg-rose-500'
                  : 'bg-sky-500'
              }`}
              style={{ width: `${Math.min(100, result.sentiment_confidence * 100)}%` }}
            />
          </div>
        </div>

        {/* Issue Category Card */}
        <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm border-t-4 border-t-purple-500">
          <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
            ISSUE CATEGORY
          </span>
          <div className="mt-2 flex items-baseline justify-between">
            <h4 className="text-2xl font-black text-purple-600 dark:text-purple-400 truncate">
              {result.issue_category}
            </h4>
            <span className="text-sm font-bold text-slate-700 dark:text-slate-300">
              {(result.issue_confidence * 100).toFixed(1)}%
            </span>
          </div>
          <div className="mt-2 w-full bg-slate-100 dark:bg-slate-800 h-2 rounded-full overflow-hidden">
            <div
              className="h-full bg-purple-500 rounded-full"
              style={{ width: `${Math.min(100, result.issue_confidence * 100)}%` }}
            />
          </div>
        </div>

        {/* Attention Level Card */}
        <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm border-t-4 border-t-amber-500">
          <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
            RECOMMENDED ATTENTION
          </span>
          <div className="mt-2 flex items-center justify-between">
            <span
              className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-black uppercase tracking-wider border ${att.badge}`}
            >
              <AttIcon className="w-3.5 h-3.5 mr-1.5" />
              {result.attention_level}
            </span>
            <span className="text-xs text-slate-400 font-medium">Business Rule</span>
          </div>
          <p className="mt-2.5 text-xs text-slate-600 dark:text-slate-300 line-clamp-2">
            {result.recommended_action}
          </p>
        </div>
      </div>

      {/* Explanation & Action Panel */}
      <div className="p-5 rounded-2xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800">
        <h5 className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-2 flex items-center">
          <ArrowRight className="w-3.5 h-3.5 mr-1.5 text-indigo-500" />
          Why this classification?
        </h5>
        <p className="text-sm text-slate-700 dark:text-slate-300 leading-relaxed">
          {result.explanation}
        </p>
      </div>

      {/* Calibrated Probability Breakdown Charts */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Sentiment Probabilities */}
        <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
          <h5 className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-4">
            Sentiment Class Probabilities (%)
          </h5>
          <div className="h-44 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={sentimentProbData} layout="vertical" margin={{ left: 20, right: 30, top: 5, bottom: 5 }}>
                <XAxis type="number" domain={[0, 100]} tick={{ fontSize: 11 }} />
                <YAxis dataKey="name" type="category" tick={{ fontSize: 11 }} width={70} />
                <Tooltip formatter={(value) => [`${value}%`, 'Probability']} />
                <Bar dataKey="value" radius={[0, 6, 6, 0]}>
                  {sentimentProbData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={getSentimentBarColor(entry.name)} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Issue Category Probabilities */}
        <div className="p-5 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-sm">
          <h5 className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-4">
            Issue Category Probabilities (%)
          </h5>
          <div className="h-44 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={issueProbData} layout="vertical" margin={{ left: 30, right: 30, top: 5, bottom: 5 }}>
                <XAxis type="number" domain={[0, 100]} tick={{ fontSize: 11 }} />
                <YAxis dataKey="name" type="category" tick={{ fontSize: 10 }} width={100} />
                <Tooltip formatter={(value) => [`${value}%`, 'Probability']} />
                <Bar dataKey="value" fill="#8b5cf6" radius={[0, 6, 6, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
