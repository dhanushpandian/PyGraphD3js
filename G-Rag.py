from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template="""
Answer the question below:

here is the conversation history: {context}

Question: {input}

Answer:
"""

model = OllamaLLM(model="llama3.1:8b") 
prompt = ChatPromptTemplate.from_template(template)

chain = prompt | model

# # result=model.invoke(input="Hello, how are you?")
#         result = chain.invoke({"context": "my name is dhanush ", "input": })
#         print(result)

def handle_message():
    context="my name is dhanush"
    print("Welcome to the chatbot")
    while True:
        input_message = input("You: ")
        if input_message == "exit":
            break
        result = chain.invoke({"context": context, "input": input_message})
        print("Bot: ", result)
        context += f'\n User: {input_message} \n Bot: {result}'

if __name__ == "__main__":
    handle_message()
