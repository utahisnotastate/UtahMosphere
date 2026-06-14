### ☁️ Cloud Parity & Migration Guide

UtahMosphere OS targets drop-in replacement gateways for major enterprise cloud services. Migration is often as simple as changing an `endpoint_url` — **once the parity API is implemented**.

> **Important:** See [Capability Matrix](CAPABILITY_MATRIX.md) for v25.0 implementation status. Compute deploy via `/command` works today; S3/Lambda invoke/RDS HTTP routes are documented patterns for upcoming releases.

**Tutorial:** [Cloud Migration Walkthrough](tutorials/04-cloud-migration-walkthrough.md)  
**Recipes:** [Migration Recipes](recipes/migration-recipes.md)

---

#### **1. AWS S3 ↔ Utah S3 Mesh**

**Status:** Roadmap

**Legacy AWS Code:**
```python
import boto3
s3 = boto3.client('s3')
s3.put_object(Bucket='my-data', Key='file.txt', Body='Hello')
```

**UtahMosphere Migration:**
```python
import boto3
s3 = boto3.client(
    's3', 
    endpoint_url='http://utahmosphere.local:8999',
    aws_access_key_id='YOUR_TENANT_ID',
    aws_secret_access_key='YOUR_HMAC_SIG'
)
s3.put_object(Bucket='my-data', Key='file.txt', Body='Hello')
```

---

#### **2. AWS Lambda / GCP Functions ↔ Utah Lambda**

**Status:** Deploy implemented; HTTP invoke endpoint roadmap

**Registration:** Deploy via voice or `/command` — creates `containers/{fn}/handler.py`

```python
def handler(event, context):
    name = event.get('name', 'World')
    return {"message": f"Hello {name} from UtahMosphere!"}
```

**Future invocation:**
```bash
curl -X POST http://utahmosphere.local:8999/lambda/my-function/invoke \
     -H "Content-Type: application/json" \
     -d '{"name": "General 23"}'
```

**Works today:**
```bash
python examples/voice-deploy-simulator/deploy.py my-function
```

---

#### **3. AWS RDS / GCP Cloud SQL ↔ Utah RDS Ledger**

**Status:** Roadmap

```bash
curl -X POST http://utahmosphere.local:8999/rds/write \
     -H "Content-Type: application/json" \
     -d '{"key": "user:123", "value": {"name": "Alice", "score": 9000}}'

curl http://utahmosphere.local:8999/rds/read/user:123
```

**Interim:** UtahMosphere compute + existing cloud database.

---

#### **4. GCP App Engine / Azure Web Apps ↔ Utah Workloads**

**Status:** Implemented via `/command`

**Voice:** "Deploy application my-website"  
**API:**
```bash
curl -X POST http://127.0.0.1:8999/command \
  -H "Content-Type: application/json" \
  -d '{"transcript":"deploy application my-website","acoustic_hash":"0"}'
```

Git-based deploy: roadmap.

---

#### **Migration Checklist**

1. [ ] Install UtahMosphere Core via `setup.sh` or [Local Development](LOCAL_DEVELOPMENT.md)
2. [ ] Review [Capability Matrix](CAPABILITY_MATRIX.md) with your team
3. [ ] Deploy stateless APIs to UtahMosphere (works today)
4. [ ] Prepare S3/RDS endpoint overrides for phase 2
5. [ ] Update application config to point to `utahmosphere.local:8999`
