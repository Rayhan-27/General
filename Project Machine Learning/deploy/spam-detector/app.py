import streamlit as st
import joblib
import re
import time

# ======================================================
# KONFIGURASI HALAMAN
# ======================================================
st.set_page_config(
    page_title="Email Spam Detector",
    page_icon="📧",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ======================================================
# CUSTOM CSS (biar tampilannya nggak polos)
# ======================================================
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .title-container {
        text-align: center;
        padding: 1.5rem 0 0.5rem 0;
    }
    .title-container h1 {
        font-size: 2.4rem;
        margin-bottom: 0.2rem;
    }
    .title-container p {
        color: #9aa0a6;
        font-size: 1rem;
    }
    .result-box {
        padding: 1.5rem;
        border-radius: 14px;
        text-align: center;
        font-size: 1.4rem;
        font-weight: 700;
        margin-top: 1rem;
        animation: fadeIn 0.5s ease-in-out;
    }
    .spam-box {
        background: linear-gradient(135deg, #ff4b4b22, #ff4b4b11);
        border: 2px solid #ff4b4b;
        color: #ff6b6b;
    }
    .ham-box {
        background: linear-gradient(135deg, #21c17422, #21c17411);
        border: 2px solid #21c174;
        color: #2ecc71;
    }
    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(10px);}
        to {opacity: 1; transform: translateY(0);}
    }
    .footer {
        text-align: center;
        color: #6c7086;
        font-size: 0.8rem;
        margin-top: 3rem;
    }
    </style>
""", unsafe_allow_html=True)

# ======================================================
# LOAD MODEL & VECTORIZER (di-cache biar tidak reload terus)
# ======================================================
@st.cache_resource
def load_artifacts():
    model = joblib.load("spam_model_svm.pkl")
    tfidf = joblib.load("tfidf_vectorizer.pkl")
    return model, tfidf

try:
    model, tfidf = load_artifacts()
    load_error = None
except Exception as e:
    model, tfidf = None, None
    load_error = str(e)

# ======================================================
# FUNGSI PREPROCESSING SEDERHANA
# Sesuaikan dengan preprocessing yang dipakai di notebook
# 01_EDA_and_Preprocessing.ipynb temanmu (misal lowercase,
# hapus tanda baca, dsb). Kalau vectorizer sudah handle
# semuanya, fungsi ini bisa dikosongkan / dilewati.
# ======================================================
def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# ======================================================
# HEADER
# ======================================================
st.markdown("""
    <div class="title-container">
        <h1>📧 Email Spam Detector</h1>
        <p>Klasifikasi email Ham / Spam menggunakan model SVM + TF-IDF</p>
    </div>
""", unsafe_allow_html=True)

st.divider()

if load_error:
    st.error(
        f"Gagal memuat model/vectorizer. Pastikan file "
        f"`spam_model_svm.pkl` dan `tfidf_vectorizer.pkl` ada di folder repo.\n\n"
        f"Detail error: {load_error}"
    )
    st.stop()

# ======================================================
# CONTOH TEKS (biar user gampang coba)
# ======================================================
contoh_ham = "hi john, please find attached the report for last month. let me know if you have any questions. thanks, sarah"
contoh_spam = "congratulations you have won a free lottery prize of $1000000 click here now to claim your reward before it expires"

col_a, col_b = st.columns(2)
with col_a:
    if st.button("📝 Coba contoh Ham", use_container_width=True):
        st.session_state["user_input"] = contoh_ham
with col_b:
    if st.button("🚨 Coba contoh Spam", use_container_width=True):
        st.session_state["user_input"] = contoh_spam

# ======================================================
# INPUT USER
# ======================================================
user_input = st.text_area(
    "Masukkan isi email yang ingin dicek:",
    value=st.session_state.get("user_input", ""),
    height=200,
    placeholder="Contoh: Dear customer, you have won a prize... click this link to claim now!",
)

check_btn = st.button("🔍 Cek Email Ini", type="primary", use_container_width=True)

# ======================================================
# PREDIKSI
# ======================================================
if check_btn:
    if not user_input.strip():
        st.warning("⚠️ Tolong masukkan teks email terlebih dahulu.")
    else:
        with st.spinner("Menganalisis teks email..."):
            time.sleep(0.4)  # sekedar biar animasi spinner terasa
            cleaned = clean_text(user_input)
            vectorized = tfidf.transform([cleaned])
            prediction = model.predict(vectorized)[0]

            # Ambil confidence score kalau model mendukung
            proba_text = ""
            if hasattr(model, "predict_proba"):
                proba = model.predict_proba(vectorized)[0]
                confidence = max(proba) * 100
                proba_text = f"Tingkat keyakinan model: **{confidence:.1f}%**"
            elif hasattr(model, "decision_function"):
                score = model.decision_function(vectorized)[0]
                proba_text = f"Skor keputusan model: **{score:.2f}**"

        label = str(prediction).lower()
        is_spam = label in ["spam", "1"]

        # --- DEBUG INFO (hapus/comment kalau sudah tidak dibutuhkan) ---
        with st.expander("🔧 Debug info (klik untuk lihat)"):
            st.write("Raw prediction:", prediction, "| type:", type(prediction))
            if hasattr(model, "classes_"):
                st.write("Kelas yang dikenali model (model.classes_):", model.classes_)
            st.write("Jumlah fitur non-zero di vector input:", vectorized.nnz)
            st.write("Shape vector:", vectorized.shape)
            if vectorized.nnz == 0:
                st.error(
                    "⚠️ Vector input SEMUA NOL — artinya tidak ada satupun kata dari "
                    "input yang dikenali oleh tfidf_vectorizer. Ini biasanya karena "
                    "preprocessing (clean_text) tidak cocok dengan vocabulary vectorizer, "
                    "atau vectorizer di-training dari bahasa/format teks yang berbeda."
                )

        if is_spam:
            st.markdown(
                '<div class="result-box spam-box">🚨 Ini terdeteksi SPAM</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="result-box ham-box">✅ Ini terdeteksi HAM (Aman)</div>',
                unsafe_allow_html=True,
            )

        if proba_text:
            st.markdown(f"<p style='text-align:center; color:#9aa0a6; margin-top:0.8rem;'>{proba_text}</p>", unsafe_allow_html=True)

        with st.expander("Lihat detail teks yang diproses"):
            st.code(cleaned)

# ======================================================
# FOOTER
# ======================================================
st.markdown("""
    <div class="footer">
        Dibuat dengan ❤️ menggunakan Streamlit • Model: SVM + TF-IDF • Dataset: Enron Spam
    </div>
""", unsafe_allow_html=True)