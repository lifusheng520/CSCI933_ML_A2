from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
# model_name = "microsoft/phi-2"

# Load tokenizer + model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    # torch_dtype=torch.float32,   # CPU safe
    torch_dtype=torch.bfloat16,   # CPU safe
    device_map="cpu",
)

# Simple prompt
query = "Who is Macbeth? Answer briefly."
# query = "Who are you?"
prompt = f"""<|system|>
You are a Shakespeare expert assistant.

Rules:
- Answer concisely, clearly and directly.
- Do NOT write scripts, dialogues, or plays.
- Do NOT invent characters or scenes.
- Keep answers short and factual.
- If unsure, say you don't know.
- Do NOT repeat your answers.

<|user|>
{query}

<|assistant|>
"""
print(prompt)

# Tokenize
inputs = tokenizer(prompt, return_tensors="pt")

# Generate
outputs = model.generate(
    **inputs,
    # max_new_tokens=100, #. phi-2
    max_new_tokens=120, # gemma-2b-it
    temperature=0.3,
    do_sample=True,
    # eos_token_id=tokenizer.eos_token_id,
    top_k = 2
)

# Decode
response = tokenizer.decode(outputs[0], skip_special_tokens=True)

print(response)