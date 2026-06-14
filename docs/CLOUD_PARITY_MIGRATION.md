### ☁️ Cloud Parity & Migration Guide

UtahMosphere OS v25.0 Golden Master provides **implemented** drop-in gateways for S3, Lambda, and RDS on port `8999`.

> **Status:** S3, Lambda invoke, and RDS HTTP routes are **live**. See [Capability Matrix](CAPABILITY_MATRIX.md) and [Omega-Build](OMEGA_BUILD.md).

**Verify:** `python examples/omega-build-verify/verify.py`

**Tutorial:** [Cloud Migration Walkthrough](tutorials/04-cloud-migration-walkthrough.md)  
**Recipes:** [Migration Recipes](recipes/migration-recipes.md)

---

#### **1. AWS S3 ↔ Utah S3 Mesh**

**Status:** **Implemented**

```bash
curl -X PUT http://127.0.0.1:8999/s3/my-data/file.txt --data-binary "Hello"
curl http://127.0.0.1:8999/s3/my-data/file.txt
```

**boto3 migration:**

```python
import boto3
s3 = boto3.client(
    's3',
    endpoint_url='http://utahmosphere.local:8999',
    aws_access_key_id='YOUR_TENANT_ID',
    aws_secret_access_key='YOUR_HMAC_SIG'
)
s3.put_object(Bucket='my-data', Key='file.txt', Body=b'Hello')
```

---

#### **2. AWS Lambda / GCP Functions ↔ Utah Lambda**

**Status:** **Implemented**

```python
def handler(event, context):
    name = event.get('name', 'World')
    return {"message": f"Hello {name} from UtahMosphere!"}
```

```bash
curl -X POST http://127.0.0.1:8999/lambda/my-function/invoke \
  -H "Content-Type: application/json" \
  -d '{"name": "General 23"}'
```

Deploy handler via voice or `/command`, then invoke.

---

#### **3. AWS RDS / GCP Cloud SQL ↔ Utah RDS Ledger**

**Status:** **Implemented**

```bash
curl -X POST http://127.0.0.1:8999/rds/write \
  -H "Content-Type: application/json" \
  -d '{"key": "user:123", "value": {"name": "Alice", "score": 9000}}'

curl http://127.0.0.1:8999/rds/read/user:123
```

---

#### **4. GCP App Engine / Azure Web Apps ↔ Utah Workloads**

**Status:** **Implemented** via `/command` + UtahX proxy

```bash
curl -X POST http://127.0.0.1:8999/command \
  -H "Content-Type: application/json" \
  -d '{"transcript":"deploy application my-website","acoustic_hash":"0"}'

curl -H "X-Client-ID: client-1" http://127.0.0.1:8999/app/my-website
```

---

#### **Migration Checklist**

1. [ ] Install via `sudo bash bootstrap.sh` or [Local Development](LOCAL_DEVELOPMENT.md)
2. [ ] Run `python examples/omega-build-verify/verify.py`
3. [ ] Point SDK `endpoint_url` to `http://utahmosphere.local:8999`
4. [ ] Migrate stateless APIs and storage paths
5. [ ] Update DNS/ingress to port `8999`
