/*
 * Fallback: export the currently open ChatGPT conversation from the DOM.
 *
 * Use only when fetch-conversation.js cannot get the JSON.
 * The script scrolls to the top repeatedly so older messages load,
 * then writes a Markdown file with one section per message.
 *
 * Run on chatgpt.com / chat.openai.com:
 *   1. Open the conversation.
 *   2. Open DevTools (F12) -> Console.
 *   3. Run this file (double-click copy-dom-js.bat, then paste here).
 */
(async () => {
  const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

  function findScroller() {
    const candidates = [document.scrollingElement, ...document.querySelectorAll("main, div")];
    let best = document.scrollingElement;
    for (const element of candidates) {
      if (!element) continue;
      if (element.scrollHeight > element.clientHeight + 200) {
        if (!best || element.scrollHeight > best.scrollHeight) best = element;
      }
    }
    return best;
  }

  const countMessages = () =>
    [...document.querySelectorAll("[data-message-author-role]")].filter(
      (node) => node.offsetParent !== null
    ).length;

  let scroller = findScroller();
  let lastCount = -1;
  let lastHeight = -1;

  for (let step = 0; step < 400; step++) {
    if (scroller) scroller.scrollTop = 0;
    window.scrollTo(0, 0);
    await sleep(700);

    const count = countMessages();
    const height = scroller ? scroller.scrollHeight : document.body.scrollHeight;
    if (step % 10 === 0) console.log(`step ${step}: ${count} messages, height ${height}`);

    if (count === lastCount && height === lastHeight && step > 4) break;
    lastCount = count;
    lastHeight = height;
    const next = findScroller();
    if (next) scroller = next;
  }

  const nodes = [...document.querySelectorAll("[data-message-author-role]")].filter(
    (node) => node.offsetParent !== null
  );

  const sections = [];
  for (const node of nodes) {
    const role = node.getAttribute("data-message-author-role") || "unknown";
    const body = node.querySelector(".markdown") || node;
    const text = (body.innerText || "").trim();
    if (text) sections.push(`## ${role}\n\n${text}`);
  }

  const markdown = sections.join("\n\n");
  const blob = new Blob([markdown], { type: "text/markdown" });
  const href = URL.createObjectURL(blob);

  const link = document.createElement("a");
  link.href = href;
  link.download = "chatgpt-dom.md";
  document.body.appendChild(link);
  link.click();
  link.remove();

  setTimeout(() => URL.revokeObjectURL(href), 10000);
  console.log(`Downloaded ${link.download} (${nodes.length} messages, ${markdown.length} chars)`);
})();
