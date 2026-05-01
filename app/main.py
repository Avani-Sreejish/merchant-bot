from fastapi import FastAPI
from app.state import store_context, state
from app.composer import decide_action
from app.schemas import ContextRequest, ReplyRequest

app = FastAPI()

@app.post("/v1/context")
def context(req: ContextRequest):
    return store_context(req.scope, req.context_id, req.version, req.payload)

@app.post("/v1/tick")
def tick():
    actions = decide_action(state)
    return {"actions": actions}

@app.post("/v1/reply")
def reply(req: ReplyRequest):
    """
    Process merchant replies with improved logic.
    Handles various response patterns and provides contextual actions.
    """
    text = req.reply_text.lower().strip()

    # Positive responses
    if any(word in text for word in ["yes", "go ahead", "sure", "okay", "ok", "please", "do it"]):
        return {
            "action": "send",
            "body": "Sending now — I also drafted a follow-up version you can reuse.",
            "cta": "open_ended",
            "rationale": "Merchant approved the action"
        }

    # Negative responses
    elif any(word in text for word in ["no", "stop", "cancel", "don't", "never"]):
        return {
            "action": "cancel",
            "body": "Understood, I've cancelled that action. Let me know if you'd like to try something else.",
            "cta": "open_ended",
            "rationale": "Merchant declined the action"
        }

    # Delay requests
    elif any(word in text for word in ["later", "wait", "tomorrow", "next week", "hold"]):
        return {
            "action": "wait",
            "body": "I'll hold off for now. Should I remind you later or would you prefer a different approach?",
            "cta": "open_ended",
            "rationale": "Merchant requested to delay"
        }

    # Questions or clarifications
    elif any(word in text for word in ["?", "how", "what", "when", "why", "explain"]):
        return {
            "action": "clarify",
            "body": "I'd be happy to explain further. What specific aspect would you like me to clarify?",
            "cta": "open_ended",
            "rationale": "Merchant asked for clarification"
        }

    # Modification requests
    elif any(word in text for word in ["change", "modify", "different", "instead", "better"]):
        return {
            "action": "modify",
            "body": "I can modify the approach. What changes would you like me to make?",
            "cta": "open_ended",
            "rationale": "Merchant wants modifications"
        }

    # Default: end conversation
    else:
        return {
            "action": "end",
            "body": "Thanks for your response. If you need anything else, feel free to reach out.",
            "cta": "closed",
            "rationale": "Unable to determine merchant intent"
        }

@app.get("/v1/healthz")
def healthz():
    return {
        "status": "ok",
        "uptime_seconds": 3600,
        "contexts_loaded": {k: len(v) for k,v in state.items()}
    }

@app.get("/v1/metadata")
def metadata():
    return {
        "team_name": "MerchantBot Team",
        "team_members": ["AI Assistant"],
        "model": "context-aware rule-based composer",
        "approach": "Multi-context flow: trigger + merchant + category personalization",
        "contact_email": "team@merchantbot.com",
        "version": "1.0.0",
        "submitted_at": "2026-05-02T00:00:00Z"
    }
