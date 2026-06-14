def handler(event, context):
    """
    UtahContainerEngine handler entry point.
    Called when the container is invoked (future Lambda-style API).
    """
    return {
        "status": "active",
        "message": "Handler ready",
        "event": event,
    }
