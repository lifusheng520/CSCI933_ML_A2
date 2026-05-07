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
  
  
# Event Summary Generation

gemma_models.py
```python
def summarize(self, query, max_new_tokens=150)
```
- For event chunks, generate event summary for retrieval enhancement
- replace event summary in event chunks with Ai-generated content