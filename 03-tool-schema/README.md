# 03 — Guarded Tool Schema (Chapter 14)

The production contract for tool-using AI: the model proposes a structured
call; the platform validates parameters, checks permissions, gates
irreversible actions behind human confirmation, audits everything, and only
then executes.

## Run

```bash
python demo.py   # stdlib only
```

## What to notice

- `refund_order` is held for human confirmation; `lookup_order` runs freely
- Every call is written to `AUDIT` before execution
- Refunding with the wrong amount fails validation *after* confirmation, which
  is the point: guards stack, and each layer has a separate job.

## Book reference

See *AI Inflection*, Chapter 14, "From Words to Actions (Tool Use)."
