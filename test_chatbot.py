from utils.chatbot import HRChatbot

bot = HRChatbot()

print("=" * 80)
print("Enterprise HR Chatbot")
print("=" * 80)

while True:

    question = input("\nEmployee : ")

    if question.lower() == "exit":
        break

    answer = bot.chat(question)

    print("\nHR Bot :\n")

    print(answer)