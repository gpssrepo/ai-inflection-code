"""
Chapter 13 — A minimal, honest RAG pipeline (stdlib only, no external APIs).

The book's RAG recipe shrunk to the smallest runnable form:
    1. index documents into chunks (with overlap)
    2. embed chunks (here: a toy term-frequency embedding, so no API key needed)
    3. retrieve top-k by cosine similarity
    4. generate answer text citing chunk ids

In production you'd swap embed() for a real embedding model and generate()
for an LLM call. The structure, and its failure modes, are identical.

Run: python demo.py
"""
import math
import re
from collections import Counter

# --- 1. A toy corpus standing in for your intranet --------------------------
DOCS = [
    {"id": "policy-2019", "title": "Travel Policy (2019)",
     "text": "Employees may claim economy-class airfare for domestic travel. "
             "Business class requires VP approval. Meal allowance is 40 dollars per day."},
    {"id": "policy-2024", "title": "Travel Policy (2024)",
     "text": "Employees may claim premium-economy airfare for flights over 6 hours. "
             "Meal allowance is 55 dollars per day. Business class requires CFO approval."},
    {"id": "policy-archived", "title": "Travel Policy (archived 2014)",
     "text": "Meal allowance is 25 dollars per day. This policy is superseded."},
]

def chunk(text: str, size: int = 40, overlap: int = 10):
    """Split text into word windows with overlap so sentences don't split."""
    words = text.split()
    for i in range(0, len(words), size - overlap):
        yield " ".join(words[i:i + size])

# --- 2. Toy embedding: normalized term-frequency vector ---------------------
VOCAB = {}
def embed(text: str) -> dict:
    counts = Counter(re.findall(r"[a-z']+", text.lower()))
    for term in counts:
        VOCAB.setdefault(term, len(VOCAB))
    total = math.sqrt(sum(v * v for v in counts.values())) or 1.0
    return {VOCAB[t]: c / total for t, c in counts.items()}

def cosine(a: dict, b: dict) -> float:
    common = set(a) & set(b)
    return sum(a[t] * b[t] for t in common)

# --- 3. Retrieval ------------------------------------------------------------
class Store:
    def __init__(self):
        self.rows = []
    def add(self, doc_id, title, text):
        for j, ch in enumerate(chunk(text)):
            self.rows.append({"cid": f"{doc_id}#{j}", "title": title,
                              "text": ch, "vec": embed(ch)})
    def search(self, query: str, k: int = 2):
        qv = embed(query)
        return sorted(self.rows, key=lambda r: cosine(qv, r["vec"]), reverse=True)[:k]

def rerank(query: str, hits):
    """Placeholder for a cross-encoder reranker in production."""
    return hits

# --- 4. Generation (rule-based stand-in for the LLM synthesis step) ---------
def generate(question: str, hits):
    evidence = "\n".join(f"  [{i+1}] ({h['cid']}) {h['text']}" for i, h in enumerate(hits))
    return (f"Q: {question}\n"
            f"A: Based on the retrieved policy passages, here is the grounded answer.\n"
            f"   Evidence:\n{evidence}\n"
            f"   Answer: Check the citations: a retrieval pipeline finds related policies, "
            f"including superseded ones. In production you'd rerank by date and "
            f"filter archives so [1] is the current policy, not the 2014 one.")

if __name__ == "__main__":
    store = Store()
    for d in DOCS:
        store.add(d["id"], d["title"], d["text"])

    hits = store.search("What is the daily meal allowance?")
    hits = rerank("What is the daily meal allowance?", hits)
    print(generate("What is the daily meal allowance?", hits))

    print("\n--- The 2014 archived policy is also retrievable: watch your hygiene. ---")
    for h in store.search("old travel meal policy"):
        print(" ", h["cid"], "->", h["text"][:60], "...")
