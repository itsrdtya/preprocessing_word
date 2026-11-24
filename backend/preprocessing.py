import re
import pandas as pd

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory


# Inisialisasi stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# Inisialisasi stopwords
stop_factory = StopWordRemoverFactory()
stopwords = set(stop_factory.get_stop_words())

# Mempertahankan kata negasi sesuai notebook
negation_words = {"tidak", "bukan", "jangan", "belum", "tanpa"}
stopwords = stopwords - negation_words

# Kamus normalisasi sesuai notebook
normalisasi = {
    "gak": "tidak",
    "ga": "tidak",
    "nggak": "tidak",
    "enggak": "tidak",
    "tdk": "tidak",
    "yg": "yang",
    "dgn": "dengan",
    "krn": "karena",
    "aja": "saja",
    "udah": "sudah",
    "blm": "belum",
    "bgt": "banget",
    "kalo": "kalau",
    "loe": "kamu",
    "lu": "kamu",
    "gw": "saya",
    "gue": "saya"
}


def preprocessing(text):
    """Preprocessing teks mengikuti urutan pada notebook HateSense."""
    if pd.isna(text):
        return ""

    text = str(text)

    # Cleaning
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"@\w+", " ", text)
    text = re.sub(r"RT\s+", " ", text)

    # Case folding
    text = text.lower()

    # Menghapus simbol dan angka
    text = re.sub(r"[^a-zA-Z\s]", " ", text)

    # Tokenisasi
    tokens = text.split()

    # Normalisasi
    tokens = [normalisasi.get(word, word) for word in tokens]

    # Stopword removal
    tokens = [
        word for word in tokens
        if word not in stopwords and len(word) > 1
    ]

    # Stemming
    tokens = [stemmer.stem(word) for word in tokens]

    return " ".join(tokens)