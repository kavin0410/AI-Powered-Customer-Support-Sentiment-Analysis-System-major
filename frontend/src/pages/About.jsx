import React from 'react';
import { 
  Cpu, 
  Database, 
  Layers, 
  Activity, 
  ShieldCheck, 
  GitBranch, 
  Code, 
  Server, 
  Layout, 
  CheckCircle2, 
  Users, 
  Target, 
  BrainCircuit,
  BarChart3
} from 'lucide-react';

const About = () => {
  return (
    <div className="space-y-8 max-w-6xl mx-auto">
      {/* Header Banner */}
      <div className="p-8 bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white rounded-2xl shadow-xl border border-indigo-500/20">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-indigo-500/30 text-indigo-300 border border-indigo-400/30 mb-3">
          <BrainCircuit className="w-3.5 h-3.5" />
          University Major Capstone Project - Phase 2
        </div>
        <h1 className="text-3xl font-extrabold tracking-tight">AI-Powered Customer Support & Sentiment Analysis System</h1>
        <p className="text-slate-300 text-base mt-2 max-w-3xl leading-relaxed">
          An enterprise-grade, end-to-end full-stack intelligence platform combining specialized Natural Language Processing 
          models with a high-throughput FastAPI backend, relational SQLite database, and an interactive React analytics dashboard.
        </p>
      </div>

      {/* Problem Statement & Objectives Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700/60 p-6 shadow-sm">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2.5 rounded-lg bg-rose-50 dark:bg-rose-900/30 text-rose-600 dark:text-rose-400">
              <Target className="w-5 h-5" />
            </div>
            <h2 className="text-lg font-bold text-slate-800 dark:text-slate-100">Problem Statement</h2>
          </div>
          <p className="text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
            Modern customer support organizations face overwhelming volumes of unstructured feedback across disparate communication 
            channels. Manual triage leads to delayed response times for critical grievances, inconsistent routing, and lack of real-time 
            visibility into systemic product, delivery, or payment failures.
          </p>
        </div>

        <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700/60 p-6 shadow-sm">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2.5 rounded-lg bg-indigo-50 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400">
              <CheckCircle2 className="w-5 h-5" />
            </div>
            <h2 className="text-lg font-bold text-slate-800 dark:text-slate-100">Core Objectives</h2>
          </div>
          <ul className="text-sm text-slate-600 dark:text-slate-300 space-y-2">
            <li className="flex items-start gap-2">
              <span className="text-indigo-500 font-bold">•</span>
              Automate multi-class sentiment identification (Positive, Negative, Neutral).
            </li>
            <li className="flex items-start gap-2">
              <span className="text-indigo-500 font-bold">•</span>
              Route feedback into 6 discrete operational categories with calibrated probabilities.
            </li>
            <li className="flex items-start gap-2">
              <span className="text-indigo-500 font-bold">•</span>
              Provide automated, rule-based attention level triage (High, Medium, Low).
            </li>
            <li className="flex items-start gap-2">
              <span className="text-indigo-500 font-bold">•</span>
              Enable dynamic analytical exploration and data-driven business decision support.
            </li>
          </ul>
        </div>
      </div>

      {/* Target System Architecture */}
      <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700/60 p-6 shadow-sm">
        <h2 className="text-lg font-bold text-slate-800 dark:text-slate-100 mb-6 flex items-center gap-2">
          <GitBranch className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
          End-to-End System Architecture
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 relative">
          {/* Frontend Card */}
          <div className="p-4 rounded-xl border border-blue-200 bg-blue-50/50 dark:border-blue-900/50 dark:bg-blue-950/20">
            <div className="flex items-center gap-2 mb-2 text-blue-700 dark:text-blue-400 font-semibold text-sm">
              <Layout className="w-4 h-4" />
              1. React Client
            </div>
            <p className="text-xs text-slate-600 dark:text-slate-300">
              Vite, Tailwind CSS, React Router, Recharts, and Axios. Dispatches asynchronous REST requests to backend endpoints.
            </p>
          </div>

          {/* API Gateway Card */}
          <div className="p-4 rounded-xl border border-emerald-200 bg-emerald-50/50 dark:border-emerald-900/50 dark:bg-emerald-950/20">
            <div className="flex items-center gap-2 mb-2 text-emerald-700 dark:text-emerald-400 font-semibold text-sm">
              <Server className="w-4 h-4" />
              2. FastAPI Backend
            </div>
            <p className="text-xs text-slate-600 dark:text-slate-300">
              Uvicorn ASGI runner, strict Pydantic schemas, CORS middleware, centralized error handling, and swagger OpenAPI docs.
            </p>
          </div>

          {/* Inference Engine Card */}
          <div className="p-4 rounded-xl border border-purple-200 bg-purple-50/50 dark:border-purple-900/50 dark:bg-purple-950/20">
            <div className="flex items-center gap-2 mb-2 text-purple-700 dark:text-purple-400 font-semibold text-sm">
              <Cpu className="w-4 h-4" />
              3. ML Pipelines
            </div>
            <p className="text-xs text-slate-600 dark:text-slate-300">
              Phase 1 serialized TF-IDF vectorizers and calibrated Scikit-learn pipelines with singleton memory caching.
            </p>
          </div>

          {/* SQLite Database Card */}
          <div className="p-4 rounded-xl border border-amber-200 bg-amber-50/50 dark:border-amber-900/50 dark:bg-amber-950/20">
            <div className="flex items-center gap-2 mb-2 text-amber-700 dark:text-amber-400 font-semibold text-sm">
              <Database className="w-4 h-4" />
              4. SQLite Database
            </div>
            <p className="text-xs text-slate-600 dark:text-slate-300">
              Normalized storage auto-seeded with 3,078 curated records, indexing pagination queries, and trend aggregations.
            </p>
          </div>
        </div>
      </div>

      {/* Technology Stack Grid */}
      <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700/60 p-6 shadow-sm">
        <h2 className="text-lg font-bold text-slate-800 dark:text-slate-100 mb-6 flex items-center gap-2">
          <Code className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
          Technical Stack
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Frontend */}
          <div className="space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">Frontend Layer</h3>
            <div className="flex flex-wrap gap-2">
              {['React 18', 'Vite 5', 'Tailwind CSS 3', 'React Router v6', 'Recharts', 'Axios', 'Lucide React'].map((tech) => (
                <span key={tech} className="px-2.5 py-1 text-xs font-medium rounded-md bg-slate-100 dark:bg-slate-700/50 text-slate-700 dark:text-slate-300">
                  {tech}
                </span>
              ))}
            </div>
          </div>

          {/* Backend */}
          <div className="space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">Backend & API</h3>
            <div className="flex flex-wrap gap-2">
              {['Python 3.11+', 'FastAPI', 'Uvicorn ASGI', 'Pydantic v2', 'SQLite 3', 'HTTPX'].map((tech) => (
                <span key={tech} className="px-2.5 py-1 text-xs font-medium rounded-md bg-slate-100 dark:bg-slate-700/50 text-slate-700 dark:text-slate-300">
                  {tech}
                </span>
              ))}
            </div>
          </div>

          {/* Machine Learning */}
          <div className="space-y-3">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">Machine Learning & Data</h3>
            <div className="flex flex-wrap gap-2">
              {['Scikit-Learn', 'TF-IDF Vectorizer', 'Joblib', 'Pandas', 'NumPy', 'NLTK'].map((tech) => (
                <span key={tech} className="px-2.5 py-1 text-xs font-medium rounded-md bg-slate-100 dark:bg-slate-700/50 text-slate-700 dark:text-slate-300">
                  {tech}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Machine Learning Specifications */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700/60 p-6 shadow-sm">
          <div className="flex items-center gap-3 mb-3">
            <div className="p-2 rounded-lg bg-emerald-50 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400">
              <Activity className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-slate-800 dark:text-slate-100">Sentiment Model</h3>
              <span className="text-xs text-slate-500">TF-IDF + Calibrated LinearSVC</span>
            </div>
          </div>
          <p className="text-xs text-slate-600 dark:text-slate-300 mb-3">
            Trained and serialized in Phase 1 (`models/sentiment_pipeline.pkl`). Evaluates polarity scores across 3 target classes:
          </p>
          <div className="flex gap-2">
            <span className="px-2.5 py-1 rounded bg-emerald-100 text-emerald-800 text-xs font-semibold dark:bg-emerald-900/40 dark:text-emerald-300">Positive</span>
            <span className="px-2.5 py-1 rounded bg-rose-100 text-rose-800 text-xs font-semibold dark:bg-rose-900/40 dark:text-rose-300">Negative</span>
            <span className="px-2.5 py-1 rounded bg-amber-100 text-amber-800 text-xs font-semibold dark:bg-amber-900/40 dark:text-amber-300">Neutral</span>
          </div>
        </div>

        <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700/60 p-6 shadow-sm">
          <div className="flex items-center gap-3 mb-3">
            <div className="p-2 rounded-lg bg-indigo-50 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400">
              <Layers className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-slate-800 dark:text-slate-100">Issue Classification Model</h3>
              <span className="text-xs text-slate-500">TF-IDF + Logistic Regression / LinearSVC</span>
            </div>
          </div>
          <p className="text-xs text-slate-600 dark:text-slate-300 mb-3">
            Trained and serialized in Phase 1 (`models/issue_pipeline.pkl`). Automatically routes complaints to 6 operational buckets:
          </p>
          <div className="flex flex-wrap gap-1.5">
            {['Product Issue', 'Delivery Issue', 'Payment Issue', 'Technical Issue', 'Service Issue', 'General Feedback'].map((cat) => (
              <span key={cat} className="px-2 py-0.5 rounded bg-indigo-50 text-indigo-700 text-xs font-medium dark:bg-indigo-900/40 dark:text-indigo-300">
                {cat}
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Project Team Section Placeholder */}
      <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700/60 p-6 shadow-sm">
        <h2 className="text-lg font-bold text-slate-800 dark:text-slate-100 mb-4 flex items-center gap-2">
          <Users className="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
          Project Team & Academic Credits
        </h2>
        <p className="text-xs text-slate-500 dark:text-slate-400 mb-6">
          This system was developed as a final year undergraduate major engineering project.
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="p-4 rounded-lg bg-slate-50 dark:bg-slate-900/40 border border-slate-200/60 dark:border-slate-700/40 text-center">
            <div className="w-12 h-12 mx-auto rounded-full bg-indigo-100 dark:bg-indigo-900/50 flex items-center justify-center text-indigo-600 dark:text-indigo-400 font-bold mb-2">
              TM1
            </div>
            <div className="text-sm font-semibold text-slate-800 dark:text-slate-200">Project Contributor</div>
            <div className="text-xs text-slate-500 dark:text-slate-400">Machine Learning & Core Pipeline</div>
          </div>

          <div className="p-4 rounded-lg bg-slate-50 dark:bg-slate-900/40 border border-slate-200/60 dark:border-slate-700/40 text-center">
            <div className="w-12 h-12 mx-auto rounded-full bg-purple-100 dark:bg-purple-900/50 flex items-center justify-center text-purple-600 dark:text-purple-400 font-bold mb-2">
              TM2
            </div>
            <div className="text-sm font-semibold text-slate-800 dark:text-slate-200">Project Contributor</div>
            <div className="text-xs text-slate-500 dark:text-slate-400">FastAPI & Database Systems</div>
          </div>

          <div className="p-4 rounded-lg bg-slate-50 dark:bg-slate-900/40 border border-slate-200/60 dark:border-slate-700/40 text-center">
            <div className="w-12 h-12 mx-auto rounded-full bg-blue-100 dark:bg-blue-900/50 flex items-center justify-center text-blue-600 dark:text-blue-400 font-bold mb-2">
              TM3
            </div>
            <div className="text-sm font-semibold text-slate-800 dark:text-slate-200">Project Contributor</div>
            <div className="text-xs text-slate-500 dark:text-slate-400">Frontend UI & Data Visualizations</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default About;
