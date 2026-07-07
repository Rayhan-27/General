"""
Script diagnostik untuk mengecek apakah model & vectorizer
bekerja dengan benar di luar Streamlit.
Jalankan: python diagnose_model.py
"""
import joblib

model = joblib.load("spam_model_svm.pkl")
tfidf = joblib.load("tfidf_vectorizer.pkl")

print("=" * 60)
print("INFO MODEL")
print("=" * 60)
print("Tipe model:", type(model))
print("Punya atribut classes_?", hasattr(model, "classes_"))
if hasattr(model, "classes_"):
    print("Isi classes_:", model.classes_)

print("\n" + "=" * 60)
print("INFO VECTORIZER")
print("=" * 60)
print("Jumlah vocabulary:", len(tfidf.vocabulary_))
print("Contoh 10 kata di vocabulary:", list(tfidf.vocabulary_.keys())[:10])

# Beberapa contoh teks yang JELAS beda karakter (spam vs ham)
contoh_teks = [
    ("SPAM jelas", "congratulations you have won a free lottery prize click here now claim reward money"),
    ("SPAM jelas 2", "buy cheap viagra online discount pills no prescription needed order now"),
    ("HAM jelas", "hi john please find attached report last month let me know questions thanks"),
    ("HAM jelas 2", "meeting scheduled tomorrow morning please bring your laptop and notes"),
]

print("\n" + "=" * 60)
print("HASIL PREDIKSI PER CONTOH")
print("=" * 60)
for label, teks in contoh_teks:
    vec = tfidf.transform([teks])
    pred = model.predict(vec)[0]
    nnz = vec.nnz
    print(f"[{label}] -> prediksi: {pred!r}  | kata dikenali: {nnz}")

# Cek juga distribusi prediksi kalau model dipaksa prediksi teks acak/kosong
print("\n" + "=" * 60)
print("CEK APAKAH MODEL SELALU JAWAB SAMA (walau vector beda-beda)")
print("=" * 60)
import numpy as np
random_texts = [
    "free money winner claim prize now",
    "urgent your account suspended verify now",
    "project deadline meeting notes attached",
    "lunch tomorrow schedule confirm",
    "asdkj alksdj laksjd laksjd",  # random gibberish, should have 0 nnz
]
preds = []
for t in random_texts:
    v = tfidf.transform([t])
    p = model.predict(v)[0]
    preds.append(p)
    print(f"Teks: {t[:40]:40s} | nnz: {v.nnz:3d} | prediksi: {p!r}")

print("\nApakah semua prediksi sama persis?", len(set(preds)) == 1)
if len(set(preds)) == 1:
    print("⚠️  MODEL SELALU MENGHASILKAN OUTPUT YANG SAMA UNTUK SEMUA INPUT.")
    print("   Ini bukan masalah di kode Streamlit — kemungkinan besar ada")
    print("   masalah saat training model (misal label salah, atau model")
    print("   yang disimpan bukan model yang benar-benar sudah di-fit).")
