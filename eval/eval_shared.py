"""eval/eval_shared.py — shared abstention-detection primitives.

Single source of truth for ABSTENTION_PHRASE and state derivation.
Imported by faithfulness.py and analyze_phase1.py.
"""

ABSTENTION_PHRASE = "No puedo responder con la documentación proporcionada."


def compute_state(response: str) -> str:
    """Deterministic state from response string (no stored field needed)."""
    if response.startswith("[GENERATION ERROR:"):
        return "error"
    if response.strip() == ABSTENTION_PHRASE:
        return "abstained"
    return "answered"


def is_pure_abstention(r: dict) -> bool:
    """True iff the generator emitted the exact abstention phrase."""
    return compute_state(r["response"]) == "abstained"


def is_error(r: dict) -> bool:
    """True iff the generation failed (works without stored 'state' field)."""
    return compute_state(r["response"]) == "error"
