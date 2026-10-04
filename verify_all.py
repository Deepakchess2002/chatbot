import sys
from nlp_engine import CollegeFAQEngine

def verify():
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass

    engine = CollegeFAQEngine()
    test_queries = [
        "What are the library timings?",
        "How can I apply for a bonafide certificate?",
        "When are the semester exams?",
        "How can I pay my semester tuition fees online?",
        "When do campus placement drives start?",
        "What is the hostel fee structure?",
        "When is the college annual cultural fest held?",
        "What is the minimum attendance requirement?"
    ]

    print("==========================================================")
    print("   COLLEGE FAQ CHATBOT - BENCHMARK VERIFICATION RESULT")
    print("==========================================================\n")

    for q in test_queries:
        res = engine.get_answer(q)
        print(f"Student Query: \"{q}\"")
        print(f"  ➜ Matched Category   : {res['category']}")
        print(f"  ➜ Confidence Score   : {res['confidence']}%")
        print(f"  ➜ Matched FAQ Title  : {res['matched_question']}")
        print(f"  ➜ Chatbot Response   : {res['answer']}\n")
        print("-" * 58)

if __name__ == "__main__":
    verify()
