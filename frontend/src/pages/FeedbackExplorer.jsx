import React, { useState, useEffect } from 'react';
import { Search, Filter, RotateCcw, Download } from 'lucide-react';
import { getFeedback } from '../services/api';
import FeedbackTable from '../components/FeedbackTable';
import FeedbackDetailModal from '../components/FeedbackDetailModal';
import { ErrorState } from '../components/LoadingState';

const SENTIMENT_OPTIONS = ['Positive', 'Negative', 'Neutral'];
const CATEGORY_OPTIONS = [
  'Product Issue',
  'Delivery Issue',
  'Payment Issue',
  'Technical Issue',
  'Service Issue',
  'General Feedback',
];

export default function FeedbackExplorer() {
  const [feedbackList, setFeedbackList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Filters state
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedSentiment, setSelectedSentiment] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');

  // Pagination state
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalRecords, setTotalRecords] = useState(0);
  const limit = 15;

  // Selected record for modal
  const [selectedRecord, setSelectedRecord] = useState(null);

  const fetchFeedback = async () => {
    try {
      setLoading(true);
      setError(null);
      const params = {
        page: currentPage,
        limit,
      };

      if (searchTerm.trim()) params.search = searchTerm.trim();
      if (selectedSentiment) params.sentiment = selectedSentiment;
      if (selectedCategory) params.issue_category = selectedCategory;
      if (startDate) params.start_date = startDate;
      if (endDate) params.end_date = endDate;

      const res = await getFeedback(params);
      setFeedbackList(res.data || []);
      setTotalRecords(res.total || 0);
      setTotalPages(Math.ceil((res.total || 0) / limit));
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFeedback();
  }, [currentPage, selectedSentiment, selectedCategory, startDate, endDate]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    setCurrentPage(1);
    fetchFeedback();
  };

  const handleResetFilters = () => {
    setSearchTerm('');
    setSelectedSentiment('');
    setSelectedCategory('');
    setStartDate('');
    setEndDate('');
    setCurrentPage(1);
  };

  const handleExportCSV = () => {
    if (feedbackList.length === 0) return;
    const headers = ['ID,Feedback,Sentiment,Issue Category,Date'];
    const rows = feedbackList.map(
      (item) =>
        `"${item.feedback_id}","${item.feedback_text.replace(/"/g, '""')}","${item.sentiment}","${item.issue_category}","${item.feedback_date}"`
    );
    const csvContent = [headers, ...rows].join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.setAttribute('href', url);
    link.setAttribute('download', `feedback_export_page_${currentPage}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h2 className="text-2xl font-black tracking-tight text-slate-900 dark:text-white">
            Customer Feedback Explorer
          </h2>
          <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
            Search, filter, inspect, and export feedback records with server-side pagination.
          </p>
        </div>

        <button
          onClick={handleExportCSV}
          disabled={feedbackList.length === 0}
          className="inline-flex items-center px-4 py-2 text-xs font-semibold rounded-xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors shadow-sm self-start"
        >
          <Download className="w-3.5 h-3.5 mr-1.5" />
          Export Page CSV
        </button>
      </div>

      {/* Filter and Search Bar */}
      <div className="p-4 sm:p-5 bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
        <form onSubmit={handleSearchSubmit} className="flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search feedback text or ID (e.g. 'refund', 'FB-00042')..."
              className="w-full pl-10 pr-4 py-2 text-xs sm:text-sm rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/60 text-slate-900 dark:text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all"
            />
          </div>
          <button
            type="submit"
            className="px-5 py-2 text-xs sm:text-sm font-semibold rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white transition-colors shadow-sm"
          >
            Search
          </button>
        </form>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3 pt-3 border-t border-slate-100 dark:border-slate-800">
          <div>
            <label className="block text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-1">
              Sentiment
            </label>
            <select
              value={selectedSentiment}
              onChange={(e) => {
                setSelectedSentiment(e.target.value);
                setCurrentPage(1);
              }}
              className="w-full p-2 text-xs rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/60 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
            >
              <option value="">All Sentiments</option>
              {SENTIMENT_OPTIONS.map((s) => (
                <option key={s} value={s}>{s}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-1">
              Issue Category
            </label>
            <select
              value={selectedCategory}
              onChange={(e) => {
                setSelectedCategory(e.target.value);
                setCurrentPage(1);
              }}
              className="w-full p-2 text-xs rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/60 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
            >
              <option value="">All Categories</option>
              {CATEGORY_OPTIONS.map((c) => (
                <option key={c} value={c}>{c}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-1">
              Start Date
            </label>
            <input
              type="date"
              value={startDate}
              onChange={(e) => {
                setStartDate(e.target.value);
                setCurrentPage(1);
              }}
              className="w-full p-2 text-xs rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/60 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>

          <div>
            <label className="block text-[11px] font-bold uppercase tracking-wider text-slate-400 mb-1">
              End Date
            </label>
            <input
              type="date"
              value={endDate}
              onChange={(e) => {
                setEndDate(e.target.value);
                setCurrentPage(1);
              }}
              className="w-full p-2 text-xs rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/60 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
        </div>

        {(searchTerm || selectedSentiment || selectedCategory || startDate || endDate) && (
          <div className="flex justify-end">
            <button
              onClick={handleResetFilters}
              className="inline-flex items-center text-xs font-semibold text-slate-500 hover:text-indigo-600 dark:hover:text-indigo-400"
            >
              <RotateCcw className="w-3.5 h-3.5 mr-1" />
              Reset All Filters
            </button>
          </div>
        )}
      </div>

      {/* Main Table */}
      {error ? (
        <ErrorState message={error} onRetry={fetchFeedback} />
      ) : (
        <FeedbackTable
          feedbackList={feedbackList}
          loading={loading}
          currentPage={currentPage}
          totalPages={totalPages}
          totalRecords={totalRecords}
          onPageChange={(page) => setCurrentPage(page)}
          onSelectRecord={(rec) => setSelectedRecord(rec)}
        />
      )}

      {/* Detail Modal */}
      {selectedRecord && (
        <FeedbackDetailModal
          record={selectedRecord}
          onClose={() => setSelectedRecord(null)}
        />
      )}
    </div>
  );
}
