# 17. System Limitations

While the platform achieves high precision and responsiveness, several operational and technical constraints should be noted:

### 1. English Language Scope
The current text preprocessing and WordNet lemmatization pipeline is tailored specifically to English vocabulary and syntax. Multi-lingual feedback or non-English text requires separate tokenization and language detection steps.

### 2. Domain-Specific Taxonomy
The issue classification taxonomy is fixed to six predefined operational categories (`Product Issue`, `Delivery Issue`, `Payment Issue`, `Technical Issue`, `Service Issue`, `General Feedback`). Unforeseen categories (e.g., legal inquiries, regulatory compliance, investor relations) are mapped to the nearest semantic neighbor or General Feedback.

### 3. Sarcasm and Complex Irony
While negation preservation successfully handles direct negative qualifiers (`"not great"`, `"never arrived"`), deeply nuanced figurative language or indirect sarcasm (e.g., *"Another masterpiece of software engineering where nothing opens"*) may pose challenges for linear TF-IDF n-gram models.

### 4. Single-Relational Database Architecture
SQLite provides fast, single-file relational storage ideal for single-instance deployments and low-to-medium scale applications. For distributed multi-node enterprise environments with concurrent write surges, a distributed database like PostgreSQL or MySQL is recommended.

### 5. Static Batch Retraining
The current machine learning pipelines are statically serialized. They do not continually update their weights online from incoming customer feedback; retraining requires running the training scripts and re-serializing the models.
