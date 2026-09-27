import React from 'react';
import { Eye, ChevronLeft, ChevronRight } from 'lucide-react';

export default function FeedbackTable({
  feedbackList,
  loading,
  currentPage,
  totalPages,
  totalRecords,
  onPageChange,
  onSelectRecord,
}) {
  const sentimentBadges = {
    Positive: 'bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-400 border-emerald-200 dark:border-emerald-800',
    Negative: 'bg-rose-50 dark:bg-rose-950/40 text-rose-700 dark:text-rose-400 border-rose-200 dark:border-rose-800',
    Neutral: 'bg-sky-50 dark:bg-sky-950/40 text-sky-700 dark:text-sky-400 border-sky-200 dark:border-sky-800',
  };

  const categoryBadges = {
    'Product Issue': 'bg-amber-50 dark:bg-amber-950/30 text-amber-700 dark:text-amber-400 border-amber-200 dark:border-amber-800',
    'Delivery Issue': 'bg-blue-50 dark:bg-blue-950/30 text-blue-700 dark:text-blue-400 border-blue-200 dark:border-blue-800',
    'Payment Issue': 'bg-fuchsia-50 dark:bg-fuchsia-950/30 text-fuchsia-700 dark:text-fuchsia-400 border-fuchsia-200 dark:border-fuchsia-800',
    'Technical Issue': 'bg-purple-50 dark:bg-purple-950/30 text-purple-700 dark:text-purple-400 border-purple-200 dark:border-purple-800',
    'Service Issue': 'bg-teal-50 dark:bg-teal-950/30 text-teal-700 dark:text-teal-400 border-teal-200 dark:border-teal-800',
    'General Feedback': 'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-200 dark:border-slate-700',
  };

  return (
    <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm text-slate-600 dark:text-slate-300">
          <thead className="bg-slate-50 dark:bg-slate-800/60 text-xs uppercase font-semibold text-slate-500 dark:text-slate-400 border-b border-slate-200 dark:border-slate-800 tracking-wider">
            <tr>
              <th scope="col" className="px-5 py-3.5 w-28">ID</th>
              <th scope="col" className="px-5 py-3.5">Customer Feedback</th>
              <th scope="col" className="px-5 py-3.5 w-32">Sentiment</th>
              <th scope="col" className="px-5 py-3.5 w-36">Issue Category</th>
              <th scope="col" className="px-5 py-3.5 w-32">Date</th>
              <th scope="col" className="px-5 py-3.5 w-24 text-center">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 dark:divide-slate-800/80">
            {loading ? (
              [...Array(6)].map((_, i) => (
                <tr key={i} className="animate-pulse">
                  <td className="px-5 py-4"><div className="h-4 bg-slate-200 dark:bg-slate-800 rounded w-16" /></td>
                  <td className="px-5 py-4"><div className="h-4 bg-slate-200 dark:bg-slate-800 rounded w-3/4" /></td>
                  <td className="px-5 py-4"><div className="h-5 bg-slate-200 dark:bg-slate-800 rounded-full w-20" /></td>
                  <td className="px-5 py-4"><div className="h-5 bg-slate-200 dark:bg-slate-800 rounded-full w-24" /></td>
                  <td className="px-5 py-4"><div className="h-4 bg-slate-200 dark:bg-slate-800 rounded w-20" /></td>
                  <td className="px-5 py-4"><div className="h-8 bg-slate-200 dark:bg-slate-800 rounded w-12 mx-auto" /></td>
                </tr>
              ))
            ) : feedbackList.length === 0 ? (
              <tr>
                <td colSpan="6" className="px-5 py-12 text-center text-slate-500 dark:text-slate-400 text-sm">
                  No customer feedback records found matching your filters.
                </td>
              </tr>
            ) : (
              feedbackList.map((item) => (
                <tr
                  key={item.id}
                  className="hover:bg-slate-50/80 dark:hover:bg-slate-800/40 transition-colors"
                >
                  <td className="px-5 py-4 font-mono font-medium text-xs text-indigo-600 dark:text-indigo-400">
                    {item.feedback_id}
                  </td>
                  <td className="px-5 py-4 font-medium text-slate-800 dark:text-slate-200 line-clamp-2 max-w-md">
                    {item.feedback_text}
                  </td>
                  <td className="px-5 py-4">
                    <span
                      className={`inline-block px-2.5 py-0.5 rounded-full text-xs font-semibold border ${
                        sentimentBadges[item.sentiment] || sentimentBadges.Neutral
                      }`}
                    >
                      {item.sentiment}
                    </span>
                  </td>
                  <td className="px-5 py-4">
                    <span
                      className={`inline-block px-2.5 py-0.5 rounded-full text-xs font-medium border ${
                        categoryBadges[item.issue_category] || categoryBadges['General Feedback']
                      }`}
                    >
                      {item.issue_category}
                    </span>
                  </td>
                  <td className="px-5 py-4 text-xs text-slate-500 dark:text-slate-400 whitespace-nowrap">
                    {item.feedback_date}
                  </td>
                  <td className="px-5 py-4 text-center">
                    <button
                      onClick={() => onSelectRecord(item)}
                      className="p-1.5 rounded-lg text-indigo-600 dark:text-indigo-400 hover:bg-indigo-50 dark:hover:bg-indigo-950/50 transition-colors"
                      title="View Record Details"
                    >
                      <Eye className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination Footer */}
      <div className="flex flex-col sm:flex-row items-center justify-between px-5 py-3.5 bg-slate-50 dark:bg-slate-800/60 border-t border-slate-200 dark:border-slate-800 text-xs text-slate-500 dark:text-slate-400 gap-3">
        <div>
          Showing page <span className="font-semibold text-slate-700 dark:text-slate-200">{currentPage}</span> of{' '}
          <span className="font-semibold text-slate-700 dark:text-slate-200">{Math.max(1, totalPages)}</span> ({totalRecords.toLocaleString()} total records)
        </div>

        <div className="flex items-center space-x-1.5">
          <button
            onClick={() => onPageChange(currentPage - 1)}
            disabled={currentPage <= 1 || loading}
            className="flex items-center px-2.5 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-200 disabled:opacity-40 disabled:cursor-not-allowed hover:bg-slate-50 dark:hover:bg-slate-700 transition-colors"
          >
            <ChevronLeft className="w-3.5 h-3.5 mr-1" />
            Previous
          </button>
          <button
            onClick={() => onPageChange(currentPage + 1)}
            disabled={currentPage >= totalPages || loading}
            className="flex items-center px-2.5 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-200 disabled:opacity-40 disabled:cursor-not-allowed hover:bg-slate-50 dark:hover:bg-slate-700 transition-colors"
          >
            Next
            <ChevronRight className="w-3.5 h-3.5 ml-1" />
          </button>
        </div>
      </div>
    </div>
  );
}
