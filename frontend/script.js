const API_BASE = "http://127.0.0.1:8000";

let currentSource = null;
let currentTopic = "";
let latestReportMd = "";
let latestFeedbackMd = "";

// ---------------- Tabs ----------------

document.querySelectorAll(".tab-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
    document.querySelectorAll(".tab-panel").forEach(p => p.classList.remove("active"));
    btn.classList.add("active");
    document.getElementById(`panel-${btn.dataset.tab}`).classList.add("active");
  });
});

// ---------------- Form submit ----------------

document.getElementById("researchForm").addEventListener("submit", (e) => {
  e.preventDefault();
  startResearch();
});

function resetUI() {
  document.getElementById("errorBanner").classList.add("d-none");
  document.getElementById("errorBanner").textContent = "";

  document.getElementById("progressSection").classList.remove("d-none");
  document.querySelectorAll(".step").forEach(el => {
    el.classList.remove("active", "done", "error");
  });
  document.getElementById("statusMessage").textContent = "Connecting to research pipeline...";

  document.getElementById("resultsSection").classList.add("d-none");
  document.getElementById("reportArticle").innerHTML = "";
  document.getElementById("feedbackArticle").innerHTML = "";
  document.getElementById("searchResults").textContent = "";
  document.getElementById("scrapedContent").textContent = "";

  latestReportMd = "";
  latestFeedbackMd = "";

  // Reset to report tab
  document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
  document.querySelectorAll(".tab-panel").forEach(p => p.classList.remove("active"));
  document.querySelector('.tab-btn[data-tab="report"]').classList.add("active");
  document.getElementById("panel-report").classList.add("active");
}

function setStepState(step, state) {
  const el = document.querySelector(`.step[data-step="${step}"]`);
  if (!el) return;

  if (state === "active") {
    const steps = Array.from(document.querySelectorAll(".step"));
    const idx = steps.indexOf(el);
    steps.slice(0, idx).forEach(s => {
      s.classList.remove("active");
      s.classList.add("done");
    });
  }

  el.classList.remove("active", "done", "error");
  el.classList.add(state);
}

function setStatusMessage(message) {
  document.getElementById("statusMessage").textContent = message;
}

function showError(message) {
  const banner = document.getElementById("errorBanner");
  banner.textContent = `⚠ ${message}`;
  banner.classList.remove("d-none");
}

function renderMarkdown(targetElId, mdText) {
  const el = document.getElementById(targetElId);
  if (!mdText || !mdText.trim()) {
    el.innerHTML = `<p class="empty-state">No content generated for this section.</p>`;
    return;
  }
  el.innerHTML = marked.parse(mdText);
}

function startResearch() {
  const topic = document.getElementById("topicInput").value.trim();
  if (!topic) return;
  currentTopic = topic;

  if (currentSource) {
    currentSource.close();
    currentSource = null;
  }

  resetUI();

  const startBtn = document.getElementById("startBtn");
  startBtn.disabled = true;
  document.getElementById("startBtnLabel").textContent = "Researching...";
  document.getElementById("startBtnSpinner").classList.remove("d-none");

  const url = `${API_BASE}/research/stream?topic=${encodeURIComponent(topic)}`;
  const source = new EventSource(url);
  currentSource = source;

  const finish = () => {
    source.close();
    currentSource = null;
    startBtn.disabled = false;
    document.getElementById("startBtnLabel").textContent = "Start Research";
    document.getElementById("startBtnSpinner").classList.add("d-none");
  };

  source.onmessage = (e) => {
    let event;
    try {
      event = JSON.parse(e.data);
    } catch (err) {
      console.error("Bad SSE payload:", e.data);
      return;
    }

    if (event.type === "status") {
      setStepState(event.step, event.state);
      setStatusMessage(event.message);

    } else if (event.type === "result") {
      const data = event.data || {};

      document.querySelectorAll(".step").forEach(el => {
        el.classList.remove("active");
        el.classList.add("done");
      });
      setStatusMessage("✅ Research completed!");

      latestReportMd = data.report || "";
      latestFeedbackMd = data.feedback || "";

      renderMarkdown("reportArticle", latestReportMd);
      renderMarkdown("feedbackArticle", latestFeedbackMd);
      document.getElementById("searchResults").textContent = data.search_results || "(empty)";
      document.getElementById("scrapedContent").textContent = data.scraped_content || "(empty)";

      document.getElementById("resultsSection").classList.remove("d-none");
      document.getElementById("resultsSection").scrollIntoView({ behavior: "smooth", block: "start" });

      finish();

    } else if (event.type === "error") {
      setStatusMessage("");
      document.querySelectorAll(".step.active").forEach(el => {
        el.classList.remove("active");
        el.classList.add("error");
      });
      showError(event.message || "Something went wrong while researching this topic.");
      finish();
    }
  };

  source.onerror = () => {
    showError("Connection to the research server was lost. Is the backend running?");
    document.querySelectorAll(".step.active").forEach(el => {
      el.classList.remove("active");
      el.classList.add("error");
    });
    finish();
  };
}

// ---------------- Export: Markdown ----------------

document.getElementById("downloadMdBtn").addEventListener("click", () => {
  if (!latestReportMd.trim()) return;
  const blob = new Blob([latestReportMd], { type: "text/markdown" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `${slugify(currentTopic || "research-report")}.md`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
});

// ---------------- Export: PDF ----------------

document.getElementById("downloadPdfBtn").addEventListener("click", () => {
  const el = document.getElementById("reportArticle");
  if (!latestReportMd.trim()) return;

  const opt = {
    margin: 12,
    filename: `${slugify(currentTopic || "research-report")}.pdf`,
    image: { type: "jpeg", quality: 0.98 },
    html2canvas: { scale: 2, backgroundColor: "#0b0e14" },
    jsPDF: { unit: "mm", format: "a4", orientation: "portrait" },
  };

  html2pdf().set(opt).from(el).save();
});

// ---------------- Copy report ----------------

document.getElementById("copyReportBtn").addEventListener("click", async () => {
  if (!latestReportMd.trim()) return;
  try {
    await navigator.clipboard.writeText(latestReportMd);
    const btn = document.getElementById("copyReportBtn");
    const original = btn.textContent;
    btn.textContent = "✅ Copied!";
    setTimeout(() => { btn.textContent = original; }, 1500);
  } catch (err) {
    console.error("Copy failed:", err);
  }
});

function slugify(text) {
  return text
    .toLowerCase()
    .trim()
    .replace(/[^\w\s-]/g, "")
    .replace(/\s+/g, "-")
    .slice(0, 60) || "report";
}