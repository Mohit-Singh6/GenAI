
# Include the os.eviron things before.

import torch
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "Qwen/Qwen2.5-3B"

tokenizer = AutoTokenizer.from_pretrained(model_name)

tokenizer("Yo Yo")

input_conversation = [
    {"role": "user", "content": "Who is the best footballer of all time?"},
    {"role": "assistant", "content": "The best footballer of all time is"}
]

input_tokens = tokenizer.apply_chat_template(
    conversation = input_conversation,
    # tokenize=False # agar ye likhoge to wo normal way mein dikhayega (bina tokens mein convert kiye) (jaise wo model samajhta hai)
)
input_tokens

input_detokens = tokenizer.apply_chat_template (
    conversation = input_conversation,
    tokenize = False,
    continue_final_message = True # is se ye last mein eos nahi lagaega, taaki hum answer likhne ke baad khud laga saken
)
input_detokens

output_label = " Cristiano Ronaldo"
full_conversation = input_detokens + output_label + tokenizer.eos_token
full_conversation

input_tokenized = tokenizer(full_conversation, return_tensors="pt", add_special_tokes=False).to(device)["input_ids"]
input_tokenized

input_ids = input_tokenized[:, :-1].to(device)
target_ids = input_tokenized[:, 1:].to(device)
print("Input_ids: ", input_ids)
print("Target_ids: ", target_ids)

import torch.nn as nn
def calculate_loss(logits, labels):
  loss_fn = nn.CrossEntropyLoss(reduction="none")
  cross_entropy = loss_fn(logits.view(-1, logits.shape[-1]), labels.view(-1))
  return cross_entropy

import torch
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    dtype=torch.bfloat16
).to(device)

from torch.optim import AdamW
model.train()

optimizer = AdamW(model.parameters(), lr=3e-5, weight_decay=0.01)

for _ in range(2):
  out = model(input_ids=input_ids)
  loss = calculate_loss(out.logits, target_ids).mean()
  loss.backward()
  optimizer.step()
  optimizer.zero_grad()
  print(loss.item())

input_prompt = [
     {"role": "user", "content": "Who is the best footballer of all time?"}
 ]

 input = tokenizer.apply_chat_template(
     conversation=input_prompt,
     return_tensors="pt",
     tokenize=True
 ).to(device)

 output = model.generate(input, max_new_tokens=25)
 print(tokenizer.batch_decode(output, skip_special_tokens=True))

