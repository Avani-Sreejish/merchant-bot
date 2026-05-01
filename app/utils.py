from typing import Any, Dict


def normalize_text(text: str) -> str:
    return text.strip().lower()


def format_response(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"status": "success", "data": payload}
