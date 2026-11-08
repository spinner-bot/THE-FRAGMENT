/*
 * Download the full JSON of the currently open ChatGPT conversation.
 *
 * Use on chatgpt.com / chat.openai.com:
 *   1. Open the conversation.
 *   2. Open DevTools (F12) -> Console.
 *   3. Run this file (double-click copy-fetch-js.bat, then paste here).
 *
 * The script uses the page's own session, so no token or cookie is typed.
 * If the endpoint returns 401/403, use the Network-tab + cURL fallback
 * described in README.md.
 */
(async () => {
  const match = location.pathname.match(/\/c\/([0-9a-f-]+)/i);
  if (!match) {
    console.error("Open a conversation first. The URL must contain /c/<id>.");
    return;
  }

  const id = match[1];
  const url = `/backend-api/conversation/${id}`;
  console.log("Fetching", url);

  const response = await fetch(url, {
    credentials: "include",
    headers: { accept: "*/*" },
  });

  if (!response.ok) {
    console.error(
      `HTTP ${response.status}. ` +
        "Fallback: DevTools -> Network -> filter \"conversation\" -> reload -> " +
        "right-click the request -> Copy as cURL (bash)."
    );
    return;
  }

  const data = await response.json();
  const json = JSON.stringify(data, null, 2);
  const blob = new Blob([json], { type: "application/json" });
  const href = URL.createObjectURL(blob);

  const link = document.createElement("a");
  link.href = href;
  link.download = `chatgpt-${id}.json`;
  document.body.appendChild(link);
  link.click();
  link.remove();

  setTimeout(() => URL.revokeObjectURL(href), 10000);
  console.log(
    `Downloaded ${link.download} (${(blob.size / 1048576).toFixed(2)} MB)`
  );
})();
