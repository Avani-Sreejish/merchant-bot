#!/usr/bin/env python3
"""
Merchant Bot Flow Simulator
Demonstrates the complete context-aware flow for MagicPin AI Challenge
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing /v1/healthz...")
    response = requests.get(f"{BASE_URL}/v1/healthz")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_metadata():
    """Test metadata endpoint"""
    print("📋 Testing /v1/metadata...")
    response = requests.get(f"{BASE_URL}/v1/metadata")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def store_contexts():
    """Store trigger, merchant, and category contexts"""
    print("💾 Storing contexts...")

    # Store category context
    category_data = {
        "scope": "category",
        "context_id": "cat_dentist_001",
        "version": 1,
        "payload": {
            "type": "dentist",
            "name": "Dental Practice",
            "specialties": ["cleaning", "fluoride", "preventive_care"]
        }
    }

    response = requests.post(f"{BASE_URL}/v1/context",
                           json=category_data,
                           headers={"Content-Type": "application/json"})
    print(f"Category Context: {response.status_code} - {response.json()}")

    # Store merchant context
    merchant_data = {
        "scope": "merchant",
        "context_id": "merc_dr_meera_001",
        "version": 1,
        "payload": {
            "id": "merc_dr_meera_001",
            "name": "Dr. Meera",
            "business_type": "dentist",
            "category_id": "cat_dentist_001",
            "location": "Mumbai",
            "services": ["cleaning", "fluoride_treatment"],
            "pricing": {"cleaning": 299}
        }
    }

    response = requests.post(f"{BASE_URL}/v1/context",
                           json=merchant_data,
                           headers={"Content-Type": "application/json"})
    print(f"Merchant Context: {response.status_code} - {response.json()}")

    # Store trigger context
    trigger_data = {
        "scope": "trigger",
        "context_id": "trig_research_001",
        "version": 1,
        "payload": {
            "type": "research_digest",
            "merchant_id": "merc_dr_meera_001",
            "category_id": "cat_dentist_001",
            "topic": "fluoride_recall_effectiveness",
            "priority": "high"
        }
    }

    response = requests.post(f"{BASE_URL}/v1/context",
                           json=trigger_data,
                           headers={"Content-Type": "application/json"})
    print(f"Trigger Context: {response.status_code} - {response.json()}")
    print()

def test_tick():
    """Test tick endpoint to generate actions"""
    print("🎯 Testing /v1/tick...")
    response = requests.post(f"{BASE_URL}/v1/tick")
    print(f"Status: {response.status_code}")
    actions = response.json().get("actions", [])
    print(f"Generated {len(actions)} action(s)")

    for i, action in enumerate(actions, 1):
        print(f"\nAction {i}:")
        print(f"  Template: {action.get('template_name')}")
        print(f"  Body: {action.get('body')}")
        print(f"  Rationale: {action.get('rationale')}")
    print()

def test_reply_accept():
    """Test accepting the action"""
    print("✅ Testing /v1/reply with acceptance...")
    reply_data = {
        "conversation_id": "conv_trig_research_001",
        "reply_text": "Yes, go ahead with that"
    }

    response = requests.post(f"{BASE_URL}/v1/reply",
                           json=reply_data,
                           headers={"Content-Type": "application/json"})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_reply_decline():
    """Test declining the action"""
    print("❌ Testing /v1/reply with decline...")
    reply_data = {
        "conversation_id": "conv_trig_research_001",
        "reply_text": "No, not right now"
    }

    response = requests.post(f"{BASE_URL}/v1/reply",
                           json=reply_data,
                           headers={"Content-Type": "application/json"})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_complete_flow():
    """Run the complete flow demonstration"""
    print("🚀 Starting Complete Flow Demonstration")
    print("=" * 50)

    # Reset state by restarting (in real deployment, you'd have proper state management)
    print("Note: For clean testing, restart the server between runs")
    print()

    test_health()
    test_metadata()
    store_contexts()
    test_tick()
    test_reply_accept()
    test_reply_decline()

    print("✨ Flow demonstration complete!")
    print("\nKey Features Demonstrated:")
    print("• Multi-context storage (trigger + merchant + category)")
    print("• Personalized action generation")
    print("• Sophisticated reply processing")
    print("• Context-aware responses")

if __name__ == "__main__":
    test_complete_flow()