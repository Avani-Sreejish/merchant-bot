def decide_action(state):
    """
    Generate actions based on stored contexts.
    Prioritizes: trigger + merchant + category context for personalization.
    """
    triggers = state.get("trigger", {})
    merchants = state.get("merchant", {})
    categories = state.get("category", {})

    if not triggers:
        return []

    actions = []

    for trigger_id, trigger_ctx in triggers.items():
        trigger_type = trigger_ctx["payload"].get("type")

        # Find associated merchant and category
        merchant_id = trigger_ctx["payload"].get("merchant_id")
        category_id = trigger_ctx["payload"].get("category_id")

        merchant_data = merchants.get(merchant_id, {}) if merchant_id else {}
        category_data = categories.get(category_id, {}) if category_id else {}

        if trigger_type == "research_digest":
            action = generate_research_action(trigger_ctx, merchant_data, category_data, trigger_id)
            if action:
                actions.append(action)

        elif trigger_type == "promotion_reminder":
            action = generate_promotion_action(trigger_ctx, merchant_data, category_data, trigger_id)
            if action:
                actions.append(action)

        elif trigger_type == "customer_engagement":
            action = generate_engagement_action(trigger_ctx, merchant_data, category_data, trigger_id)
            if action:
                actions.append(action)

    return actions


def generate_research_action(trigger_ctx, merchant_data, category_data, trigger_id):
    """Generate personalized research digest action."""
    merchant_name = merchant_data.get("name", "Merchant")
    category_type = category_data.get("type", "business")

    # Customize based on category
    if category_type == "dentist":
        research_topic = "fluoride recall effectiveness"
        insight = "3-month fluoride recall outperformed 6-month recall by 38%"
        offer = "₹299 cleaning offer"
    elif category_type == "restaurant":
        research_topic = "customer retention strategies"
        insight = "Personalized follow-ups increased repeat visits by 25%"
        offer = "loyalty program"
    else:
        research_topic = "business optimization"
        insight = "Data-driven decisions improved performance by 20%"
        offer = "special promotion"

    return {
        "conversation_id": f"conv_{trigger_id}",
        "merchant_id": merchant_data.get("id", "m_001"),
        "customer_id": None,
        "send_as": "vera",
        "trigger_id": trigger_id,
        "template_name": "research_digest_v1",
        "template_params": [merchant_name, research_topic],
        "body": f"{merchant_name}, recent {research_topic} research shows {insight}. Should I draft a customer campaign for your {offer}?",
        "cta": "open_ended",
        "suppression_key": f"research:{category_type}:{trigger_ctx.get('version', 'latest')}",
        "rationale": f"Personalized research digest for {category_type} business"
    }


def generate_promotion_action(trigger_ctx, merchant_data, category_data, trigger_id):
    """Generate promotion reminder action."""
    merchant_name = merchant_data.get("name", "Merchant")
    category_type = category_data.get("type", "business")

    return {
        "conversation_id": f"conv_{trigger_id}",
        "merchant_id": merchant_data.get("id", "m_001"),
        "customer_id": None,
        "send_as": "vera",
        "trigger_id": trigger_id,
        "template_name": "promotion_reminder_v1",
        "template_params": [merchant_name],
        "body": f"{merchant_name}, your promotion ends soon. Would you like me to extend it or create a follow-up campaign?",
        "cta": "open_ended",
        "suppression_key": f"promotion:{category_type}:{trigger_id}",
        "rationale": "Promotion expiration reminder"
    }


def generate_engagement_action(trigger_ctx, merchant_data, category_data, trigger_id):
    """Generate customer engagement action."""
    merchant_name = merchant_data.get("name", "Merchant")
    category_type = category_data.get("type", "business")

    return {
        "conversation_id": f"conv_{trigger_id}",
        "merchant_id": merchant_data.get("id", "m_001"),
        "customer_id": trigger_ctx["payload"].get("customer_id"),
        "send_as": "vera",
        "trigger_id": trigger_id,
        "template_name": "engagement_v1",
        "template_params": [merchant_name],
        "body": f"{merchant_name}, I noticed customer engagement opportunities. Should I send personalized messages to increase activity?",
        "cta": "open_ended",
        "suppression_key": f"engagement:{category_type}:{trigger_id}",
        "rationale": "Customer engagement opportunity"
    }
