# !pip install transformers

# # Include the os.eviron things before.

# model_name = "Qwen/Qwen2.5-3B"

# from transformers import AutoTokenizer

# tokenizer = AutoTokenizer.from_pretrained(model_name)

# print(tokenizer("Hello, there mate!"))
# input_tokens = tokenizer("Hello, there mate!")['input_ids']
# print(input_tokens)

# print(tokenizer.get_vocab())

# from transformers import AutoModelForCausalLM

# import torch
# model = AutoModelForCausalLM.from_pretrained(model_name, dtype=torch.bfloat16)

# from transformers import pipeline

# gen_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)

# gen_pipeline("Hey, there mate!", max_new_tokens=25)

# tokens = tokenizer("The most dense body in the universe?", return_tensors="pt")['input_ids']
# print(tokens)

# gen_tokens = model.generate(tokens, max_new_tokens=25)
# print(gen_tokens)

# output = tokenizer.batch_decode(gen_tokens)
# output