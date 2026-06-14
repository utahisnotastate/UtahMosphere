def handler(event, context):
    """Paid-access app pattern — access gated at /app/{name} by Utah-Tycoon."""
    client_id = event.get("client_id", "anonymous")
    return {
        "status": "premium_content_unlocked",
        "client_id": client_id,
        "content": "Thank you for supporting this sovereign node.",
    }
