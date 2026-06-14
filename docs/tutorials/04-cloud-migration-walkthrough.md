# Tutorial: Cloud Migration Walkthrough

**Audience:** AWS, GCP, and Azure developers and platform owners  
**Time:** 60 minutes  
**Goal:** Map existing cloud workloads to UtahMosphere and run a working pilot

---

## Before You Start

Read the [Capability Matrix](../CAPABILITY_MATRIX.md). Not all cloud-parity APIs are implemented in v25.0. This tutorial focuses on **what works today** and **how to prepare** for full parity.

---

## Migration Map

| Cloud Service | UtahMosphere Target | v25.0 Status |
|---------------|---------------------|--------------|
| AWS S3 | Utah S3 Mesh | Planned (endpoint docs ready) |
| AWS Lambda | Utah Lambda / ContainerEngine | Handler stubs on deploy |
| AWS RDS | Utah RDS Ledger | Planned |
| App Engine / Web Apps | Voice/API deploy | **Implemented** via `/command` |
| API Gateway | UtahX + kernel `:8999` | Partial |

---

## Step 1: Inventory Your App

List dependencies:

```
[ ] Object storage (S3/GCS)
[ ] Serverless functions
[ ] SQL / NoSQL database
[ ] Container / VM hosting
[ ] Auth (IAM/OAuth)
```

Mark each as **migrate now**, **hybrid**, or **stay on cloud** using the matrix.

---

## Step 2: Stand Up UtahMosphere

```bash
export UTAH_DATA_DIR="$(pwd)/.utah-data"
python utahmosphere_os.py
```

---

## Step 3: Migrate Compute First (Works Today)

**Cloud pattern:** Lambda function or Cloud Run service

**UtahMosphere pattern:** Deploy a container handler

```bash
python examples/voice-deploy-simulator/deploy.py my-function
```

Copy your handler logic into:

```
.utah-data/containers/my-function/handler.py
```

Template:

```python
def handler(event, context):
    name = event.get("name", "World")
    return {"message": f"Hello {name} from UtahMosphere!"}
```

Use the [container-handler template](../../templates/container-handler/).

---

## Step 4: Test HTTP Access + Monetization

```bash
python examples/paid-app-access/access_app.py my-function
```

Maps to cloud API Gateway + usage billing patterns.

---

## Step 5: Prepare S3 Migration (When API Ships)

Keep this boto3 pattern ready — change only `endpoint_url`:

```python
import boto3

s3 = boto3.client(
    "s3",
    endpoint_url="http://utahmosphere.local:8999",
    aws_access_key_id="YOUR_TENANT_ID",
    aws_secret_access_key="YOUR_HMAC_SIG",
)
```

Signature recipe: [Backend Recipes](../recipes/backend-recipes.md)

---

## Step 6: Prepare RDS Migration (When API Ships)

```bash
# Future endpoints — documented for parity
curl -X POST http://127.0.0.1:8999/rds/write \
  -H "Content-Type: application/json" \
  -d '{"key": "user:123", "value": {"name": "Alice"}}'
```

Until then, use local JSON in `secure_registry.json` or external DB with UtahMosphere as compute-only.

---

## Step 7: Hybrid Cutover

Recommended 4-phase plan:

1. **Phase 1:** Deploy stateless APIs to UtahMosphere; keep DB on cloud
2. **Phase 2:** Move high-egress storage to mesh when S3 API lands
3. **Phase 3:** Migrate session/state to RDS ledger API
4. **Phase 4:** Decommission redundant cloud compute

---

## Migration Checklist

- [ ] UtahMosphere pilot node healthy
- [ ] Compute workloads deployed via `/command`
- [ ] HMAC secrets generated for future storage APIs
- [ ] DNS/ingress plan for `:8999`
- [ ] Rollback plan documented
- [ ] Team trained on [API Reference](../API_REFERENCE.md)

More recipes: [Migration Recipes](../recipes/migration-recipes.md)  
Full guide: [Cloud Parity Migration](../CLOUD_PARITY_MIGRATION.md)
