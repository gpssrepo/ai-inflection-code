"""
Chapter 14 — the guarded tool-schema pattern.

Shows the production contract this book describes: the model proposes a
structured call; the platform validates, scopes, audits, and only then
executes. Everything here runs offline with stub data.

Run: python demo.py
"""
import json
import time

# ---- the tool registry (business-level names, not raw SDK endpoints) -------
TOOLS = {
    "refund_order": {
        "description": "Refunds an order. Irreversible: requires human confirmation.",
        "irreversible": True,
        "params": {
            "order_id": {"type": "string", "required": True},
            "amount":   {"type": "number", "required": True},
            "reason":   {"type": "string", "required": True},
        },
    },
    "lookup_order": {
        "description": "Read-only: fetch an order by id.",
        "irreversible": False,
        "params": {"order_id": {"type": "string", "required": True}},
    },
}

ORDERS = {"ord_1001": {"amount": 150.00, "status": "settled"},
          "ord_1002": {"amount": 89.25,  "status": "settled"}}

AUDIT = []

def validate(call: dict) -> dict:
    """Reject bad tool calls before anything touches a system of record."""
    tool = TOOLS.get(call.get("tool"))
    if tool is None:
        return {"ok": False, "error": "unknown tool"}
    args = call.get("args", {})
    for name, spec in tool["params"].items():
        if spec.get("required") and name not in args:
            return {"ok": False, "error": f"missing required parameter: {name}"}
    return {"ok": True}

def execute(call: dict, confirmed: bool = False) -> dict:
    """The program disposes: permissions, gates, audit, then the action."""
    v = validate(call)
    if not v["ok"]:
        AUDIT.append({**call, "outcome": "rejected", "reason": v["error"]})
        return v
    tool = TOOLS[call["tool"]]
    if tool["irreversible"] and not confirmed:
        AUDIT.append({**call, "outcome": "held_for_review"})
        return {"ok": False, "error": "irreversible action requires human confirmation"}
    # --- the action itself ---
    if call["tool"] == "lookup_order":
        order = ORDERS.get(call["args"]["order_id"])
        result = {"ok": True, "result": order or {"error": "not found"}}
    elif call["tool"] == "refund_order":
        o = ORDERS.get(call["args"]["order_id"])
        if not o or abs(o["amount"] - call["args"]["amount"]) > 1e-9:
            result = {"ok": False, "error": "amount must equal charged amount"}
        else:
            o["status"] = "refunded"
            result = {"ok": True, "result": {"refunded": call["args"]["amount"]}}
    AUDIT.append({**call, "outcome": "executed" if result["ok"] else "failed",
                  "ts": time.time()})
    return result

if __name__ == "__main__":
    # 1. a read-only flow works freely
    print(execute({"tool": "lookup_order", "args": {"order_id": "ord_1001"}}))

    # 2. the refund is held until a human confirms
    print(execute({"tool": "refund_order",
                   "args": {"order_id": "ord_1001", "amount": 150.0,
                            "reason": "duplicate charge"}}))

    # 3. confirmed, it executes
    print(execute({"tool": "refund_order",
                   "args": {"order_id": "ord_1001", "amount": 150.0,
                            "reason": "duplicate charge"}},
                  confirmed=True))

    # 4. a bad amount fails validation-on-execution
    print(execute({"tool": "refund_order",
                   "args": {"order_id": "ord_1002", "amount": 1.0,
                            "reason": "test"}},
                  confirmed=True))

    print("\nAudit trail:")
    print(json.dumps(AUDIT, indent=2))
