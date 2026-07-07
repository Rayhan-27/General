import streamlit as st
import joblib
import re
import time

# ======================================================
# KONFIGURASI HALAMAN
# ======================================================
st.set_page_config(
    page_title="Spam Shield — Email Classifier",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ======================================================
# CUSTOM CSS
# ======================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at 15% -10%, #4c1d9530 0%, transparent 45%),
            radial-gradient(circle at 90% 10%, #0891b230 0%, transparent 40%),
            #0a0c12;
    }

    #MainMenu, footer, header {visibility: hidden;}

    /* ============ NAVBAR ============ */
    .navbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.6rem 0 1.4rem 0;
        border-bottom: 1px solid #ffffff10;
        margin-bottom: 1.6rem;
    }
    .navbar-brand {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 1.15rem;
        color: #f1f5f9;
    }
    .navbar-brand .logo-box {
        width: 34px; height: 34px;
        border-radius: 9px;
        background: linear-gradient(135deg, #8b5cf6, #06b6d4);
        display: flex; align-items: center; justify-content: center;
        font-size: 1.1rem;
        box-shadow: 0 4px 14px #8b5cf655;
    }
    .navbar-tag {
        font-size: 0.72rem;
        color: #64748b;
        background: #ffffff08;
        border: 1px solid #ffffff14;
        padding: 0.28rem 0.7rem;
        border-radius: 999px;
    }

    /* ============ HERO ============ */
    .hero {
        text-align: center;
        padding: 0.8rem 1rem 1.8rem 1rem;
    }
    .hero h1 {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 2.5rem;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #ffffff 15%, #c4b5fd 55%, #67e8f9 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        line-height: 1.15;
    }
    .hero p {
        color: #8b94a3;
        font-size: 1rem;
        max-width: 460px;
        margin: 0 auto;
    }

    /* ============ STAT PILLS ============ */
    .stats-row {
        display: flex;
        justify-content: center;
        gap: 0.7rem;
        flex-wrap: wrap;
        margin: 1.4rem 0 0.4rem 0;
    }
    .stat-pill {
        background: #ffffff06;
        border: 1px solid #ffffff12;
        border-radius: 12px;
        padding: 0.65rem 1.1rem;
        text-align: center;
        min-width: 100px;
    }
    .stat-pill .num {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 1.15rem;
        color: #e2e8f0;
        display: block;
    }
    .stat-pill .lbl {
        font-size: 0.68rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    /* ============ LANGUAGE NOTICE ============ */
    .lang-notice {
        display: flex;
        align-items: flex-start;
        gap: 0.6rem;
        background: linear-gradient(135deg, #0891b214, #0891b208);
        border: 1px solid #0891b240;
        color: #67e8f9;
        padding: 0.7rem 1rem;
        border-radius: 12px;
        font-size: 0.85rem;
        margin: 1.6rem 0 1rem 0;
        line-height: 1.45;
    }
    .lang-notice b { color: #a5f3fc; }

    /* ============ INPUT CARD ============ */
    .input-card {
        background: linear-gradient(180deg, #ffffff08, #ffffff02);
        border: 1px solid #ffffff14;
        border-radius: 20px;
        padding: 1.7rem;
        box-shadow: 0 20px 50px -20px #00000080;
    }
    .card-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #cbd5e1;
        margin-bottom: 0.6rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }

    .stTextArea textarea {
        background-color: #05060a !important;
        border: 1px solid #ffffff1a !important;
        border-radius: 13px !important;
        color: #e5e7eb !important;
        font-size: 0.95rem !important;
        padding: 1rem !important;
    }
    .stTextArea textarea:focus {
        border: 1px solid #8b5cf6 !important;
        box-shadow: 0 0 0 3px #8b5cf62a !important;
    }
    .stTextArea textarea::placeholder { color: #4b5563 !important; }

    div.stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #8b5cf6, #6366f1);
        color: white;
        border: none;
        border-radius: 13px;
        padding: 0.75rem 0;
        font-weight: 600;
        font-size: 1rem;
        letter-spacing: 0.01em;
        transition: all 0.25s ease;
        box-shadow: 0 8px 24px -8px #8b5cf680;
        margin-top: 0.9rem;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 28px -8px #8b5cf6a0;
    }
    div.stButton > button:active { transform: translateY(0px); }

    /* ============ RESULT ============ */
    .result-box {
        padding: 1.9rem 1.6rem;
        border-radius: 18px;
        text-align: center;
        margin-top: 1.5rem;
        animation: fadeUp 0.5s ease-out;
        position: relative;
        overflow: hidden;
    }
    .result-box::before {
        content: "";
        position: absolute;
        inset: 0;
        opacity: 0.5;
        background: radial-gradient(circle at 50% 0%, currentColor 0%, transparent 60%);
    }
    .result-box .icon-circle {
        width: 62px; height: 62px;
        border-radius: 50%;
        background: currentColor;
        display: flex; align-items: center; justify-content: center;
        margin: 0 auto 0.8rem auto;
        position: relative;
        z-index: 1;
    }
    .result-box .icon-circle span { font-size: 1.8rem; filter: grayscale(0) brightness(2); }
    .result-box .label {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.45rem;
        font-weight: 700;
        position: relative; z-index: 1;
    }
    .result-box .sub {
        font-size: 0.88rem;
        opacity: 0.8;
        margin-top: 0.3rem;
        position: relative; z-index: 1;
    }
    .spam-box { background: #ef44441a; border: 1px solid #ef444450; color: #f87171; }
    .ham-box { background: #10b9811a; border: 1px solid #10b98150; color: #34d399; }

    @keyframes fadeUp {
        from {opacity: 0; transform: translateY(14px);}
        to {opacity: 1; transform: translateY(0);}
    }

    .confidence-wrap { margin-top: 1.1rem; position: relative; z-index: 1; }
    .confidence-label {
        display: flex; justify-content: space-between;
        font-size: 0.8rem; color: #9aa4b2; margin-bottom: 0.35rem;
    }
    .confidence-bar-bg {
        background: #ffffff14;
        border-radius: 999px;
        height: 9px;
        overflow: hidden;
    }
    .confidence-bar-fill {
        height: 100%;
        border-radius: 999px;
        transition: width 0.7s cubic-bezier(.4,0,.2,1);
    }

    /* ============ FOOTER ============ */
    .footer {
        text-align: center;
        color: #3f4757;
        font-size: 0.76rem;
        margin-top: 3.2rem;
        padding: 1.2rem 0 0.6rem 0;
        border-top: 1px solid #ffffff0c;
    }
    </style>
""", unsafe_allow_html=True)

# ======================================================
# LOAD MODEL & VECTORIZER
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
# PREPROCESSING
# ======================================================
def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# ======================================================
# NAVBAR
# ======================================================
st.markdown("""
    <div class="navbar">
        <div class="navbar-brand">
            <div class="logo-box">🛡️</div>
            Spam Shield
        </div>
        <div class="navbar-tag">SVM + TF-IDF</div>
    </div>
""", unsafe_allow_html=True)

# ======================================================
# HERO
# ======================================================
st.markdown("""
    <div class="hero">
        <h1>Is this email trying<br>to fool you?</h1>
        <p>Tempel isi email di bawah, sistem akan menganalisis pola teksnya dan menentukan apakah email tersebut spam atau aman.</p>
    </div>
""", unsafe_allow_html=True)

if load_error:
    st.error(
        f"Gagal memuat model/vectorizer. Pastikan file "
        f"`spam_model_svm.pkl` dan `tfidf_vectorizer.pkl` ada di folder repo.\n\n"
        f"Detail error: {load_error}"
    )
    st.stop()

# ======================================================
# STAT PILLS
# ======================================================
st.markdown("""
    <div class="stats-row">
        <div class="stat-pill"><span class="num">98.3%</span><span class="lbl">Akurasi</span></div>
        <div class="stat-pill"><span class="num">5.171</span><span class="lbl">Data Latih</span></div>
        <div class="stat-pill"><span class="num">5.000</span><span class="lbl">Fitur TF-IDF</span></div>
    </div>
""", unsafe_allow_html=True)

# ======================================================
# LANGUAGE NOTICE
# ======================================================
st.markdown("""
    <div class="lang-notice">
        🌐 <span><b>Catatan penting:</b> model ini hanya dilatih dengan data berbahasa Inggris.
        Masukkan teks email dalam <b>Bahasa Inggris</b> agar hasil deteksi akurat — teks berbahasa lain
        kemungkinan besar tidak akan dikenali dengan benar.</span>
    </div>
""", unsafe_allow_html=True)

# ======================================================
# INPUT CARD
# ======================================================
st.markdown('<div class="input-card">', unsafe_allow_html=True)
st.markdown('<div class="card-label">✉️ Isi Email</div>', unsafe_allow_html=True)

user_input = st.text_area(
    "Isi email",
    height=210,
    placeholder="Example: Dear customer, you have won a prize... click this link to claim now!",
    label_visibility="collapsed",
)

check_btn = st.button("🔍  Analisis Email Sekarang")
st.markdown('</div>', unsafe_allow_html=True)

# ======================================================
# PREDIKSI
# ======================================================
if check_btn:
    if not user_input.strip():
        st.warning("⚠️ Tolong masukkan teks email terlebih dahulu.")
    else:
        with st.spinner("Menganalisis pola teks email..."):
            time.sleep(0.5)
            cleaned = clean_text(user_input)
            vectorized = tfidf.transform([cleaned])
            prediction = model.predict(vectorized)[0]

            confidence = None
            if hasattr(model, "predict_proba"):
                proba = model.predict_proba(vectorized)[0]
                confidence = max(proba) * 100
            elif hasattr(model, "decision_function"):
                score = model.decision_function(vectorized)[0]
                confidence = min(99.0, 50 + abs(score) * 15)

        label = str(prediction).lower()
        is_spam = label in ["spam", "1"]

        if is_spam:
            box_class, icon, title, sub = "spam-box", "🚨", "Terdeteksi SPAM", "Sebaiknya jangan klik tautan atau membalas email ini."
            bar_color = "linear-gradient(90deg, #ef4444, #f87171)"
        else:
            box_class, icon, title, sub = "ham-box", "✅", "Email Ini Aman", "Tidak ditemukan ciri-ciri email spam."
            bar_color = "linear-gradient(90deg, #10b981, #34d399)"

        confidence_html = ""
        if confidence is not None:
            confidence_html = f"""
                <div class="confidence-wrap">
                    <div class="confidence-label">
                        <span>Tingkat keyakinan</span>
                        <span><b>{confidence:.1f}%</b></span>
                    </div>
                    <div class="confidence-bar-bg">
                        <div class="confidence-bar-fill" style="width:{confidence}%; background:{bar_color};"></div>
                    </div>
                </div>
            """

        st.markdown(f"""
            <div class="result-box {box_class}">
                <div class="icon-circle"><span>{icon}</span></div>
                <div class="label">{title}</div>
                <div class="sub">{sub}</div>
                {confidence_html}
            </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            with st.expander("📄 Teks setelah diproses"):
                st.code(cleaned if cleaned else "(kosong — tidak ada kata dikenali)")
        with col2:
            with st.expander("🔧 Debug info"):
                st.write("Prediksi mentah:", prediction)
                if hasattr(model, "classes_"):
                    st.write("Kelas model:", model.classes_)
                st.write("Fitur non-zero:", vectorized.nnz, "/ 5000")
                if vectorized.nnz == 0:
                    st.error("Tidak ada kata dari input yang dikenali vectorizer.")

# ======================================================
# FOOTER
# ======================================================
st.markdown("""
    <div class="footer">
        Spam Shield · Dibuat dengan Streamlit · Model SVM + TF-IDF
    </div>
""", unsafe_allow_html=True)