
#         # Don't run this code here


# # transformers is a library from hugging face
# from transformers import AutoTokenizer 
# from transformers import AutoModelForCausalLM
# # Causal llm is the model that predicts the next word (like gpt)

# from dotenv import load_dotenv
# load_dotenv()

# model_name = "Qwen/Qwen2.5-3B"

# tokenizer = AutoTokenizer.from_pretrained(model_name) # gets the tokenizer of the chosen model

# # print(tokenizer("Hello, there mate!"))
# # print(tokenizer.get_vocab())

# tokens = tokenizer("Hello, there mate!")['input_ids']
# # print (tokens)

# model = AutoModelForCausalLM.from_pretrained(model_name, )

# from transformers import pipeline
# gen_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)

# gen_pipeline("Hey, there mate!", max_new_tokens=25)