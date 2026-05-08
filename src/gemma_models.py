import torch
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

class GemmaAssistant:
    def __init__(self, model_name="google/gemma-3-1b-it"):
        print(f"Loading model: {model_name}...")
        self.device = "mps" if torch.backends.mps.is_available() else "cpu"
        
        # Load once and move to device
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name, 
            dtype=torch.float32 if self.device == "mps" else torch.float32
        ).to(self.device)
        self.model.eval()
        
        print("Model loaded successfully.")
        print(f"Using device: {self.device}")

    def generate_answer(self, query, max_new_tokens=150):

        # Format the system prompt and query
        system_rules = (
            "You are a Shakespeare expert assistant.\n"
            "Rules:\n"
            "- Answer concisely, clearly and directly.\n"
            "- Do NOT write scripts, dialogues, or plays.\n"
            "- Keep answers short and factual.\n"
            "- If unsure, say you don't know."
        )

        # for test
        # messages = [
        #     {"role": "user", "content": f"{system_rules}\n\nQuestion: {query}"},
        # ]

        # for API call
        messages = [
            {"role": "user", "content": query},
        ]

        # Process tokens
        inputs = self.tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
        ).to(self.device)

        # Generate
        # with torch.no_grad(): # Disable gradient calculation for inference speed
        outputs = self.model.generate(
            **inputs, 
            max_new_tokens=max_new_tokens,
            do_sample=False,
            pad_token_id=self.tokenizer.pad_token_id if self.tokenizer.pad_token_id is not None else self.tokenizer.eos_token_id,
            eos_token_id=self.tokenizer.eos_token_id
        )

        # Decode only the newly generated tokens
        input_length = inputs["input_ids"].shape[-1]
        decoded = self.tokenizer.decode(outputs[0][input_length:], skip_special_tokens=True)
        return decoded.strip()

    def summarize(self, query, max_new_tokens=150):

        # Format the system prompt and query
        system_rules = (
            "You are a Shakespeare expert assistant.You summary the input briefly.\n"
            "Rules:\n"
            "- Answer concisely, clearly and directly.\n"
            "- Do NOT write scripts, dialogues, or plays.\n"
            "- Keep answers short and factual.\n"
            "- If unsure, say you don't know."
        )

        messages = [
            {"role": "user", "content": f"{system_rules}\n\nQuestion: {query}"},
        ]

        # Process tokens
        inputs = self.tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
        ).to(self.device)

        # Generate
        # with torch.no_grad(): # Disable gradient calculation for inference speed
        outputs = self.model.generate(
            **inputs, 
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.7,
            pad_token_id=self.tokenizer.eos_token_id
        )

        # Decode only the newly generated tokens
        input_length = inputs["input_ids"].shape[-1]
        decoded = self.tokenizer.decode(outputs[0][input_length:], skip_special_tokens=True)
        return decoded.strip()

if __name__ == "__main__":

    # Gemma Models
    # model_name = "google/gemma-2b-it"   # instruction-tuned version
    # model_name = "google/gemma-1.1-2b-it"   # instruction-tuned version
    model_name = "google/gemma-3-270m-it"   # instruction-tuned version
    # model_name = "google/gemma-3-1b-it"   # instruction-tuned version
    # model_name = "google/gemma-3-4b-it"   # instruction-tuned version

    # 1. Initialize once (this takes time)
    assistant = GemmaAssistant(model_name)

    # 2. Call frequently (this is fast)
    queries = [
        "Why did Macbeth kill Ducan?",
        "Who is Macbeth?",
        "What is the significance of the three witches?",
        "Where does Hamlet take place?",
    ]

    for q in queries:
        print(f"\nUser: {q}")
        answer = assistant.generate_answer(q)
        print(f"Assistant: {answer}")