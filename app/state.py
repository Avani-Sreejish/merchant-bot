state = {
    "category": {},
    "merchant": {},
    "customer": {},
    "trigger": {},
    "conversations": {}
}


def store_context(scope, context_id, version, payload):
    if scope not in state:
        return {"accepted": False, "reason": "invalid_scope"}

    existing = state[scope].get(context_id)
    if existing:
        if version < existing["version"]:
            return {"accepted": False, "reason": "stale_version", "current_version": existing["version"]}
        if version == existing["version"]:
            return {"accepted": True, "ack_id": f"ack_{context_id}", "stored_at": existing["delivered_at"]}
    state[scope][context_id] = {
        "context_id": context_id,
        "version": version,
        "payload": payload,
        "delivered_at": "2026-05-02T10:00:00Z"
    }
    return {"accepted": True, "ack_id": f"ack_{context_id}", "stored_at": "2026-05-02T10:00:00Z"}
