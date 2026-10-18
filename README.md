# AI Inflection — Companion Code

Executable examples from the book **AI Inflection** by Ganesh Sundaram.

| Example | Chapter | What it shows |
|---------|---------|---------------|
| `01-bpe-tokenization/` | 10 | How models actually see text — byte-pair encoding in practice |
| `02-minimal-rag/` | 13 | The smallest honest retrieval-augmented generation pipeline |
| `03-tool-schema/` | 14 | The guarded tool-schema pattern used in production tool use |

## Quick start

```bash
pip install -r requirements.txt   # tiktoken only; the rest use only stdlib
python 01-bpe-tokenization/demo.py
python 02-minimal-rag/demo.py
python 03-tool-schema/demo.py
```

## Repository layout

```
01-bpe-tokenization/   # tokenization demo from Chapter 10
02-minimal-rag/        # tiny runnable RAG loop from Chapter 13
03-tool-schema/        # guarded tool schema demo from Chapter 14
diagrams/              # figure source SVGs referenced in the book
```

## License

MIT. Code is illustrative; use freely in learning and prototypes.
