import sys
from nlp_engine import CollegeFAQEngine

def run_cli():
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass

    print("=" * 65)
    print("      GRADUATE COLLEGE FAQ CHATBOT (NLP DRIVEN)")
    print("=" * 65)
    print("Type your questions below (e.g. 'What are the library timings?').")
    print("Type 'category' to set a topic filter, or 'exit' / 'quit' to exit.\n")

    engine = CollegeFAQEngine()
    current_category = "All Categories"

    while True:
        try:
            prompt = f"[{current_category}] Student: "
            user_query = input(prompt).strip()
            
            if not user_query:
                continue

            if user_query.lower() in ["exit", "quit", "q", "bye"]:
                print("\nChatbot: Thank you for using College FAQ Chatbot. Good luck with your studies!")
                break

            if user_query.lower() == "category":
                print("\nAvailable Categories:")
                for idx, cat in enumerate(engine.categories, 1):
                    print(f"  {idx}. {cat}")
                choice = input("\nSelect category number: ").strip()
                if choice.isdigit() and 1 <= int(choice) <= len(engine.categories):
                    current_category = engine.categories[int(choice) - 1]
                    print(f"Active category set to: {current_category}\n")
                else:
                    print("Invalid choice. Keeping active category.\n")
                continue

            # Query NLP Engine
            res = engine.get_answer(user_query, category_filter=current_category)

            print(f"\nChatbot [{res['confidence']}% match]: {res['answer']}")
            if res.get("matched_question"):
                print(f"Matched FAQ: \"{res['matched_question']}\"")
            if res.get("suggestions"):
                print("Related Questions:")
                for sug in res["suggestions"]:
                    print(f"  • {sug}")
            print("-" * 65 + "\n")

        except KeyboardInterrupt:
            print("\nExiting Chatbot. Bye!")
            break
        except Exception as e:
            print(f"Error processing query: {e}\n")

if __name__ == "__main__":
    run_cli()
