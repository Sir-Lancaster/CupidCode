import cookie from "cookie";

export async function makeRequest(uri, method = "get", body = {}) {
  const parsedCookie = cookie.parse(document.cookie)
  const options = {
    method,
    headers: {
      "Content-Type": "application/json",
      "Accept": "application/json",
      "X-CSRFToken": parsedCookie.csrftoken // protects against CSRF attacks
    },
    credentials: "include", // includes cookies in the request
  }
  if (method === "post") {
    options.body = JSON.stringify(body)
  }

  const result = await fetch(uri, options);

  // Read response as text first so we can inspect non-JSON responses
  const text = await result.text().catch(() => null);
  const contentType = result.headers.get("content-type") || "";

  if (!result.ok) {
    console.error(`Request failed ${result.status} ${result.statusText}`, { uri, contentType, body: text });
    // If it actually is JSON, try to parse it, otherwise throw with the text for debugging
    if (contentType.includes("application/json")) {
      try { return JSON.parse(text); } catch (e) { /* fall through */ }
    }
    throw new Error(`Request to ${uri} failed: ${result.status} - see console for body`);
  }

  // Successful: parse JSON only when server declares JSON, otherwise return text
  if (contentType.includes("application/json")) {
    try { return JSON.parse(text); }
    catch (err) {
      console.error("Failed to parse JSON response", { uri, contentType, text });
      throw err;
    }
  }

  // Not JSON — return text so caller can inspect (or change to throw if you prefer)
  return text;
}

export async function logoutRequest() {
    const parsedCookie = cookie.parse(document.cookie)
    const options = {
        'method':'get',
        headers: {
          "X-CSRFToken": parsedCookie.csrftoken // protects against CSRF attacks
        },
        credentials: "include", // includes cookies in the request
    }
    await fetch('/logout/', options);
}