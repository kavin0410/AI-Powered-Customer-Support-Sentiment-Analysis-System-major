import React, { useState } from 'react';
import { Wand2, Sparkles, Send, RotateCcw, AlertCircle } from 'lucide-react';
import { predictFeedback } from '../services/api';
import PredictionResult from '../components/PredictionResult';

const SAMPLE_FEEDBACK = [
  "The product quality is excellent and I am very happy with my purchase.",
  "My order arrived three days late and the package was damaged.",
  "Money was deducted from my account but the payment failed.",
  "The mobile application crashes whenever I try to open it.",
  "The customer service representative was very helpful.",
  "I received the wrong product.",
  "The delivery was completed on time.",
  "I would like to know more about your product."
];

export default function Prediction() {
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handlePredict = async (textToPredict) => {
    const targetText = typeof textToPredict === 'string' ? textToPredict : inputText;
    
    if (!targetText || !targetText.trim()) {
      setError("Please enter customer feedback before running prediction.");
      return;
    }

    if (targetText.trim().length < 3) {
      setError("Feedback text is too brief. Please enter at least a few words.");
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const res = await predictFeedback(targetText.trim());
      setResult(res);
    } catch (err) {
      setError(err.message || "Unable to analyze the feedback. Please check that the backend is running.");
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  const handleSampleClick = (sample) => {
    setInputText(sample);
    handlePredict(sample);
  };

  const handleClear = () => {
    setInputText('');
    setResult(null);
    setError(null);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Page Header */}
      <div>
        <h2 className="text-2xl font-black tracking-tight text-slate-900 dark:text-white flex items-center">
          <Wand2 className="w-6 h-6 mr-2.5 text-indigo-600 dark:text-indigo-400" />
          Real-Time Customer Feedback Predictor
        </h2>
        <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
          Perform dual-task classification for Sentiment & Issue Categories using calibrated Phase 1 ML models.
        </p>
      </div>

      {/* Main Input Card */}
      <div className="p-6 bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm transition-colors">
        <label className="block text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-2">
          Customer Feedback Input
        </label>
        
        <textarea
          rows={4}
          value={inputText}
          onChange={(e) => {
            setInputText(e.target.value);
            if (error) setError(null);
          }}
          placeholder="Enter customer feedback here... (e.g., 'My payment went through but order says failed and money was deducted.')"
          className="w-full p-4 text-sm rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/60 text-slate-900 dark:text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all resize-y"
        />

        {/* Error message */}
        {error && (
          <div className="mt-3 p-3 rounded-xl bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-900/60 flex items-center text-xs font-medium text-rose-700 dark:text-rose-300">
            <AlertCircle className="w-4 h-4 mr-2 shrink-0 text-rose-500" />
            <span>{error}</span>
          </div>
        )}

        {/* Action Buttons */}
        <div className="mt-4 flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center space-x-2">
            <button
              onClick={() => handlePredict()}
              disabled={loading}
              className="inline-flex items-center px-5 py-2.5 text-sm font-semibold rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-md shadow-indigo-500/20"
            >
              {loading ? (
                <>
                  <div className="w-4 h-4 mr-2 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Analyzing Model...
                </>
              ) : (
                <>
                  <Send className="w-4 h-4 mr-2" />
                  Analyze Feedback
                </>
              )}
            </button>

            <button
              onClick={handleClear}
              className="inline-flex items-center px-4 py-2.5 text-sm font-medium rounded-xl text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
            >
              <RotateCcw className="w-4 h-4 mr-1.5" />
              Clear
            </button>
          </div>

          <span className="text-xs text-slate-400 font-mono">
            {inputText.length}/3000 chars
          </span>
        </div>

        {/* Quick Test Samples */}
        <div className="mt-6 pt-5 border-t border-slate-100 dark:border-slate-800">
          <span className="text-xs font-semibold text-slate-500 dark:text-slate-400 flex items-center mb-2.5">
            <Sparkles className="w-3.5 h-3.5 mr-1.5 text-amber-500" />
            Quick Test Scenarios (Click to test):
          </span>
          <div className="flex flex-wrap gap-2">
            {SAMPLE_FEEDBACK.map((sample, i) => (
              <button
                key={i}
                onClick={() => handleSampleClick(sample)}
                className="text-xs text-left px-3 py-1.5 rounded-lg bg-slate-100 dark:bg-slate-800/80 text-slate-700 dark:text-slate-300 hover:bg-indigo-50 dark:hover:bg-indigo-950/40 hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors border border-slate-200/60 dark:border-slate-700/60 truncate max-w-xs"
                title={sample}
              >
                {sample}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Prediction Output */}
      {result && <PredictionResult result={result} />}
    </div>
  );
}
