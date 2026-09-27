# 10. Text Preprocessing Pipeline

Customer natural language input typically contains typos, contractions, URLs, informal abbreviations, and irregular casing. A custom `TextPreprocessor` stage transforms raw text into clean, standardized tokens suitable for TF-IDF feature extraction.

## Preprocessing Pipeline Architecture

```
Raw Customer Text
       │
       ▼
1. Case Normalization (Lowercase)
       │
       ▼
2. Noise Sanitization (Remove URLs, Emails, Special Punctuation)
       │
       ▼
3. Contraction Expansion ("can't" -> "cannot", "won't" -> "will not")
       │
       ▼
4. Negation-Preserving Stopword Filtering (Retaining: not, no, nor, never, neither)
       │
       ▼
5. WordNet Lemmatization (nouns/verbs to canonical dictionary roots)
       │
       ▼
Preprocessed Standardized Tokens
```

## Critical Preprocessing Stages

### 1. Contraction Expansion
Informal customer speech frequently shortens negations and pronouns. A lookup dictionary expands these before tokenization:
- `"wasn't"` $\rightarrow$ `"was not"`
- `"didn't"` $\rightarrow$ `"did not"`
- `"couldn't"` $\rightarrow$ `"could not"`

### 2. Negation Preservation
Standard NLP stopword lists (such as default NLTK English stopwords) routinely remove tokens such as `"not"`, `"never"`, `"no"`, and `"without"`. In sentiment analysis, removing negations causes severe polarity inversion:
- Example: `"The product is not working"` $\rightarrow$ if `"not"` is stripped $\rightarrow$ `"product working"` (inverting Negative sentiment to Positive).
- **Solution:** A whitelist filters out stopwords while strictly preserving negation tokens:
  ```python
  NEGATION_WORDS = {"not", "no", "never", "nor", "neither", "barely", "hardly", "scarcely", "without", "cannot"}
  ```

### 3. Lemmatization
Utilizes NLTK's `WordNetLemmatizer` to reduce plural nouns and verb conjugations to base lexemes:
- `"headphones"` $\rightarrow$ `"headphone"`
- `"crashed"` $\rightarrow$ `"crash"`
- `"delivering"` $\rightarrow$ `"deliver"`
