# Minimal API — Starter Project

Smallest forkable API workload for UtahMosphere.

## Local test

```bash
python handler_service.py
curl http://127.0.0.1:8080/health
curl http://127.0.0.1:8080/hello
```

## Deploy to UtahMosphere

```bash
python ../../examples/voice-deploy-simulator/deploy.py minimal-api
cp handler.py ../../.utah-data/containers/minimal-api/handler.py
```

Tutorial: [Your First App](../../docs/tutorials/05-developer-first-app.md)
