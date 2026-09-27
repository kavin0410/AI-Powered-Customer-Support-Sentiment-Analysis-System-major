import React, { useState, useEffect } from 'react';
import { Smile, Frown, Meh, Award, AlertOctagon } from 'lucide-react';
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  AreaChart,
  Area,
} from 'recharts';
import { getSentimentAnalytics } from '../services/api';
import MetricCard from '../components/MetricCard';
import ChartCard from '../components/ChartCard';
import { LoadingSpinner, ErrorState } from '../components/LoadingState';

const SENTIMENT_COLORS = {
  Positive: '#22c55e',
  Negative: '#ef4444',
  Neutral: '#0ea5e9',
};

export default function SentimentAnalysis({ isDarkMode }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await getSentimentAnalytics();
      setData(res);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (loading) return <LoadingSpinner message="Aggregating sentiment statistics..." />;
  if (error) return <ErrorState message={error} onRetry={fetchData} />;
  if (!data) return null;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-black tracking-tight text-slate-900 dark:text-white">
          Sentiment Analytics Deep-Dive
        </h2>
        <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
          Detailed metrics, satisfaction indicators, and category correlation diagnostics.
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <MetricCard
          title="Positive Sentiment Rate"
          value={`${data.positive_percentage}%`}
          subtext="Satisfied customer interactions"
          icon={Smile}
          accent="emerald"
        />
        <MetricCard
          title="Negative Sentiment Rate"
          value={`${data.negative_percentage}%`}
          subtext="Dissatisfied tickets requiring attention"
          icon={Frown}
          accent="rose"
        />
        <MetricCard
          title="Neutral Sentiment Rate"
          value={`${data.neutral_percentage}%`}
          subtext="Inquiries, queries & balanced reviews"
          icon={Meh}
          accent="sky"
        />
      </div>

      {/* Extrema Callout Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="p-5 rounded-2xl bg-rose-50/70 dark:bg-rose-950/20 border border-rose-200 dark:border-rose-900/60 flex items-start space-x-3.5">
          <div className="p-2.5 rounded-xl bg-rose-100 dark:bg-rose-900/50 text-rose-600 dark:text-rose-400 shrink-0">
            <AlertOctagon className="w-5 h-5" />
          </div>
          <div>
            <span className="text-[11px] font-bold uppercase tracking-wider text-rose-600 dark:text-rose-400">
              Highest Dissatisfaction Hotspot
            </span>
            <h4 className="text-base font-extrabold text-slate-900 dark:text-white mt-0.5">
              {data.highest_negative_category?.category || 'N/A'}
            </h4>
            <p className="text-xs text-slate-600 dark:text-slate-300 mt-1 leading-relaxed">
              Exhibits a <strong className="text-rose-600 dark:text-rose-400">{data.highest_negative_category?.negative_pct}%</strong> negative sentiment rate ({data.highest_negative_category?.negative} complaints out of {data.highest_negative_category?.total} tickets).
            </p>
          </div>
        </div>

        <div className="p-5 rounded-2xl bg-emerald-50/70 dark:bg-emerald-950/20 border border-emerald-200 dark:border-emerald-900/60 flex items-start space-x-3.5">
          <div className="p-2.5 rounded-xl bg-emerald-100 dark:bg-emerald-900/50 text-emerald-600 dark:text-emerald-400 shrink-0">
            <Award className="w-5 h-5" />
          </div>
          <div>
            <span className="text-[11px] font-bold uppercase tracking-wider text-emerald-600 dark:text-emerald-400">
              Highest Customer Praise
            </span>
            <h4 className="text-base font-extrabold text-slate-900 dark:text-white mt-0.5">
              {data.highest_positive_category?.category || 'N/A'}
            </h4>
            <p className="text-xs text-slate-600 dark:text-slate-300 mt-1 leading-relaxed">
              Leads satisfaction with a <strong className="text-emerald-600 dark:text-emerald-400">{data.highest_positive_category?.positive_pct}%</strong> positive rate ({data.highest_positive_category?.positive} positive reviews).
            </p>
          </div>
        </div>
      </div>

      {/* Charts Row 1: Sentiment Donut & Temporal Sentiment Inflow */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ChartCard
          title="Overall Sentiment Distribution"
          subtitle="Proportionate breakdown of analyzed customer feedback"
        >
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={data.sentiment_distribution}
                  dataKey="count"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  innerRadius={65}
                  outerRadius={100}
                  paddingAngle={4}
                  label={({ name, percentage }) => `${name}: ${percentage}%`}
                >
                  {data.sentiment_distribution.map((entry) => (
                    <Cell key={`cell-${entry.name}`} fill={SENTIMENT_COLORS[entry.name] || '#94a3b8'} />
                  ))}
                </Pie>
                <Tooltip formatter={(val, name, props) => [`${val} (${props.payload.percentage}%)`, name]} />
                <Legend verticalAlign="bottom" height={36} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>

        {/* Monthly Sentiment Trend Area Chart */}
        <ChartCard
          title="Monthly Sentiment Trajectory"
          subtitle="Tracking satisfaction shifts over time"
        >
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={data.monthly_sentiment_trend} margin={{ top: 10, right: 20, left: 0, bottom: 5 }}>
                <XAxis dataKey="month" tick={{ fontSize: 11, fill: isDarkMode ? '#94a3b8' : '#64748b' }} />
                <YAxis tick={{ fontSize: 11, fill: isDarkMode ? '#94a3b8' : '#64748b' }} />
                <Tooltip />
                <Legend />
                <Area type="monotone" dataKey="positive" name="Positive" stackId="1" stroke="#22c55e" fill="#22c55e" fillOpacity={0.4} />
                <Area type="monotone" dataKey="neutral" name="Neutral" stackId="1" stroke="#0ea5e9" fill="#0ea5e9" fillOpacity={0.4} />
                <Area type="monotone" dataKey="negative" name="Negative" stackId="1" stroke="#ef4444" fill="#ef4444" fillOpacity={0.4} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>
      </div>

      {/* Charts Row 2: Sentiment by Category Stacked */}
      <ChartCard
        title="Sentiment Proportions by Operational Category"
        subtitle="Comparing positive vs negative concentration within each issue domain"
      >
        <div className="h-80 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={data.sentiment_by_issue}
              layout="vertical"
              margin={{ top: 10, right: 30, left: 40, bottom: 5 }}
            >
              <XAxis type="number" tick={{ fontSize: 11, fill: isDarkMode ? '#94a3b8' : '#64748b' }} />
              <YAxis dataKey="category" type="category" tick={{ fontSize: 11, fill: isDarkMode ? '#94a3b8' : '#64748b' }} width={120} />
              <Tooltip />
              <Legend />
              <Bar dataKey="positive" name="Positive" stackId="a" fill="#22c55e" />
              <Bar dataKey="neutral" name="Neutral" stackId="a" fill="#0ea5e9" />
              <Bar dataKey="negative" name="Negative" stackId="a" fill="#ef4444" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </ChartCard>
    </div>
  );
}
