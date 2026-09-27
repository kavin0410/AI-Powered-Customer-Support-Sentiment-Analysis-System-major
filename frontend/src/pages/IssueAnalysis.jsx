import React, { useState, useEffect } from 'react';
import { Tag, AlertTriangle, TrendingUp, BarChart2 } from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
} from 'recharts';
import { getIssueAnalytics } from '../services/api';
import MetricCard from '../components/MetricCard';
import ChartCard from '../components/ChartCard';
import { LoadingSpinner, ErrorState } from '../components/LoadingState';

const CATEGORY_COLORS = ['#3b82f6', '#f59e0b', '#ec4899', '#8b5cf6', '#14b8a6', '#64748b'];

export default function IssueAnalysis({ isDarkMode }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await getIssueAnalytics();
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

  if (loading) return <LoadingSpinner message="Evaluating issue category dynamics..." />;
  if (error) return <ErrorState message={error} onRetry={fetchData} />;
  if (!data) return null;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-black tracking-tight text-slate-900 dark:text-white">
          Customer Support Issue Category Analysis
        </h2>
        <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
          Taxonomy breakdown across all six operational domains: Product, Delivery, Payment, Technical, Service, and General Feedback.
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <MetricCard
          title="Most Reported Issue Domain"
          value={data.most_reported_issue}
          subtext="Highest absolute ticket volume driver"
          icon={Tag}
          accent="indigo"
        />
        <MetricCard
          title="Highest Negative Ticket Volume"
          value={data.highest_negative_issue}
          subtext="Category with the most customer complaints"
          icon={AlertTriangle}
          accent="rose"
        />
      </div>

      {/* Charts Row 1: Issue Frequency & Proportional Share */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ChartCard
          title="Issue Frequency Ranking"
          subtitle="Total feedback records categorized by operational issue type"
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
                <Tooltip formatter={(val, name, props) => [`${val} tickets (${props.payload.percentage}%)`, 'Volume']} />
                <Bar dataKey="count" radius={[6, 6, 0, 0]}>
                  {data.issue_distribution.map((entry, index) => (
                    <Cell key={`cell-${entry.name}`} fill={CATEGORY_COLORS[index % CATEGORY_COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>

        {/* Issue Percentage Donut Chart */}
        <ChartCard
          title="Issue Category Share (%)"
          subtitle="Proportional percentage distribution of customer concerns"
        >
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={data.issue_percentages}
                  dataKey="count"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  innerRadius={65}
                  outerRadius={100}
                  paddingAngle={3}
                  label={({ name, percentage }) => `${name}: ${percentage}%`}
                >
                  {data.issue_percentages.map((entry, index) => (
                    <Cell key={`cell-${entry.name}`} fill={CATEGORY_COLORS[index % CATEGORY_COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={(val, name, props) => [`${val} (${props.payload.percentage}%)`, name]} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>
      </div>

      {/* Category Granular Statistics Table */}
      <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden p-5">
        <h4 className="text-sm sm:text-base font-bold text-slate-900 dark:text-white mb-4">
          Detailed Category Performance Breakdown
        </h4>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-600 dark:text-slate-300">
            <thead className="bg-slate-50 dark:bg-slate-800/60 text-xs uppercase font-semibold text-slate-500 dark:text-slate-400 border-b border-slate-200 dark:border-slate-800 tracking-wider">
              <tr>
                <th className="px-4 py-3">Category</th>
                <th className="px-4 py-3 text-right">Total Tickets</th>
                <th className="px-4 py-3 text-right">Category Share</th>
                <th className="px-4 py-3 text-right">Negative Rate</th>
                <th className="px-4 py-3 text-right">Positive Rate</th>
                <th className="px-4 py-3 text-center">Triage Urgency</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800/80">
              {data.category_statistics?.map((stat) => (
                <tr key={stat.category} className="hover:bg-slate-50/70 dark:hover:bg-slate-800/40">
                  <td className="px-4 py-3.5 font-bold text-slate-900 dark:text-white">
                    {stat.category}
                  </td>
                  <td className="px-4 py-3.5 text-right font-mono">
                    {stat.total_tickets.toLocaleString()}
                  </td>
                  <td className="px-4 py-3.5 text-right font-mono text-slate-500">
                    {stat.percentage}%
                  </td>
                  <td className="px-4 py-3.5 text-right font-bold text-rose-600 dark:text-rose-400 font-mono">
                    {stat.negative_rate}%
                  </td>
                  <td className="px-4 py-3.5 text-right font-bold text-emerald-600 dark:text-emerald-400 font-mono">
                    {stat.positive_rate}%
                  </td>
                  <td className="px-4 py-3.5 text-center">
                    <span
                      className={`inline-block px-2.5 py-0.5 rounded-full text-xs font-semibold ${
                        stat.negative_rate >= 50
                          ? 'bg-rose-100 dark:bg-rose-950/60 text-rose-700 dark:text-rose-300'
                          : 'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300'
                      }`}
                    >
                      {stat.negative_rate >= 50 ? 'High' : 'Normal'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
