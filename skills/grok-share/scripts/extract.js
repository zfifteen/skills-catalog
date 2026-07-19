() => {
  const container = document.querySelector("main > div:nth-child(2) > div > div");
  if (!container) return { error: "no conversation container" };
  const blocks = [...container.children];
  const turns = [];
  for (const block of blocks) {
    const thoughtBtn = [...block.querySelectorAll("button")].find((b) =>
      /^Thought for/.test((b.textContent || "").trim())
    );
    const role = thoughtBtn ? "assistant" : "user";
    let text = "";
    if (role === "user") {
      const p = block.querySelector("p");
      text = (p ? p.innerText : block.innerText).trim();
    } else {
      const parts = [];
      block.querySelectorAll("p, h3").forEach((el) => {
        const t = el.innerText.trim();
        if (t && !/^Thought for/.test(t)) parts.push(t);
      });
      text = parts.join("\n\n");
    }
    if (text) turns.push({ role, text });
  }
  if (!turns.length) return { error: "no turns found" };
  return {
    title: document.title.replace(/ \| Shared Grok Conversation$/, "").trim(),
    url: location.href,
    extracted_at: new Date().toISOString(),
    turn_count: turns.length,
    turns,
  };
}