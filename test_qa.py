from utils.qa import DocumentQA

qa = DocumentQA()

print("=" * 80)
print("Enterprise AI Document Intelligence")
print("=" * 80)

while True:

    question = input("\nAsk a Question (type exit to quit): ")

    if question.lower() == "exit":
        break

    answer = qa.ask(question)

    print("\nAnswer:\n")

    print(answer)

    print("-" * 80)