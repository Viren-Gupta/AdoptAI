import Rag as rag
import numpy as np
import ollama as olm # importing ollama model client library

# Pull a model
olm.pull('gemma3')

rag = rag.Rag()
rag.initRag()

user_input = input("Enter query\n")
use_rag = input("Enter 1 for Rag based results and 0 for non Rag based results\n")

if use_rag == "0":
    modelQuery = user_input
else:
    ragOutput = rag.getSimilarContent(user_input)
    modelQuery = user_input + " with reference as the following \n" + ragOutput[0]

messages = [
    {'role': 'user', 'content': modelQuery},
]

print("Model Query: " + modelQuery)
response = olm.chat(model='gemma3', messages=messages)
print(response['message']['content'])