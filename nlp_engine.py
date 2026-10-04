import json
import re
import os
from typing import List, Dict, Any, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.stem import PorterStemmer

# Download NLTK resources quietly if needed
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    try:
        nltk.download('stopwords', quiet=True)
    except Exception:
        pass

ENGLISH_STOP_WORDS = {
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are',
    'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by',
    'can', 'did', 'do', 'does', 'doing', 'down', 'during', 'each', 'few', 'for', 'from', 'further',
    'had', 'has', 'have', 'having', 'he', 'her', 'here', 'hers', 'herself', 'him', 'himself', 'his',
    'how', 'i', 'if', 'in', 'into', 'is', 'it', "it's", 'its', 'itself', 'just', 'me', 'more', 'most',
    'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'our',
    'ours', 'ourselves', 'out', 'over', 'own', 's', 'same', 'she', 'should', 'so', 'some', 'such',
    'than', 'that', "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there',
    'these', 'they', 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was',
    'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with',
    'you', 'your', 'yours', 'yourself', 'yourselves'
}

class CollegeFAQEngine:
    def __init__(self, data_path: str = None):
        if data_path is None:
            data_path = os.path.join(os.path.dirname(__file__), "faq_data.json")
        self.data_path = data_path
        self.stemmer = PorterStemmer()
        self.vectorizer = None
        self.corpus_vectors = None
        self.faq_list: List[Dict[str, Any]] = []
        self.flat_corpus: List[str] = []
        self.corpus_mapping: List[int] = [] # Maps flat corpus index back to faq item index
        self.categories: List[str] = []
        
        self.load_data()
        self.build_index()

    def preprocess(self, text: str) -> str:
        """Clean, lower-case, remove punctuation and stem text."""
        if not text:
            return ""
        # Lowercase
        text = text.lower()
        # Remove non-alphanumeric characters except spaces
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        # Tokenize by whitespace
        tokens = text.split()
        # Remove stopwords and stem remaining words
        cleaned_tokens = [self.stemmer.stem(w) for w in tokens if w not in ENGLISH_STOP_WORDS]
        return " ".join(cleaned_tokens) if cleaned_tokens else " ".join(tokens)

    def load_data(self):
        """Load FAQ items from JSON data file."""
        with open(self.data_path, "r", encoding="utf-8") as f:
            self.faq_list = json.load(f)
        
        # Extract unique categories
        cat_set = set(item.get("category", "General") for item in self.faq_list)
        self.categories = ["All Categories"] + sorted(list(cat_set))

    def build_index(self):
        """Prepare flat text corpus and train TF-IDF vectorizer."""
        self.flat_corpus = []
        self.corpus_mapping = []

        for idx, item in enumerate(self.faq_list):
            # Include main question
            main_q = item["question"]
            processed_main = self.preprocess(main_q)
            self.flat_corpus.append(processed_main)
            self.corpus_mapping.append(idx)

            # Include question variations for better recall
            for var in item.get("variations", []):
                processed_var = self.preprocess(var)
                if processed_var:
                    self.flat_corpus.append(processed_var)
                    self.corpus_mapping.append(idx)

        # Train TF-IDF vectorizer (unigram + bigram)
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        self.corpus_vectors = self.vectorizer.fit_transform(self.flat_corpus)

    def get_answer(self, query: str, category_filter: str = "All Categories", threshold: float = 0.40) -> Dict[str, Any]:
        """Find the best matching answer for a user query."""
        if not query or not query.strip():
            return {
                "answer": "Please ask a question regarding College Exams, Fees, Timetable, Placements, Hostel, or Events!",
                "matched_question": "",
                "category": "",
                "confidence": 0.0,
                "suggestions": []
            }

        processed_query = self.preprocess(query)
        if not processed_query:
            processed_query = query.lower()

        query_tokens = set(processed_query.split())

        query_vector = self.vectorizer.transform([processed_query])
        similarities = cosine_similarity(query_vector, self.corpus_vectors)[0]

        # Filter by category if specified
        valid_indices = []
        for corpus_idx, faq_idx in enumerate(self.corpus_mapping):
            item_cat = self.faq_list[faq_idx].get("category", "General")
            if category_filter == "All Categories" or item_cat == category_filter:
                valid_indices.append(corpus_idx)

        if not valid_indices:
            return {
                "answer": f"No questions found in the category '{category_filter}'. Try searching under 'All Categories'.",
                "matched_question": "",
                "category": category_filter,
                "confidence": 0.0,
                "suggestions": []
            }

        # Find maximum similarity among valid corpus entries
        best_corpus_idx = valid_indices[0]
        max_sim = -1.0

        for corpus_idx in valid_indices:
            sim = similarities[corpus_idx]
            if sim > max_sim:
                max_sim = sim
                best_corpus_idx = corpus_idx

        # Calculate token overlap between query and best corpus entry
        best_corpus_text = self.flat_corpus[best_corpus_idx]
        corpus_tokens = set(best_corpus_text.split())
        overlap = query_tokens.intersection(corpus_tokens)
        
        # Token overlap ratio relative to query length
        overlap_ratio = len(overlap) / max(len(query_tokens), 1)

        # Rank top suggestions
        scored_corpus = [(corpus_idx, similarities[corpus_idx]) for corpus_idx in valid_indices]
        scored_corpus.sort(key=lambda x: x[1], reverse=True)

        # Collect unique top suggested questions
        top_suggestions = []
        seen_faqs = set()
        for c_idx, sim in scored_corpus:
            f_idx = self.corpus_mapping[c_idx]
            if f_idx not in seen_faqs:
                seen_faqs.add(f_idx)
                top_suggestions.append(self.faq_list[f_idx]["question"])
                if len(top_suggestions) >= 3:
                    break

        matched_faq = self.faq_list[self.corpus_mapping[best_corpus_idx]]

        # Require reasonable similarity and at least some token overlap
        if max_sim >= threshold and (overlap_ratio >= 0.25 or len(overlap) >= 2 or max_sim > 0.65):
            return {
                "answer": matched_faq["answer"],
                "matched_question": matched_faq["question"],
                "category": matched_faq["category"],
                "confidence": round(float(max_sim) * 100, 1),
                "suggestions": top_suggestions[1:] if len(top_suggestions) > 1 else []
            }
        else:
            fallback_msg = (
                "I couldn't find an exact match for your query in our FAQ database. "
                "Please check the suggested questions below, or contact the Academic Helpdesk at support@college.edu / Window No. 4."
            )
            return {
                "answer": fallback_msg,
                "matched_question": "",
                "category": matched_faq["category"],
                "confidence": round(float(max_sim) * 100, 1),
                "suggestions": top_suggestions
            }

if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass

    # Self-test
    engine = CollegeFAQEngine()
    test_queries = [
        "What are the library timings?",
        "How can I apply for a bonafide certificate?",
        "When are the semester exams?",
        "How much is the hostel fee?",
        "What is the rocket launch schedule?" # Out of scope
    ]
    print("=== NLP Engine Self-Test ===")
    for q in test_queries:
        res = engine.get_answer(q)
        print(f"\nUser Query: {q}")
        print(f"Confidence: {res['confidence']}%")
        print(f"Matched Q: {res['matched_question']}")
        print(f"Answer: {res['answer']}")
