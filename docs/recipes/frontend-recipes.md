# Frontend Recipes

Browser and client-side patterns for UtahMosphere.

---

## Recipe: Fetch Node Status

**Status:** Implemented

```javascript
async function getNodeStatus(baseUrl = "http://127.0.0.1:8999") {
  const res = await fetch(`${baseUrl}/status`);
  if (!res.ok) throw new Error(`Status ${res.status}`);
  return res.json();
}

// Usage
const { tenants, claimed } = await getNodeStatus();
console.log("Apps:", tenants, "Claimed:", claimed);
```

---

## Recipe: Deploy App from Browser (via /command)

**Status:** Implemented (open mode or matching vibe hash)

```javascript
async function deployApp(appName, acousticHash = "0".repeat(64)) {
  const res = await fetch("http://127.0.0.1:8999/command", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      transcript: `deploy application ${appName}`,
      acoustic_hash: acousticHash,
    }),
  });
  return res.json();
}
```

> CORS: Kernel does not set CORS headers. Use same-origin proxy or server-side call in production.

---

## Recipe: Tycoon Payment Flow

**Status:** Implemented

```javascript
async function accessApp(appName, clientId = "web-client") {
  const res = await fetch(`http://127.0.0.1:8999/app/${appName}`, {
    headers: { "X-Client-ID": clientId },
  });

  if (res.status === 402) {
    const invoice = await res.json();
    return { paid: false, invoice };
  }

  return { paid: true, data: await res.json() };
}

// Poll until paid (simulated ~60s settlement)
async function waitForAccess(appName, clientId, maxWaitMs = 90000) {
  const start = Date.now();
  while (Date.now() - start < maxWaitMs) {
    const result = await accessApp(appName, clientId);
    if (result.paid) return result;
    await new Promise((r) => setTimeout(r, 5000));
  }
  throw new Error("Payment timeout");
}
```

Template: [frontend-upload](../../templates/frontend-upload/)

---

## Recipe: Direct-to-Edge Upload (S3 Mesh)

**Status:** Roadmap

```javascript
async function uploadToUtah(file, tenantId, signature) {
  const response = await fetch(
    `http://utahmosphere.local:8999/s3/assets/${file.name}`,
    {
      method: "POST",
      headers: {
        "X-Utah-Tenant-ID": tenantId,
        "X-Utah-Signature": signature,
        "Content-Type": file.type,
      },
      body: file,
    }
  );
  return response.json();
}
```

Generate signature server-side — never expose `UTAH_SECRET_VECTOR` in browser code.

---

## Recipe: Health Badge Component (React)

```jsx
function UtahHealthBadge({ baseUrl }) {
  const [health, setHealth] = useState(null);

  useEffect(() => {
    fetch(`${baseUrl}/health`)
      .then((r) => r.json())
      .then(setHealth)
      .catch(() => setHealth({ status: "down" }));
  }, [baseUrl]);

  if (!health) return <span>Checking…</span>;
  return (
    <span className={health.status === "healthy" ? "ok" : "err"}>
      {health.node} — {health.status}
    </span>
  );
}
```

Starter: [voice-controlled-dashboard](../../starter-projects/voice-controlled-dashboard/)
