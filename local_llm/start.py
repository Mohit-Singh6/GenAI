import ollama

# Prepare the conversation history
messages = [
    {"role": "system", "content": "You are a expert assistant in explaining phenomenons."},
    {"role": "user", "content": "What is a black hole."}
]



# Call the local model (make sure you downloaded qwen2.5:3b first!)
stream = ollama.chat(
    model="qwen2.5:3b",
    messages=messages,
    stream=True
)

# Print out tokens in real-time as your CPU generates them
for chunk in stream:
    print(chunk.message.content, end="", flush=True)


    # Direct printing

# response = ollama.chat(
#     model="qwen2.5:3b",
#     messages=[
#         {"role": "user", "content": "Explain the difference between SQL and NoSQL in one sentence."}
#     ]
# )

# # Extract and print the content text block
# print(response.message.content)