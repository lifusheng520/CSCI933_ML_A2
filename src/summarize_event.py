import json
from gemma_models import GemmaAssistant

def get_llm_summary(assistant, text):

    prompt = build_prompt_no_rag(text)
    # Generate response
    response = assistant.generate_answer(prompt)
    return response

def build_prompt_no_rag(question):

    prompt = f"""
    You are a Shakespeare-aware assistant helping a beginner understand the plays.
    Summarize the "text" below briefly.

    Explain clearly in modern English.
    Keep the answer concise and accurate.

Text:
{question}

Answer:
"""
    return prompt

def process_jsonl(assistant, input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f_in, \
         open(output_file, 'w', encoding='utf-8') as f_out:
        
        for line in f_in:
            if not line.strip():
                continue
                
            # Load the JSON object
            data = json.loads(line)
            
            # 1. Get the text to summarize
            event_text = data.get("text", "")
            
            # 2. Get the new summary from LLM
            #print(f"Summarizing chunk: {data.get('chunk_id')}...")
            new_summary = get_llm_summary(assistant, event_text)
            #print(f"AI-generated summary: {new_summary}")
            
            # 3. Replace the old summary
            data["event_summary"] = new_summary
            
            # 4. Write the updated line to the new file
            f_out.write(json.dumps(data) + '\n')


if __name__ == "__main__":

    # model_name = "google/gemma-3-270m-it"   # instruction-tuned version
    #model_name = "google/gemma-3-1b-it"   # instruction-tuned version
    model_name = "google/gemma-3-4b-it"   # instruction-tuned version
    assistant = GemmaAssistant(model_name)
    # Run the process
    process_jsonl(assistant, '/Users/sylas/Coding workspace/CSCI933_ML_A2/data/processed/macbeth_events.jsonl', '/Users/sylas/Coding workspace/CSCI933_ML_A2/data/processed/macbeth_events_aigen_4b.jsonl')
    print("Processing complete!")



