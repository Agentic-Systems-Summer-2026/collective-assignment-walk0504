// Netlify Function: vault
// Stores/retrieves an encrypted "vault" blob per user password-hash key.
// The client encrypts the data with a key derived from the password, so the
// server only ever sees opaque ciphertext — never the password or plaintext.
import { getStore } from "@netlify/blobs";

export default async (request, context) => {
  try {
    const store = getStore("aginsight-vault");
    const url = new URL(request.url);
    const method = request.method;
    const vaultKey = url.searchParams.get("key") || null;

    // GET /vault?key=<hash>  ->  return stored ciphertext (or 404)
    if (method === "GET") {
      if (!vaultKey) {
        return new Response(JSON.stringify({ error: "missing key" }), {
          status: 400,
          headers: { "content-type": "application/json" },
        });
      }
      const blob = await store.get(vaultKey, { type: "text" });
      if (blob == null) {
        return new Response(JSON.stringify({ found: false }), {
          status: 200,
          headers: { "content-type": "application/json" },
        });
      }
      return new Response(
        JSON.stringify({ found: true, data: blob }),
        { status: 200, headers: { "content-type": "application/json" } }
      );
    }

    // POST /vault  body: { key, data }  ->  write ciphertext
    if (method === "POST" || method === "PUT") {
      const body = await request.json();
      const { key, data } = body || {};
      if (!key || typeof data !== "string") {
        return new Response(JSON.stringify({ error: "invalid body" }), {
          status: 400,
          headers: { "content-type": "application/json" },
        });
      }
      // Keep blobs bounded (reject > 500 KB) to be safe.
      if (data.length > 500 * 1024) {
        return new Response(JSON.stringify({ error: "too large" }), {
          status: 413,
          headers: { "content-type": "application/json" },
        });
      }
      await store.set(key, data, { metadata: { type: "encrypted-vault", v: "1" } });
      return new Response(
        JSON.stringify({ ok: true }),
        { status: 200, headers: { "content-type": "application/json" } }
      );
    }

    return new Response(JSON.stringify({ error: "method not allowed" }), {
      status: 405,
      headers: { "content-type": "application/json" },
    });
  } catch (err) {
    console.error("vault error:", err);
    return new Response(JSON.stringify({ error: "server error" }), {
      status: 500,
      headers: { "content-type": "application/json" },
    });
  }
};
