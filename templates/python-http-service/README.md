# Python HTTP Service Template

Standalone microservice — run beside or behind UtahMosphere kernel.

```bash
PORT=8080 python handler.py
curl http://127.0.0.1:8080/health
```

Deploy to UtahMosphere as a tenant, then proxy via UtahX manifests.
