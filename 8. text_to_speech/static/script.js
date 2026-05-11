const fileInput = document.getElementById("fileInput");
const readBtn = document.getElementById("readBtn");
const stopBtn = document.getElementById("stopBtn");
const statusEl = document.getElementById("status");

if (!("speechSynthesis" in window)) {
  statusEl.textContent = "Speech is not supported in this browser.";
}

function setStatus(message) {
  statusEl.textContent = message;
}

function speakText(text) {
  window.speechSynthesis.cancel();

  const trimmed = text.trim();
  if (!trimmed) {
    setStatus("No readable text found in this file.");
    return;
  }

  const utterance = new SpeechSynthesisUtterance(trimmed.slice(0, 5000));
  utterance.rate = 1;
  utterance.onstart = () => setStatus("Reading started...");
  utterance.onend = () => setStatus("Done reading.");
  utterance.onerror = () => setStatus("Could not read the text.");

  window.speechSynthesis.speak(utterance);
}

async function extractPdfText(file) {
  const pdfjsLib = await import("https://cdnjs.cloudflare.com/ajax/libs/pdf.js/4.5.136/pdf.min.mjs");
  pdfjsLib.GlobalWorkerOptions.workerSrc = "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/4.5.136/pdf.worker.min.mjs";

  const bytes = new Uint8Array(await file.arrayBuffer());
  const pdf = await pdfjsLib.getDocument({ data: bytes }).promise;

  let fullText = "";
  for (let pageNo = 1; pageNo <= pdf.numPages; pageNo++) {
    const page = await pdf.getPage(pageNo);
    const content = await page.getTextContent();
    const pageText = content.items.map(item => item.str).join(" ");
    fullText += pageText + " ";
  }
  return fullText;
}

async function extractDocxText(file) {
  const arrayBuffer = await file.arrayBuffer();
  const result = await mammoth.extractRawText({ arrayBuffer });
  return result.value || "";
}

readBtn.addEventListener("click", async () => {
  const file = fileInput.files[0];
  if (!file) {
    setStatus("Please choose a file first.");
    return;
  }

  const ext = file.name.split(".").pop().toLowerCase();

  try {
    setStatus("Reading file...");

    if (ext === "pdf") {
      const text = await extractPdfText(file);
      speakText(text);
      return;
    }

    if (ext === "docx") {
      const text = await extractDocxText(file);
      speakText(text);
      return;
    }

    if (ext === "doc") {
      setStatus(".doc files are not supported in browser. Please use .docx or .pdf.");
      return;
    }

    setStatus("Only PDF or Word files are allowed.");
  } catch (error) {
    console.error(error);
    setStatus("Could not process this file.");
  }
});

stopBtn.addEventListener("click", () => {
  window.speechSynthesis.cancel();
  setStatus("Reading stopped.");
});
