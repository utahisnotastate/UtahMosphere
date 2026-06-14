/**
 * Frontend upload client template (S3 Mesh — roadmap API).
 * For implemented APIs, use fetchStatus() and accessApp().
 */

const BASE_URL = "http://127.0.0.1:8999";

export async function fetchStatus() {
  const res = await fetch(`${BASE_URL}/status`);
  return res.json();
}

export async function accessApp(appName, clientId = "web-client") {
  const res = await fetch(`${BASE_URL}/app/${appName}`, {
    headers: { "X-Client-ID": clientId },
  });
  if (res.status === 402) {
    return { paid: false, invoice: await res.json() };
  }
  return { paid: true, data: await res.json() };
}

/** Roadmap — S3 Mesh upload */
export async function uploadToUtah(file, tenantId, signature) {
  const res = await fetch(`${BASE_URL}/s3/assets/${file.name}`, {
    method: "POST",
    headers: {
      "X-Utah-Tenant-ID": tenantId,
      "X-Utah-Signature": signature,
      "Content-Type": file.type,
    },
    body: file,
  });
  return res.json();
}
