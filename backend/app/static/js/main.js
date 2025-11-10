document.addEventListener("DOMContentLoaded", () => {
  const buildBtn = document.getElementById("build-index-btn");
  const statusDiv = document.getElementById("status");
  const searchBtn = document.getElementById("search-btn");
  const searchInput = document.getElementById("search-input");
  const resultsDiv = document.getElementById("search-results");

  if (buildBtn) {
    buildBtn.addEventListener("click", async () => {
      statusDiv.textContent = "Building index…";
      try {
        const r = await fetch("/api/build_index", { method: "POST" });
        const j = await r.json();
        statusDiv.textContent = "Result: " + JSON.stringify(j);
      } catch (e) {
        statusDiv.textContent = "Error building index: " + e;
      }
    });
  }

  if (searchBtn) {
    searchBtn.addEventListener("click", async () => {
      const q = searchInput.value.trim();
      if (!q) return;
      resultsDiv.innerHTML = "Searching…";
      try {
        const resp = await fetch(`/api/search?q=${encodeURIComponent(q)}&k=6`);
        if (!resp.ok) {
          const txt = await resp.text();
          resultsDiv.textContent = "Search error: " + txt;
          return;
        }
        const data = await resp.json();
        if (!data.results || data.results.length === 0) {
          resultsDiv.innerHTML = "<p>No results</p>";
          return;
        }
        resultsDiv.innerHTML = "";
        data.results.forEach(r => {
          const el = document.createElement("div");
          el.className = "card";
          el.innerHTML = `<h4>${r.title}</h4><p class="meta">${r.domain} • score: ${r.score.toFixed(3)}</p><p class="snippet">${r.snippet}</p><p><a href="${r.url}" target="_blank">Open</a></p>`;
          resultsDiv.appendChild(el);
        });
      } catch (e) {
        resultsDiv.textContent = "Search failed: " + e;
      }
    });
  }
});
