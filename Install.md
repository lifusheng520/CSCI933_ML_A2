# 1 Install

Python 3.12.11

```
conda create -n 933_rag python=3.12.11

conda activate 933_rag

pip install -r requirements.txt
```

# 2 Models

## Embedding Models
- Indexing and Retrieval: sentence-transformers/all-MiniLM-L6-v2

## SLM Candidates
- baseline.py  distilgpt2
- slm_models.py TinyLLaMa, Phi-2
- gemma_models.py Google Gemma
  - google/gemma-3-270m-it 270M 
  - google/gemma-3-1b-it 1B perfect
  - google/gemma-3-4b-it 4B too slow on cpu


# 3 RAG Pipeline Test

## Test Entrance:

rag_test.py

## Model Selection

Mainly tested on gemma models from tiny to large models: 
```python
model_name = "google/gemma-3-270m-it"   # instruction-tuned version
model_name = "google/gemma-3-1b-it"   # instruction-tuned version
model_name = "google/gemma-3-4b-it"   # instruction-tuned version
```

## Data Chunking

**Chunk type** - aggregate text in raw data from coarse-grained to fine-grained:

- 'scenes'
- 'event'
- 'utterance'

Maybe 'event' is a better choice and I'm generating event summary for MacBeth by GenAI.


## Indexing

retireval.py

```python 
def build_index(self, chunks: List[Chunk]) -> None
```

- Read lines in chunk jsonl, embed them and create indices using FAISS vectordb.
- Indexing using play, scene_summary, keywords
- Plan to add event_summary. It could be quite helpful.


## Retrieval 

retireval.py
```python
def retrieve(self, query: str, top_k: int = 3) -> List[Tuple[Chunk, float]]:
```
- retrieve top-k related chunk indices by query using Cosine Similarity
- Plan to enhance this retrieval, perhaps re-ranking

## Answer Generation

gemma_models.py

```python
def generate_answer(self, query, max_new_tokens=150)
```
- generate answers by retrieved chunks and question
  
  
# 4 Event Summary Generation

gemma_models.py
```python
def summarize(self, query, max_new_tokens=150)
```
- For event chunks, generate event summary for retrieval enhancement
- replace event summary in event chunks with Ai-generated content

# 5 Tips for Downloading Gemma Models

In order to use pretrained models, Google Gemma require users to login huggingface and get access granted first. 


**Steps**

1. Make sure that transformers library has already been installed in conda environment. If not,
  ```
    pip install transformers
  ```
2. Login huggingface to get granted for a model, e.g. gemma-3-1b-it
    https://huggingface.co/google/gemma-3-1b-it
3. Create a token: https://huggingface.co/settings/tokens. Copy and save it in notebook since it's not visible after created.
4. On the page above, edit the permission of the token, and toggle this permission - "Read access to contents of all public gated repos you can access" and save.
5. Activate conda environment e.g. "933_rag": conda activate 933_rag
6. Login huggingface, then paste the token when prompted. The token is not visible.
  ```
    hf auth login
  ```
7. Run rag_test.py, gemma model will be downloaded automatically for the first time.