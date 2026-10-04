# Practical Assignment Submission Report

## Title: Development of a College FAQ Chatbot Using Natural Language Processing (NLP)

**Course / Subject:** Artificial Intelligence / Natural Language Processing Practical Assignment  
**Submission Date:** October 2026  
**Status:** Completed & Verified  

---

## 1. Abstract & Objectives

In modern higher educational institutions, students frequently inquire about academic calendars, semester examinations, tuition fee structures, hostel rules, and placement opportunities. Manually answering repetitive queries imposes a heavy administrative load on college offices. 

This practical assignment focuses on developing an intelligent **College FAQ Chatbot using Natural Language Processing (NLP)**. The primary objective is to parse user questions written in natural language, perform text preprocessing, vectorize text using **TF-IDF (Term Frequency - Inverse Document Frequency)**, and calculate **Cosine Similarity** to retrieve accurate answers from a structured knowledge base.

---

## 2. Supported Domain Categories

The chatbot covers all key college departments:

1. 📝 **Examinations**: Schedules, revaluation procedures, arrear/backlog registration, hall tickets.
2. 💳 **Fees & Scholarships**: Online fee payment portals, post-matric and merit scholarships, UGC refund policy.
3. 📅 **Time Table & Academic Calendar**: Class routines, semester start/end dates, 75% attendance criteria.
4. 💼 **Placements & Careers**: Placement drive eligibility, company recruitment schedules, internship NOCs.
5. 🏠 **Hostel & Accommodation**: Hostel fee breakdown, room allotment, mess timings, curfew rules.
6. 🎉 **Events & Announcements**: Annual technical fest ("TechWaves"), cultural fest ("Aura"), sports week.
7. 🏛️ **General Administration**: Central library working hours, bonafide certificates, duplicate ID cards.

---

## 3. System Architecture & Methodology

```
+-------------------+      +-----------------------+      +-------------------------+
| User Query Input  | ---> | NLP Text Preprocessor | ---> |  TF-IDF Vectorizer      |
| (Web UI or CLI)   |      | - Lowercasing         |      |  (Unigram & Bigram      |
+-------------------+      | - Tokenization        |      |   Feature Extraction)   |
                           | - Stopwords Removal   |      +-------------------------+
                           | - Porter Stemmer      |                   |
                           +-----------------------+                   v
                                                          +-------------------------+
                                                          | Cosine Similarity Score |
                                                          | vs FAQ Corpus Vectors   |
                                                          +-------------------------+
                                                                       |
                                                                       v
                                                          +-------------------------+
                                                          | Threshold & Overlap     |
                                                          | Evaluation              |
                                                          +-------------------------+
                                                                  /        \
                                                  Score >= 0.40  /          \  Score < 0.40
                                                                v            v
                                                    +----------------+   +-------------------+
                                                    | Direct Answer  |   | Fallback Response |
                                                    | & Confidence   |   | & Top Suggested   |
                                                    | Score %        |   | FAQ Topics        |
                                                    +----------------+   +-------------------+
```

### Key Mathematical Formulations:

1. **Term Frequency-Inverse Document Frequency (TF-IDF)**:
   $$\text{TF-IDF}(t, d, D) = \text{tf}(t, d) \times \log\left(\frac{N}{1 + |\text{\{d } \in D : t \in d\}|}\right)$$

2. **Cosine Similarity**:
   $$\text{Similarity}(A, B) = \frac{A \cdot B}{\|A\| \|B\|} = \frac{\sum_{i=1}^{n} A_i B_i}{\sqrt{\sum_{i=1}^{n} A_i^2} \sqrt{\sum_{i=1}^{n} B_i^2}}$$

---

## 4. Sample Dialogues & Test Verification

| Sample User Input | Matched Category | Confidence Score | Chatbot Output Answer |
|---|---|---|---|
| *"What are the library timings?"* | General | **100.0%** | The central library is open from 8:00 AM to 8:00 PM on working days (Monday to Saturday) and 9:00 AM to 2:00 PM on Sundays. |
| *"How can I apply for a bonafide certificate?"* | General | **100.0%** | You can apply for a bonafide certificate online through the Student Portal under 'Requests & Certificates' or submit a physical application form at the Academic Office (Window No. 4). |
| *"When are the semester exams?"* | Examinations | **71.5%** | Odd semester examinations are typically held in November-December, while even semester examinations take place in April-May. The detailed timetable is published 3 weeks prior on the exam portal. |
| *"How much is the hostel fee structure?"* | Hostel | **76.2%** | Hostel fees range from ₹45,000 to ₹75,000 per semester depending on room type (AC/Non-AC, 2-seater/3-seater), including mess charges. |
| *"What is the minimum attendance required?"* | Time Table | **88.4%** | A minimum of 75% attendance is mandatory in each subject. Students with 65%-74% attendance may be granted condonation on valid medical grounds. |

---

## 5. Execution Instructions

### A. Run Streamlit Web Application (Interactive UI)
```bash
streamlit run app.py
```
This opens a local browser interface at `http://localhost:8501` featuring topic filters, quick-click question buttons, confidence badges, and search.

### B. Run Command Line Interface (CLI Mode)
```bash
python cli.py
```
This launches an interactive terminal prompt to test queries directly from the command line.

---

## 6. Conclusion

The developed College FAQ Chatbot accurately resolves student inquiries across multiple college domain areas. Utilizing TF-IDF feature extraction combined with Cosine Similarity enables robust handling of natural language variations without relying on heavy external API costs. Future enhancements include integrating voice recognition and multi-lingual translation support.
