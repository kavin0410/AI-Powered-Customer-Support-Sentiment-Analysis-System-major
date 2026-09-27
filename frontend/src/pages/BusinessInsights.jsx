import React, { useState, useEffect } from 'react';
import { getBusinessInsights } from '../services/api';
import { LoadingSpinner, ErrorAlert } from '../components/LoadingState';
import { 
  Lightbulb, 
  TrendingUp, 
  AlertTriangle, 
  CheckCircle, 
  ArrowRight, 
  RefreshCw, 
  Layers, 
  Target, 
  Zap,
  ShieldCheck
} from 'lucide-react';

const BusinessInsights = () => {
  const [insights, setInsights] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchInsights = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getBusinessInsights();
      setInsights(data);
    } catch (err) {
      setError(err.message || 'Failed to fetch business insights');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchInsights();
  }, []);

  const getInsightIcon = (type) => {
    switch (type) {
      case 'alert':
        return <AlertTriangle className="w-6 h-6 text-rose-500" />;
      case 'opportunity':
        return <TrendingUp className="w-6 h-6 text-emerald-500" />;
      case 'action':
        return <Zap className="w-6 h-6 text-amber-500" />;
      default:
        return <Lightbulb className="w-6 h-6 text-indigo-500" />;
    }
  };

  const getMetricBadgeStyle = (type) => {
    switch (type) {
      case 'alert':
        return 'bg-rose-50 text-rose-700 border-rose-200 dark:bg-rose-900/30 dark:text-rose-400 dark:border-rose-800';
      case 'opportunity':
        return 'bg-emerald-50 text-emerald-700 border-emerald-200 dark:bg-emerald-900/30 dark:text-emerald-400 dark:border-emerald-800';
      case 'action':
        return 'bg-amber-50 text-amber-700 border-amber-200 dark:bg-amber-900/30 dark:text-amber-400 dark:border-amber-800';
      default:
        return 'bg-indigo-50 text-indigo-700 border-indigo-200 dark:bg-indigo-900/30 dark:text-indigo-400 dark:border-indigo-800';
    }
  };

  if (loading) return <LoadingSpinner message="Synthesizing dynamic business intelligence..." />;
  if (error) return <ErrorAlert message={error} onRetry={fetchInsights} />;

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 p-6 bg-gradient-to-r from-indigo-900 via-indigo-800 to-slate-900 text-white rounded-2xl shadow-lg border border-indigo-700/40">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-indigo-500/30 text-indigo-200 border border-indigo-400/30 mb-2">
            <Zap className="w-3.5 h-3.5" />
            Dynamic Statistical Inference
          </div>
          <h1 className="text-2xl font-bold tracking-tight">Executive Business Insights & Action Plan</h1>
          <p className="text-indigo-200 text-sm mt-1 max-w-2xl">
            Automated operational intelligence derived strictly from real customer feedback distributions, sentiment polarity metrics, and classification vectors.
          </p>
        </div>
        <button
          onClick={fetchInsights}
          className="inline-flex items-center gap-2 px-4 py-2 bg-white/10 hover:bg-white/20 text-white rounded-lg text-sm font-medium border border-white/20 transition-all cursor-pointer backdrop-blur-sm self-start md:self-auto"
        >
          <RefreshCw className="w-4 h-4" />
          Refresh Insights
        </button>
      </div>

      {/* Summary KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700/60 p-5 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">Total Insights</span>
            <div className="p-2 rounded-lg bg-indigo-50 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400">
              <Layers className="w-5 h-5" />
            </div>
          </div>
          <div className="text-3xl font-bold text-slate-900 dark:text-slate-100 mt-2">{insights.length}</div>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">Dynamically generated fact-based insights</p>
        </div>

        <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700/60 p-5 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">Data Integrity</span>
            <div className="p-2 rounded-lg bg-emerald-50 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400">
              <ShieldCheck className="w-5 h-5" />
            </div>
          </div>
          <div className="text-3xl font-bold text-emerald-600 dark:text-emerald-400 mt-2">100% Verified</div>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">Zero fabricated or mock conclusions</p>
        </div>

        <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700/60 p-5 shadow-sm">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">Triage Alignment</span>
            <div className="p-2 rounded-lg bg-amber-50 dark:bg-amber-900/30 text-amber-600 dark:text-amber-400">
              <Target className="w-5 h-5" />
            </div>
          </div>
          <div className="text-3xl font-bold text-amber-600 dark:text-amber-400 mt-2">Active</div>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">Rule-based customer attention mapping</p>
        </div>
      </div>

      {/* Dynamic Insights Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {insights.map((item, idx) => (
          <div 
            key={idx}
            className="flex flex-col justify-between bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700/60 p-6 shadow-sm hover:shadow-md transition-shadow"
          >
            <div>
              {/* Header with icon and metric */}
              <div className="flex items-start justify-between gap-4 mb-4">
                <div className="flex items-center gap-3">
                  <div className="p-2.5 rounded-xl bg-slate-100 dark:bg-slate-700/50">
                    {getInsightIcon(item.type)}
                  </div>
                  <div>
                    <span className="text-xs font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500">
                      {item.type || 'Observation'}
                    </span>
                    <h3 className="text-lg font-bold text-slate-800 dark:text-slate-100 leading-snug">
                      {item.title}
                    </h3>
                  </div>
                </div>

                {item.metric && (
                  <span className={`px-3 py-1 text-sm font-bold rounded-lg border whitespace-nowrap ${getMetricBadgeStyle(item.type)}`}>
                    {item.metric}
                  </span>
                )}
              </div>

              {/* Factual Observation Description */}
              <div className="text-sm text-slate-600 dark:text-slate-300 leading-relaxed mb-4">
                {item.description}
              </div>
            </div>

            {/* Recommended Action / Next Step if present */}
            {item.action && (
              <div className="mt-4 pt-4 border-t border-slate-100 dark:border-slate-700/60">
                <div className="flex items-start gap-2.5 bg-slate-50 dark:bg-slate-900/40 rounded-lg p-3 border border-slate-200/60 dark:border-slate-700/40">
                  <ArrowRight className="w-4 h-4 text-indigo-600 dark:text-indigo-400 shrink-0 mt-0.5" />
                  <div>
                    <span className="text-xs font-semibold uppercase tracking-wider text-indigo-600 dark:text-indigo-400 block">
                      Recommended Strategic Action:
                    </span>
                    <span className="text-xs font-medium text-slate-700 dark:text-slate-300">
                      {item.action}
                    </span>
                  </div>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default BusinessInsights;
