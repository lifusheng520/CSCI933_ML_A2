"""
Baseline system scaffold.

Students must implement a baseline for comparison with the RAG system.
A baseline may be:
- prompt-only generation without retrieval;
- simple keyword search;
- retrieval-only response without generation;
- another justified minimal approach.

The baseline must be described and compared against the improved RAG system.
"""

from __future__ import annotations
from transformers import AutoTokenizer, AutoModelForCausalLM

from prompts.baseline_prompt import build_prompt


def baseline_answer(prompt):
    """
    Placeholder baseline.

    Replace this with a real baseline method.
    """
    # TODO: Implement a meaningful baseline.

    # get model
    model_name = "distilgpt2"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    inputs = tokenizer(prompt, return_tensors="pt")

    outputs = model.generate(
        **inputs,
        max_new_tokens=50,
        do_sample=True,
        temperature=0.7,
        top_k=50,
        top_p=0.95
    )
    generate_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    answer = generate_text[len(prompt):]
    return answer




#test
if __name__ == "__main__":
    question = "Who is Hamlet?"
    print("Question:", question)
    prompt = build_prompt(question)
    print(baseline_answer(prompt))
