"""
Chapter 10 — BPE tokenization demonstration.

Shows how a model tokenizer slices everyday text, including the
contraction example from the book: "didn't" is not one token.

Run:
    pip install tiktoken
    python demo.py
"""
import tiktoken

# cl100k_base is the vocabulary used by GPT-4-class OpenAI models.
enc = tiktoken.get_encoding("cl100k_base")

def inspect(text: str) -> None:
    ids = enc.encode(text)
    pieces = [enc.decode([i]) for i in ids]
    print(f"  text:    {text!r}")
    print(f"  ids:     {ids}")
    print(f"  pieces:  {pieces}")
    print(f"  tokens:  {len(ids)}\n")

if __name__ == "__main__":
    inspect("The animal didn't cross the street because it was too tired")
    inspect("didn't")   # contraction: 'didn' + ''t' — two tokens
    inspect("unbelievable")
    inspect("Kaizala")  # a rarer word splits into smaller pieces
    inspect("宽度")     # non-ASCII scripts often spread over more tokens
    inspect("one hundred million")  # common phrasing merges efficiently
