from langchain_ollama import OllamaLLM

model = OllamaLLM(model='llama3.2')


def generate_response(user_query, retrieved_data):
    # For bullet points, header use this prompt
    '''"You are an intelligent chatbot representing Apollo Hospital. Your role is to respond to user queries in a "
        "friendly, informative, and structured manner using the information provided below. Structure your response in a clear format with headings, bullet points, and relevant details where necessary.\n\n"
        f"Retrieved Information: {retrieved_data}\n\n"
        f"User Query: {user_query}\n\n"
        "Chatbot Response:"'''
    input_prompt = (
        "You are Sona, an intelligent AI chatbot representing Apollo Adlux Hospital. Your role is to respond to user "
        "queries based on the provided information"
        f"Retrieved Information: {retrieved_data}\n\n"
        f"User Query: {user_query}\n\n"
        "Chatbot Response:"
    )

    result = model.invoke(input=input_prompt)

    return result


"""
user_query = "How can I cope with my increased sensitivity to light?"
retrieved_data = (
    "Increased sensitivity to light can result from migraines, eye strain, or other conditions. Wearing sunglasses "
    "and consulting an eye care professional for evaluation can be beneficial."
)
print(generate_response(user_query, retrieved_data))
"""
"""
while True:
    user_query = input('Enter a user query: ')
    retrieved_data = input("Enter retrieved data: ")
    print(generate_response(user_query, retrieved_data))
"""
