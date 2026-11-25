import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")

text = """
My name is Rahul.
I am learning Python.
I am learning machine learning.
I am learning generative AI.
I want to become an AI Engineer.
"""

tokens = encoding.encode(text)

print("Original text:")
print(text)

print("\nToken IDs:")
print(tokens)

print("\nToken pieces:")

for token in tokens:
    piece = encoding.decode([token])
    print(repr(piece))
