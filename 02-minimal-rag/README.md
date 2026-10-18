# 02 — Minimal RAG Pipeline (Chapter 13)

The smallest honest retrieval-augmented generation loop: chunk, embed, retrieve,
rerank, synthesize — all in one file. Uses a term-frequency embedding so it runs
offline; swap `embed()` and `generate()` for real models in production.

## Run

```bash
python demo.py   # stdlib only
```

## What to notice

- Retrieval finds *related* passages, including a superseded 2014 policy —
  watch the citation step; stale-document hygiene decides whether this is a
  feature or a bug.
- The generator is a stand-in; the point is the pipeline contract, not the
  model.

## Book reference

See *AI Inflection*, Chapter 13, "Why LLMs Need Memory (RAG)."
