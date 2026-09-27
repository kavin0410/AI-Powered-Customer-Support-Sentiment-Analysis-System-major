import React, { useState, useEffect } from 'react';
import {
  MessageSquare,
  Smile,
  Frown,
  Meh,
  Tag,
  TrendingUp,
  RefreshCw,
} from 'lucide-react';
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
  LineChart,
  Line,
} from 'recharts';
import { getDashboard } from '../services/api';
import MetricCard from '../components/MetricCard';
import ChartCard from '../components/ChartCard';
import { LoadingSpinner, ErrorState } from '../components/LoadingState';

const SENTIMENT_COLORS = {
  Positive: '#22c55e',
  Negative: '#ef4444',
  Neutral: '#0ea5e9',
};

const ISSUE_COLORS = ['#3b82f6', '#f59e0b', '#ec4899', '#8b5cf6', '#14b8a6', '#64748b'];

export default function Dashboard({ isDarkMode }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await getDashboard();
      setData(res);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  if (loading) return <LoadingSpinner message="Calculating real-time analytics from dataset..." />;
  if (error) return <ErrorState message={error} onRetry={fetchDashboardData} />;
  if (!data) return null;

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pb-2">
        <div>
          <h2 className="text-2xl font-black tracking-tight text-slate-900 dark:text-white">
            Executive Analytics Dashboard
          </h2>
          <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
            Real-time operational intelligence on customer sentiment and support issue patterns.
          </p>
        </div>

        <button
          onClick={fetchDashboardData}
          className="inline-flex items-center px-3.5 py-2 text-xs font-semibold rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors shadow-sm self-start"
        >
          <RefreshCw className="w-3.5 h-3.5 mr-1.5" />
          Refresh Metrics
        </button>
      </div>

      {/* KPI Cards Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        <MetricCard
          title="Total Feedback"
          value={data.total_feedback.toLocaleString()}
          subtext="100% analyzed records"
          icon={MessageSquare}
          accent="indigo"
        />
        <MetricCard
          title="Positive Sentiment"
          value={data.positive_feedback.toLocaleString()}
          subtext={`${data.positive_percentage}% of total`}
          icon={Smile}
          accent="emerald"
        />
        <MetricCard
          title="Negative Sentiment"
          value={data.negative_feedback.toLocaleString()}
          subtext={`${data.negative_percentage}% of total`}
          icon={Frown}
          accent="rose"
        />
        <MetricCard
          title="Neutral Sentiment"
          value={data.neutral_feedback.toLocaleString()}
          subtext={`${data.neutral_percentage}% of total`}
          icon={Meh}
          accent="sky"
        />
        <MetricCard
          title="Top Issue Category"
          value={data.most_common_issue}
          subtext={`${data.most_common_issue_count.toLocaleString()} tickets logged`}
          icon={Tag}
          accent="purple"
        />
      </div>

      {/* Charts Row 1: Sentiment Distribution & Issue Distribution */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Sentiment Distribution Pie */}
        <ChartCard
          title="Sentiment Distribution"
          subtitle="Proportional mix of Positive, Negative, and Neutral feedback"
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
                <Tooltip
                  formatter={(val, name, props) => [`${val} records (${props.payload.percentage}%)`, name]}
                />
                <Legend verticalAlign="bottom" height={36} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>

        {/* Issue Category Distribution Bar */}
        <ChartCard
          title="Issue Category Distribution"
          subtitle="Breakdown of customer tickets by operational domain"
        >
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data.issue_distribution} margin={{ top: 10, right: 20, left: 0, bottom: 25 }}>
                <XAxis
                  dataKey="name"
                  interval={0}
                  tick={{ fontSize: 10, fill: isDarkMode ? '#94a3b8' : '#64748b' }}
                  angle={-20}
                  textAnchor="end"
                />
                <YAxis tick={{ fontSize: 11, fill: isDarkMode ? '#94a3b8' : '#64748b' }} />
                <Tooltip
                  formatter={(val, name, props) => [`${val} (${props.payload.percentage}%)`, 'Volume']}
                />
                <Bar dataKey="count" radius={[6, 6, 0, 0]}>
                  {data.issue_distribution.map((entry, index) => (
                    <Cell key={`cell-${entry.name}`} fill={ISSUE_COLORS[index % ISSUE_COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>
      </div>

      {/* Charts Row 2: Monthly Trends & Trajectory */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Monthly Volume Trend */}
        <ChartCard
          title="Monthly Feedback Volume"
          subtitle="Tracking feedback inflow across consecutive months"
        >
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data.monthly_feedback} margin={{ top: 10, right: 20, left: 0, bottom: 5 }}>
                <XAxis dataKey="month" tick={{ fontSize: 11, fill: isDarkMode ? '#94a3b8' : '#64748b' }} />
                <YAxis tick={{ fontSize: 11, fill: isDarkMode ? '#94a3b8' : '#64748b' }} />
                <Tooltip />
                <Legend />
                <Bar dataKey="positive" name="Positive" stackId="a" fill="#22c55e" />
                <Bar dataKey="neutral" name="Neutral" stackId="a" fill="#0ea5e9" />
                <Bar dataKey="negative" name="Negative" stackId="a" fill="#ef4444" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>

        {/* Sentiment Trajectory Line Chart */}
        <ChartCard
          title="Sentiment Trends Over Time"
          subtitle="Longitudinal trajectories for each sentiment class"
        >
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={data.sentiment_trend} margin={{ top: 10, right: 20, left: 0, bottom: 5 }}>
                <XAxis dataKey="month" tick={{ fontSize: 11, fill: isDarkMode ? '#94a3b8' : '#64748b' }} />
                <YAxis tick={{ fontSize: 11, fill: isDarkMode ? '#94a3b8' : '#64748b' }} />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="positive" name="Positive" stroke="#22c55e" strokeWidth={2.5} dot={{ r: 3 }} />
                <Line type="monotone" dataKey="negative" name="Negative" stroke="#ef4444" strokeWidth={2.5} dot={{ r: 3 }} />
                <Line type="monotone" dataKey="neutral" name="Neutral" stroke="#0ea5e9" strokeWidth={2.5} dot={{ r: 3 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>
      </div>

      {/* Charts Row 3: Sentiment vs Issue Heatmap / Stacked Bar */}
      <ChartCard
        title="Sentiment Breakdown by Issue Category"
        subtitle="Analyzing customer satisfaction and dissatisfaction rates across categories"
      >
        <div className="h-80 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={data.sentiment_issue_matrix}
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
