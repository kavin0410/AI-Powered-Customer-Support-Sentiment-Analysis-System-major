# 01. Abstract

## Project Title
**AI-Powered Customer Support & Sentiment Analysis System**

## Abstract
Modern enterprises experience an exponential volume of incoming customer support communications across online portals, emails, social media, and ticketing platforms. The overwhelming scale and unstructured nature of this feedback introduce severe operational bottlenecks: high manual triage latency, misrouted tickets, and failure to detect critical service outages or payment failures in real time. 

This major capstone engineering project delivers an end-to-end, full-stack intelligence system combining calibrated machine learning algorithms, high-throughput backend APIs, relational database persistence, and an interactive modern web dashboard. 

The core predictive foundation leverages Natural Language Processing (NLP) techniques, including customized contraction expansion, punctuation sanitization, negation-preserving stopword filtering, and WordNet lemmatization. Feature extraction is performed using sublinear TF-IDF vectorization with unigram and bigram representation. Two specialized classification models—a 3-class Sentiment Analysis model (Positive, Negative, Neutral) and a 6-class Customer Issue Categorizer (Product Issue, Delivery Issue, Payment Issue, Technical Issue, Service Issue, General Feedback)—are deployed with calibrated probability distributions.

A production-grade REST API developed in FastAPI (Python) encapsulates the inference engines and connects to a normalized SQLite database pre-seeded with 3,078 verified customer interaction records. A modern Single Page Application (SPA) built with React 18, Vite, Tailwind CSS, and Recharts interfaces with the backend to provide real-time KPI tracking, server-side paginated record exploration, dual-task prediction with rule-based attention level triage (High, Medium, Low), multi-dimensional analytics, dynamic business insights, and full dark/light theme support. Comprehensive evaluation confirms robust generalization, zero data leakage, and high reliability across 38 automated test cases.
