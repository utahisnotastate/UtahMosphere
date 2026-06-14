def handler(event, context):
    """Minimal API workload for UtahMosphere ContainerEngine."""
    route = event.get("path", "/")
    if route == "/health":
        return {"status": "ok"}
    if route == "/hello":
        name = event.get("name", "World")
        return {"message": f"Hello, {name}!"}
    return {"status": "active", "routes": ["/health", "/hello"]}
