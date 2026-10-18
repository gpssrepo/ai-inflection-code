# 01 — BPE Tokenization Demo (Chapter 10)

Shows what a model actually sees when you write "didn't": not one indivisible word
but subword slices (`didn` + `'t`), and how everyday sentence punctuation and
languages price differently in tokens.

## Run

```bash
pip install tiktoken
python demo.py
```

## What to notice

- `didn't` splits into two tokens, not three
- Multi-byte scripts (Chinese, Tamil) spend more tokens per character
- This is why long multilingual prompts cost more than they look

## Book reference

See *AI Inflection*, Chapter 10, "Tokenization: turning text into numbers."
