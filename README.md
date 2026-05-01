# Merchant Bot - MagicPin AI Challenge

A context-aware AI bot that handles merchant interactions through a sophisticated multi-context flow.

## Features

- **Multi-Context Processing**: Handles trigger, merchant, and category contexts
- **Personalized Actions**: Generates tailored responses based on business type and merchant data
- **Sophisticated Reply Processing**: Understands various merchant responses (accept, decline, delay, clarify)
- **Deterministic Flow**: Reliable, predictable behavior for production use

## API Endpoints

All endpoints are available at your public URL:

### POST /v1/context
Store context data (trigger, merchant, category)
```json
{
  "scope": "trigger|merchant|category",
  "context_id": "unique_id",
  "version": 1,
  "payload": { ... }
}
```

### POST /v1/tick
Generate actions based on stored contexts
```json
{
  "actions": [
    {
      "conversation_id": "...",
      "merchant_id": "...",
      "template_name": "...",
      "body": "...",
      "rationale": "..."
    }
  ]
}
```

### POST /v1/reply
Process merchant responses
```json
{
  "conversation_id": "...",
  "reply_text": "..."
}
```

### GET /v1/healthz
Health check with context counts
```json
{
  "status": "ok",
  "uptime_seconds": 3600,
  "contexts_loaded": { ... }
}
```

### GET /v1/metadata
Team and model information
```json
{
  "team_name": "MerchantBot Team",
  "model": "context-aware rule-based composer",
  "approach": "Multi-context flow: trigger + merchant + category personalization"
}
```

## Flow Example

1. **Store Category Context**: Business type information
2. **Store Merchant Context**: Merchant profile and preferences
3. **Store Trigger Context**: Action trigger with merchant/category links
4. **Call Tick**: Generate personalized action
5. **Process Reply**: Handle merchant response appropriately

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload

# Test with simulator
python flow_simulator.py
```

## Deployment

For the MagicPin AI Challenge, deploy to a service that provides a public HTTPS URL:

- **Railway**: `railway deploy`
- **Render**: Connect GitHub repo
- **Fly.io**: `fly deploy`
- **Heroku**: `git push heroku main`
- **Vercel**: For serverless (may need adapter)

Ensure your deployment exposes these exact endpoints at the root path.

## Testing

Run the included simulator:
```bash
python flow_simulator.py
```

This demonstrates the complete flow with realistic data.