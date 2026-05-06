"""baseline prompt
"""
def build_prompt(user_input):
    prompt = f"""
    You are a helpful assistant.
    Do not make up facts. If unsure, answer generally.
    Question: {user_input}
    Answer:
    """
    return prompt.strip()
