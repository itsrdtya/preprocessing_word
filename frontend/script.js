const input = document.getElementById("textInput");
const count = document.getElementById("charCount");
const analyzeBtn = document.getElementById("analyzeBtn");
const buttonText = document.getElementById("buttonText");
const clearBtn = document.getElementById("clearBtn");
const errorMessage = document.getElementById("errorMessage");
const resultSection = document.getElementById("resultSection");

const categoryInfo = {
  NON_HS_NON_ABUSIVE: ["Non-Hate Speech", "Teks tidak terdeteksi mengandung ujaran kebencian maupun bahasa kasar.", "non-hs"],
  HS: ["Hate Speech", "Teks terindikasi mengandung ujaran kebencian.", "hs"],
  ABUSIVE: ["Abusive Non-Hate Speech", "Teks terindikasi mengandung bahasa kasar, tetapi bukan ujaran kebencian.", "abusive"],
  HS_AND_ABUSIVE: ["Abusive Hate Speech", "Teks terindikasi mengandung ujaran kebencian dan bahasa kasar.", "both"]
};

input.addEventListener("input", () => {
  count.textContent = `${input.value.length} / 5000 karakter`;
  errorMessage.textContent = "";
});

clearBtn.addEventListener("click", () => {
  input.value = "";
  count.textContent = "0 / 5000 karakter";
  errorMessage.textContent = "";
  resultSection.classList.add("hidden");
  input.focus();
});

analyzeBtn.addEventListener("click", async () => {
  const text = input.value.trim();
  errorMessage.textContent = "";
  if (!text) {
    errorMessage.textContent = "Masukkan teks terlebih dahulu sebelum melakukan analisis.";
    input.focus();
    return;
  }

  analyzeBtn.disabled = true;
  buttonText.textContent = "Menganalisis...";
  resultSection.classList.add("hidden");

  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Analisis gagal dilakukan.");

    const info = categoryInfo[data.prediction];
    const badge = document.getElementById("categoryBadge");
    badge.className = "category-badge";
    if (info) {
      badge.textContent = info[0];
      badge.classList.add(info[2]);
      document.getElementById("categoryDescription").textContent = info[1];
    } else {
      badge.textContent = data.category || data.prediction || "Kategori tidak diketahui";
      document.getElementById("categoryDescription").textContent = "Hasil prediksi dari model HateSense.";
    }
    document.getElementById("originalText").textContent = data.original_text ?? text;
    document.getElementById("cleanText").textContent = data.clean_text || "(Tidak ada token tersisa setelah preprocessing)";
    resultSection.classList.remove("hidden");
    resultSection.scrollIntoView({ behavior: "smooth", block: "nearest" });
  } catch (error) {
    errorMessage.textContent = error.message || "Tidak dapat terhubung ke server. Pastikan Flask sedang berjalan.";
  } finally {
    analyzeBtn.disabled = false;
    buttonText.textContent = "Analisis Teks";
  }
});
