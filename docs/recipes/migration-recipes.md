# Migration Recipes

Cloud parity patterns for AWS, GCP, and Azure workloads.

> **Note:** S3, Lambda invoke, and RDS HTTP routes are documented for parity but not fully implemented in v25.0. See [Capability Matrix](../CAPABILITY_MATRIX.md).

---

## AWS S3 → Utah S3 Mesh

**Status:** Roadmap (endpoint pattern ready)

```python
import boto3

s3 = boto3.client(
    "s3",
    endpoint_url="http://utahmosphere.local:8999",
    aws_access_key_id="YOUR_TENANT_ID",
    aws_secret_access_key="YOUR_HMAC_SIG",
)
s3.put_object(Bucket="my-data", Key="file.txt", Body=b"Hello")
```

---

## AWS Lambda → Utah ContainerEngine

**Status:** Deploy works today; HTTP invoke endpoint roadmap

**Step 1 — Deploy:**

```bash
python examples/voice-deploy-simulator/deploy.py my-function
```

**Step 2 — Handler (future invoke target):**

```python
def handler(event, context):
    name = event.get("name", "World")
    return {"message": f"Hello {name} from UtahMosphere!"}
```

**Future invoke:**

```bash
curl -X POST http://utahmosphere.local:8999/lambda/my-function/invoke \
  -H "Content-Type: application/json" \
  -d '{"name": "General 23"}'
```

Template: [container-handler](../../templates/container-handler/)

---

## AWS RDS → Utah RDS Ledger

**Status:** Roadmap

```bash
# Write
curl -X POST http://utahmosphere.local:8999/rds/write \
  -H "Content-Type: application/json" \
  -d '{"key": "user:123", "value": {"name": "Alice", "score": 9000}}'

# Read
curl http://utahmosphere.local:8999/rds/read/user:123
```

**Interim:** Keep cloud RDS; point UtahMosphere compute at existing DB connection string.

---

## GCP App Engine → Utah Workloads

**Status:** Implemented via `/command`

```bash
curl -X POST http://127.0.0.1:8999/command \
  -H "Content-Type: application/json" \
  -d '{"transcript":"deploy application my-website","acoustic_hash":"0"}'
```

Future: git-based deploy voice command (roadmap).

---

## Azure Web Apps → Utah Workloads

Same as GCP — deploy via API/voice, place Azure Front Door or App Gateway in front during hybrid phase.

---

## Recipe: Migration Checklist

```markdown
- [ ] UtahMosphere node healthy (/health)
- [ ] Capability matrix reviewed with team
- [ ] Stateless APIs deployed to UtahMosphere
- [ ] HMAC secrets generated for future storage
- [ ] DNS points to UtahMosphere ingress
- [ ] Rollback runbook written
- [ ] Cloud resources tagged for decommission phase
```

---

## Recipe: Endpoint URL Find-Replace

| SDK | Change |
|-----|--------|
| boto3 S3 | `endpoint_url='http://HOST:8999'` |
| AWS CLI | `--endpoint-url http://HOST:8999` |
| Custom HTTP | Base URL → `http://HOST:8999` |

Full guide: [Cloud Parity Migration](../CLOUD_PARITY_MIGRATION.md)
