### VER VERY IMPORTANT: 
- If you want response in json then you must include the word "json" in the user input. If you don't include it then the model will throw an error. This is because the model is not able to understand that you want the response in json format. So, always include the word "json" in the user input if you want the response in json format.

- **In Python, chat_completion.choices[0].message.content evaluates to a plain Python string (<class 'str'>).**
- **Even though you have turned on JSON mode, the API always transmits the final payload across the network as raw text.**