from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib
import os

from preprocessing import preprocessing

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")
# Inisialisasi Flask
app = Flask(
    __name__,
    template_folder=FRONTEND_DIR,
    static_folder=FRONTEND_DIR,
    static_url_path="/static"
)
CORS(app)

MODEL_PATH = os.path.join(BASE_DIR, "best_model_hatesense.pkl")
TFIDF_PATH = os.path.join(BASE_DIR, "tfidf_hatesense.pkl")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"File model tidak ditemukan: {MODEL_PATH}")

if not os.path.exists(TFIDF_PATH):
    raise FileNotFoundError(f"File TF-IDF tidak ditemukan: {TFIDF_PATH}")

model = joblib.load(MODEL_PATH)
tfidf = joblib.load(TFIDF_PATH)

# Pemetaan label hasil model ke nama kategori untuk website
LABELS = {
    "NON_HS_NON_ABUSIVE": "Non-Hate Speech",
    "HS": "Hate Speech",
    "ABUSIVE": "Abusive Non-Hate Speech",
    "HS_AND_ABUSIVE": "Abusive Hate Speech"
}


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(silent=True)

        if not data or "text" not in data:
            return jsonify({
                "error": "Input teks tidak ditemukan"
            }), 400

        text = data["text"]

        if not isinstance(text, str) or not text.strip():
            return jsonify({
                "error": "Teks tidak boleh kosong"
            }), 400

        # Preprocessing harus sama dengan preprocessing saat training
        clean_text = preprocessing(text)

        if not clean_text.strip():
            return jsonify({
                "error": "Teks tidak dapat diproses"
            }), 400

        # Transformasi menggunakan TF-IDF hasil training yang sama
        text_vector = tfidf.transform([clean_text])

        # Prediksi dengan model terbaik yang tersimpan
        prediction = str(model.predict(text_vector)[0])
        category = LABELS.get(prediction, prediction)

        return jsonify({
            "original_text": text,
            "clean_text": clean_text,
            "prediction": prediction,
            "category": category
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
