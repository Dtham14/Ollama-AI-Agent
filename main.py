from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

model = OllamaLLM(model="llama3.2")

template = """
You are an expert in answering question about Music Theory.  
Here are some facts: {facts}
Here is the question to answer: {question}
"""

prompt = ChatPromptTemplate.from_template(template)

chain = prompt | model

while True:
    print("\n\n====================================================")
    question = input("Ask your question (q to quit):\n")
    if question ==  "q":
        break   
    
    facts = retriever.invoke(question)
    result = chain.invoke({"facts": facts, "question": question})
    print("\n\n====================================================")
    print("\n" + result)



