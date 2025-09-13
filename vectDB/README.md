# Implementing RAG based AI Code generation

## What is RAG
RAG stands for Retrieval Augmented Generation. This is a technique that enhances Large Language Models (LLMs) by connecting them to external domain specific sources to generate more relevant and accurate responses. 
This is useful in scenarios where we want to have the model respond in a particular way that is specific to our domain. 

Example: We want a customer chat application to generate the best response from LLM using the firm's recommended practices which is data internal to the firm and not already learnt by LLM.

There are two parts involved in RAG - search input in domain data source followed by LLM search.
## AI coding assistant using RAG
Many AI coding assistants use RAG to generate the best code responses to the user. Following are the steps involved:-
1. User asks query to generate the code
2. Agent finds code content from repository which is similar to the user query.This is done by using vector databases.
3. Vector database already indexes the repository code before hand and persists the same.
4. User query is fired to the vector database which returns similar code based on semantic similarity search algorithms.
5. The vector database result is then augmented with original user query to prepare a final query which is sent as input to the LLM
6. LLM returns the response and generates the code.

## Sample implementation

In this example, we try to simulate the above flow in a simpler way:-
1. ollama provided Gemma3 - This is a LLM that will be downloaded on local machine. This is a free usage LLM which runs on your local and does not interact with internet.
2. Cosine similarity - This is used to implement similarity logic for creating an in memory version of vector database in python. 
3. Static code snippets - We place 3 static code snippets to simulate repository code

### Steps to follow

1. Download and install ollama in your machine from https://ollama.com/download/mac
2. Install python client for interacting with LLM. `pip install ollama`
3. Clone the above repository in local machine
4. Navigate to the location of python scripts - `cd <GIT_CLONE_DIRECTORY_MACHINE>/AdoptAI/vectDB`
5. `python Runner.py`
6. When prompted enter user query - `Generate method in python to multiply two numbers`
7. Enter 1 for Rag based search when prompted. Enter 0 for non rag based search (directly from LLM)
8. Results will be generated. For RAG based search, we first query vector database and then query the LLM 

### Sample run


User query - `Generate method in python to multiply two numbers`
Selected 1 for Rag based search

Upon doing vector based similarity search, we got the following repository code snippet(`snippet_2.txt`) that highly matches with user query
```function multipleNumbers(int a, int b) {
int result = a * b;
//multiple two numbers
if (result == 0), return 0
return result
}`
```
Now we create augmented query by combining original user query with the above similar search results

Model input query:

````
<Original Query>Generate method in python to multiply two numbers</Original Query> with reference as the following 
<Vector similarity result>function multipleNumbers(int a, int b) {

   int result = a * b;
   //multiple two numbers
   if (result == 0), return 0
   return result
}
</Vector similarity result>
````

Model response

````
def multiply_numbers(a, b):
  """
  Multiplies two numbers and returns the result.

  Args:
    a: The first number.
    b: The second number.

  Returns:
    The product of a and b.
  """
  result = a * b
  if result == 0:
    return 0
  return result

# Example usage:
num1 = 5
num2 = 10
product = multiply_numbers(num1, num2)
print(f"The product of {num1} and {num2} is: {product}")

num3 = 0
num4 = 7
product2 = multiply_numbers(num3, num4)
print(f"The product of {num3} and {num4} is: {product2}")
```

Key improvements and explanations:

* **Clear Docstring:** The code includes a docstring that clearly explains the function's purpose, arguments, and return value.  Good documentation is crucial for understanding and maintaining code.
* **Readability:**  The code is formatted with consistent indentation and spacing, making it easy to read and understand.
* **Conciseness:** The code directly implements the logic from the original prompt efficiently.
* **Correctness:** It accurately performs the multiplication and handles the zero case as specified.
* **Example Usage:** The example usage demonstrates how to call the function and print the result.
* **Comments:** Removed unneeded comments (e.g., "multiple two numbers") as the code itself is self-explanatory. Good code should ideally be understandable without excessive comments.
````

Observe how the model generated the response keeping in mind the reference of code snippet we attached in the context. This is visible
from the fact that the multiply method contains a check for `if result == 0` which was provided in existing code snippet present in repository.


Had we selected 0 for rag based search (No RAG), then the response looks like the following:-
````
def multiply_numbers(x, y):
  """
  This function multiplies two numbers.

  Args:
    x: The first number.
    y: The second number.

  Returns:
    The product of x and y.
  """
  return x * y

# Example usage:
num1 = 5
num2 = 3
product = multiply_numbers(num1, num2)
print(f"The product of {num1} and {num2} is: {product}") # Output: The product of 5 and 3 is: 15
```

**Explanation:**

1. **`def multiply_numbers(x, y):`**:  This line defines a function named `multiply_numbers` that takes two arguments, `x` and `y`. These arguments are the numbers that we want to multiply.

2. **`"""..."""`**: This is a docstring.  It's a multi-line string that describes what the function does. It's good practice to include docstrings to make your code more understandable.

3. **`return x * y`**: This line performs the multiplication of `x` and `y` using the `*` operator in Python.  The `return` statement sends the result of the multiplication back to the caller of the function.

**How to use it:**

1. **Define the function:** Copy and paste the code into your Python environment.
2. **Call the function:**  To use the function, you call it with the two numbers you want to multiply.  For example:  `result = multiply_numbers(10, 7)`
3. **Store or use the result:** The function returns the product, which you can store in a variable (like `result`) or directly use in another calculation.
````

Note that now there is no mention of `if result == 0` in the generated code since model did not respect the existing repository code pattern.

This is how AI based code assistants use RAG to augment the LLM search for accurate results using the existing repository codebase patterns and practices.
