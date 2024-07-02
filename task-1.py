def chatbot_response(user_input):
    user_input = user_input.lower()

    if "hello" in user_input or "hi" in user_input:
        return "Hello! How can I assist you today?"
    elif "how are you" in user_input:
        return "I'm just a chatbot, but I'm doing great! How can I help you?"
    elif "what is your name" in user_input:
        return "I am a simple chatbot created to assist you. What's your name?"
    elif "bye" in user_input or "goodbye" in user_input:
        return "Goodbye! Have a great day!"
    else:
        return "I'm sorry, I didn't understand that. Can you please rephrase?"


print("Chatbot: Hello! How can I assist you today?")

while True:
    user_input = input("You: ")
    response = chatbot_response(user_input)
    print("Chatbot:", response)
    
    if "bye" in user_input or "goodbye" in user_input:
        break