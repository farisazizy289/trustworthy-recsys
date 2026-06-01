import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Trustworthy RecSys",
    page_icon="🔒",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# CATEGORY TRANSLATION MAP
# ─────────────────────────────────────────────
CATEGORY_MAP = {
    "agro_industria_e_comercio":             {"en": "Agro Industry & Trade",          "id": "Industri & Perdagangan Agro"},
    "alimentos":                             {"en": "Food",                            "id": "Makanan"},
    "alimentos_bebidas":                     {"en": "Food & Beverages",               "id": "Makanan & Minuman"},
    "artes":                                 {"en": "Arts & Crafts",                  "id": "Seni & Kerajinan"},
    "artigos_de_natal":                      {"en": "Christmas Articles",             "id": "Perlengkapan Natal"},
    "audio":                                 {"en": "Audio",                          "id": "Audio"},
    "automotivo":                            {"en": "Automotive",                     "id": "Otomotif"},
    "bebes":                                 {"en": "Babies",                         "id": "Perlengkapan Bayi"},
    "beleza_saude":                          {"en": "Beauty & Health",                "id": "Kecantikan & Kesehatan"},
    "brinquedos":                            {"en": "Toys",                           "id": "Mainan"},
    "cama_mesa_banho":                       {"en": "Bed, Table & Bath",             "id": "Kasur, Meja & Kamar Mandi"},
    "casa_conforto":                         {"en": "Home Comfort",                   "id": "Kenyamanan Rumah"},
    "casa_construcao":                       {"en": "Home Construction",              "id": "Konstruksi Rumah"},
    "construcao_ferramentas_construcao":     {"en": "Construction Tools",             "id": "Alat Konstruksi"},
    "construcao_ferramentas_ferramentas":    {"en": "Hardware Tools",                 "id": "Perkakas"},
    "construcao_ferramentas_iluminacao":     {"en": "Lighting Tools",                 "id": "Alat Penerangan"},
    "construcao_ferramentas_jardim":         {"en": "Garden Tools",                   "id": "Alat Taman"},
    "construcao_ferramentas_seguranca":      {"en": "Safety Tools",                   "id": "Alat Keamanan"},
    "eletrodomesticos":                      {"en": "Home Appliances",                "id": "Peralatan Rumah Tangga"},
    "eletrodomesticos_2":                    {"en": "Home Appliances II",             "id": "Peralatan Rumah Tangga II"},
    "eletronicos":                           {"en": "Electronics",                    "id": "Elektronik"},
    "esporte_lazer":                         {"en": "Sports & Leisure",               "id": "Olahraga & Rekreasi"},
    "fashion_bolsas_e_acessorios":           {"en": "Fashion Bags & Accessories",     "id": "Tas & Aksesori Fashion"},
    "fashion_calcados":                      {"en": "Fashion Footwear",               "id": "Alas Kaki Fashion"},
    "fashion_esporte":                       {"en": "Sports Fashion",                 "id": "Fashion Olahraga"},
    "fashion_roupa_feminina":                {"en": "Women's Fashion",                "id": "Fashion Wanita"},
    "fashion_roupa_masculina":               {"en": "Men's Fashion",                  "id": "Fashion Pria"},
    "ferramentas_jardim":                    {"en": "Garden & Tools",                 "id": "Taman & Perkakas"},
    "flores":                                {"en": "Flowers",                        "id": "Bunga"},
    "fraldas_higiene":                       {"en": "Diapers & Hygiene",              "id": "Popok & Kebersihan"},
    "informatica_acessorios":                {"en": "Computer Accessories",           "id": "Aksesori Komputer"},
    "instrumentos_musicais":                 {"en": "Musical Instruments",            "id": "Alat Musik"},
    "livros_interesse_geral":                {"en": "General Interest Books",         "id": "Buku Umum"},
    "livros_tecnicos":                       {"en": "Technical Books",                "id": "Buku Teknis"},
    "malas_acessorios":                      {"en": "Luggage & Accessories",          "id": "Koper & Aksesori"},
    "market_place":                          {"en": "Marketplace",                    "id": "Marketplace"},
    "moveis_decoracao":                      {"en": "Furniture & Decoration",         "id": "Furnitur & Dekorasi"},
    "moveis_escritorio":                     {"en": "Office Furniture",               "id": "Furnitur Kantor"},
    "moveis_sala":                           {"en": "Living Room Furniture",          "id": "Furnitur Ruang Tamu"},
    "musica":                                {"en": "Music",                          "id": "Musik"},
    "papelaria":                             {"en": "Stationery",                     "id": "Alat Tulis"},
    "pc_gamer":                              {"en": "PC Gamer",                       "id": "PC Gaming"},
    "perfumaria":                            {"en": "Perfumery",                      "id": "Parfum"},
    "pet_shop":                              {"en": "Pet Shop",                       "id": "Toko Hewan Peliharaan"},
    "relogios_presentes":                    {"en": "Watches & Gifts",                "id": "Jam Tangan & Hadiah"},
    "tablets_impressao_imagem":              {"en": "Tablets & Image Printing",       "id": "Tablet & Cetak Gambar"},
    "telefonia":                             {"en": "Telephony",                      "id": "Telepon & Komunikasi"},
    "utilidades_domesticas":                 {"en": "Household Utilities",            "id": "Peralatan Rumah Tangga"},
    "utilidades_domesticas_2":              {"en": "Household Utilities II",          "id": "Peralatan Rumah Tangga II"},
}

def translate(raw_name, lang):
    entry = CATEGORY_MAP.get(raw_name)
    if entry:
        return entry[lang]
    return raw_name.replace("_", " ").title()

def raw_from_display(display_name, lang, all_cats):
    for raw in all_cats:
        if translate(raw, lang) == display_name:
            return raw
    return display_name

# ─────────────────────────────────────────────
# CSS — inherits dark aesthetic from Olist app
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Sora', sans-serif;
    background: #07090f;
}
.block-container { padding: 3rem 2rem 4rem !important; max-width: 760px; }

.app-header { text-align: center; margin-bottom: 2rem; }
.app-title  { font-size: 28px; font-weight: 700; color: #f1f5f9; letter-spacing: -0.5px; margin: 0 0 6px; }
.app-sub    { font-size: 13px; color: #475569; margin: 0; }
.app-badge  {
    display: inline-block; font-size: 10px;
    font-family: 'JetBrains Mono', monospace;
    color: #38bdf8; background: #0c1929;
    border: 1px solid #1e3a5f; border-radius: 99px;
    padding: 3px 12px; margin-top: 10px; letter-spacing: 0.05em;
}
.badge-trust {
    display: inline-block; font-size: 10px;
    font-family: 'JetBrains Mono', monospace;
    color: #4ade80; background: #0c1a0c;
    border: 1px solid #166534; border-radius: 99px;
    padding: 3px 12px; margin-top: 6px; margin-left: 6px; letter-spacing: 0.05em;
}
.divider { border: none; border-top: 1px solid #0f172a; margin: 1.6rem 0; }
.control-label {
    font-size: 11px; font-weight: 500; color: #475569;
    text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px;
}
.lang-note {
    font-size: 11px; color: #334155;
    margin: -8px 0 14px;
    font-family: 'JetBrains Mono', monospace;
}

/* Result */
.result-header { display: flex; align-items: center; gap: 10px; margin: 1.2rem 0 0.8rem; }
.result-title  { font-size: 13px; font-weight: 600; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.08em; }
.result-type-badge {
    font-size: 10px; font-family: 'JetBrains Mono', monospace;
    padding: 3px 10px; border-radius: 99px; letter-spacing: 0.04em;
}
.rec-item {
    display: flex; align-items: center; padding: 13px 18px;
    background: #0d1117; border: 1px solid #0f172a;
    border-radius: 10px; margin-bottom: 6px;
}
.rec-rank  { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #334155; width: 28px; flex-shrink: 0; }
.rec-main  { flex: 1; }
.rec-name  { font-size: 14px; color: #e2e8f0; font-weight: 500; margin: 0 0 2px; }
.rec-raw   { font-size: 11px; color: #334155; font-family: 'JetBrains Mono', monospace; margin: 0; }
.rec-right { display: flex; align-items: center; gap: 10px; }
.rec-score { font-family: 'JetBrains Mono', monospace; font-size: 13px; color: #38bdf8; font-weight: 500; }
.score-bar-wrap { width: 70px; height: 4px; background: #0f172a; border-radius: 99px; overflow: hidden; }
.score-bar-fill { height: 100%; border-radius: 99px; background: linear-gradient(90deg, #1e40af, #38bdf8); }

.breakdown-row { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; margin-top: 1.2rem; }
.bd-card { background: #0d1117; border: 1px solid #0f172a; border-radius: 10px; padding: 14px 16px; text-align: center; }
.bd-val  { font-family: 'JetBrains Mono', monospace; font-size: 20px; font-weight: 500; margin: 0 0 4px; }
.bd-lbl  { font-size: 11px; color: #475569; margin: 0; text-transform: uppercase; letter-spacing: 0.06em; }
.bd-sub  { font-size: 10px; color: #334155; margin: 3px 0 0; }

/* Trust stats */
.trust-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; margin: 1rem 0; }
.trust-card { background: #0d1117; border: 1px solid #0f172a; border-radius: 10px; padding: 14px 16px; text-align: center; }
.trust-val  { font-family: 'JetBrains Mono', monospace; font-size: 22px; font-weight: 500; margin: 0 0 4px; }
.trust-lbl  { font-size: 11px; color: #475569; margin: 0; text-transform: uppercase; letter-spacing: 0.06em; }
.trust-sub  { font-size: 10px; color: #334155; margin: 3px 0 0; }

.info-box  { background: #0d1117; border: 1px solid #0f172a; border-radius: 10px; padding: 16px 18px; margin-top: 1.5rem; }
.info-row  { display: flex; gap: 10px; align-items: flex-start; margin-bottom: 8px; font-size: 12px; line-height: 1.6; color: #64748b; }
.info-row:last-child { margin-bottom: 0; }
.info-key  { font-family: 'JetBrains Mono', monospace; color: #38bdf8; white-space: nowrap; flex-shrink: 0; min-width: 130px; }

.empty-state { text-align: center; padding: 3rem 2rem; color: #334155; font-size: 13px; }
.empty-icon  { font-size: 32px; margin-bottom: 10px; }

.section-label {
    font-size: 11px; font-weight: 600; color: #475569;
    text-transform: uppercase; letter-spacing: 0.1em;
    margin: 0 0 10px; display: flex; align-items: center; gap: 8px;
}
.section-label::after {
    content: ''; flex: 1; height: 1px; background: #0f172a;
}

.stButton > button {
    background: #0f172a !important; border: 1px solid #1e293b !important;
    color: #e2e8f0 !important; font-family: 'Sora', sans-serif !important;
    font-size: 13px !important; font-weight: 500 !important;
    border-radius: 8px !important; padding: 0.55rem 1.5rem !important;
    width: 100% !important; transition: all 0.2s !important;
}
.stButton > button:hover { background: #1e293b !important; border-color: #334155 !important; }
.stButton > button[kind="primary"] { background: #0c1929 !important; border-color: #1e3a5f !important; color: #38bdf8 !important; }
.stButton > button[kind="primary"]:hover { background: #112240 !important; border-color: #38bdf8 !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DATA LOADER — tries real artifacts first,
# falls back to synthetic demo data
# ─────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data():
    import os

    # ── Try loading real artifacts ──────────────────────────────────────
    try:
        trusted_sim  = pd.read_csv("artifacts/category_similarity_trusted_matrix.csv", index_col=0)
        popularity   = pd.read_csv("artifacts/category_popularity.csv")
        trust_scores = pd.read_csv("artifacts/user_trust_scores.csv")

        pop_df = popularity.copy()
        if "popularity_score" not in pop_df.columns:
            max_p = pop_df["total_purchase"].max()
            max_s = pop_df["avg_score"].max()
            pop_df["popularity_score"] = (
                0.7 * pop_df["total_purchase"] / max_p
                + 0.3 * pop_df["avg_score"] / max_s
            ).round(4)

        pop_df = pop_df.sort_values("popularity_score", ascending=False).reset_index(drop=True)
        pop_scores  = dict(zip(pop_df["product_category_name"], pop_df["popularity_score"]))
        all_cats    = sorted(trusted_sim.index.tolist())
        return pop_df, trusted_sim, pop_scores, all_cats, trust_scores, False  # False = not demo

    except Exception:
        pass  # fall through to demo data

    # ── Synthetic demo data ─────────────────────────────────────────────
    popularity_data = {
        "product_category_name": [
            "moveis_decoracao","cama_mesa_banho","informatica_acessorios",
            "utilidades_domesticas","esporte_lazer","beleza_saude",
            "ferramentas_jardim","relogios_presentes","moveis_escritorio",
            "automotivo","telefonia","brinquedos","artigos_de_natal",
            "bebes","eletronicos","pet_shop","papelaria","flores",
            "perfumaria","audio",
        ],
        "total_purchase": [1875,1624,1071,986,812,696,676,332,393,272,250,230,200,180,160,140,120,100,90,80],
        "avg_score":      [3.54,3.50,3.34,3.53,3.65,3.81,3.52,3.56,3.21,3.86,3.40,3.70,3.60,3.80,3.30,3.90,3.50,4.00,3.75,3.45],
    }
    pop_df = pd.DataFrame(popularity_data)
    max_p  = pop_df["total_purchase"].max()
    max_s  = pop_df["avg_score"].max()
    pop_df["popularity_score"] = (
        0.7 * pop_df["total_purchase"] / max_p
        + 0.3 * pop_df["avg_score"] / max_s
    ).round(4)
    pop_df = pop_df.sort_values("popularity_score", ascending=False).reset_index(drop=True)

    categories = list(CATEGORY_MAP.keys())
    n = len(categories)
    np.random.seed(42)
    raw = np.random.rand(n, n) * 0.025
    sim = (raw + raw.T) / 2
    np.fill_diagonal(sim, 1.0)
    cat_idx = {c: i for i, c in enumerate(categories)}
    known = {
        ("agro_industria_e_comercio", "moveis_decoracao"):    0.0241,
        ("agro_industria_e_comercio", "utilidades_domesticas"): 0.0133,
        ("alimentos", "moveis_decoracao"):                    0.0156,
        ("alimentos", "esporte_lazer"):                       0.0324,
        ("alimentos", "beleza_saude"):                        0.0239,
        ("alimentos_bebidas", "utilidades_domesticas"):        0.0389,
        ("alimentos_bebidas", "esporte_lazer"):               0.0430,
        ("alimentos_bebidas", "beleza_saude"):                0.0353,
        ("cama_mesa_banho", "moveis_decoracao"):              0.0312,
        ("cama_mesa_banho", "utilidades_domesticas"):         0.0285,
        ("esporte_lazer", "beleza_saude"):                    0.0198,
        ("esporte_lazer", "moveis_decoracao"):                0.0167,
        ("informatica_acessorios", "eletronicos"):            0.0421,
        ("informatica_acessorios", "telefonia"):              0.0389,
        ("beleza_saude", "perfumaria"):                       0.0456,
        ("beleza_saude", "fraldas_higiene"):                  0.0312,
    }
    for (a, b), v in known.items():
        if a in cat_idx and b in cat_idx:
            sim[cat_idx[a]][cat_idx[b]] = v
            sim[cat_idx[b]][cat_idx[a]] = v

    sim_df = pd.DataFrame(sim, index=categories, columns=categories)
    pop_scores = dict(zip(pop_df["product_category_name"], pop_df["popularity_score"]))

    # Synthetic trust scores
    np.random.seed(0)
    n_users = 10000
    trust_vals = np.random.choice(
        [1.0, 0.5, 0.1],
        size=n_users,
        p=[0.72, 0.18, 0.10]
    )
    trust_df_demo = pd.DataFrame({
        "customer_unique_id": [f"user_{i:05d}" for i in range(n_users)],
        "trust_score": trust_vals
    })

    return pop_df, sim_df, pop_scores, categories, trust_df_demo, True  # True = demo


def hybrid_recommend(category_name, similarity_df, pop_scores, popularity_df,
                     n=5, cf_w=0.7, pop_w=0.3):
    if category_name is None or category_name not in similarity_df.index:
        result = popularity_df.head(n)[["product_category_name","popularity_score"]].copy()
        result.columns = ["category","score"]
        result["cf_score"]  = 0.0
        result["pop_score"] = result["score"]
        result["type"] = "popularity"
        return result.reset_index(drop=True)

    cf_scores = (
        similarity_df[category_name]
        .drop(index=category_name)
        .sort_values(ascending=False)
        .head(n * 4)
    )
    blended = []
    for cat, cf_s in cf_scores.items():
        p_s = pop_scores.get(cat, 0)
        blended.append({
            "category" : cat,
            "cf_score" : round(float(cf_s), 4),
            "pop_score": round(float(p_s), 4),
            "score"    : round(cf_w * float(cf_s) + pop_w * float(p_s), 4),
            "type"     : "hybrid"
        })
    return (
        pd.DataFrame(blended)
        .sort_values("score", ascending=False)
        .head(n)
        .reset_index(drop=True)
    )


# ─────────────────────────────────────────────
# LOAD
# ─────────────────────────────────────────────
with st.spinner(""):
    popularity_df, similarity_df, pop_scores, all_categories, trust_df, is_demo = load_data()

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <p class="app-title">🔒 Trustworthy RecSys</p>
    <p class="app-sub">Product Category Recommendation · Filtered from Fake Reviews</p>
    <span class="app-badge">Hybrid · SVD + Popularity</span>
    <span class="badge-trust">Trust-Weighted CF</span>
</div>
""", unsafe_allow_html=True)

if is_demo:
    st.markdown("""
    <div style="background:#1a1200;border:1px solid #854f0b;border-radius:8px;
                padding:10px 16px;font-size:12px;color:#fac775;margin-bottom:1rem;
                font-family:'JetBrains Mono',monospace;">
        ⚠ Demo mode · artifacts/ folder tidak ditemukan · menggunakan data sintetik
    </div>
    """, unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LANGUAGE SELECTOR
# ─────────────────────────────────────────────
st.markdown('<p class="control-label">Bahasa Kategori</p>', unsafe_allow_html=True)
lang_col1, lang_col2, _ = st.columns([1, 1, 3])
with lang_col1:
    lang_id = st.button(
        "Indonesia", key="btn_id",
        type="primary" if st.session_state.get("lang","id") == "id" else "secondary"
    )
with lang_col2:
    lang_en = st.button(
        "English", key="btn_en",
        type="primary" if st.session_state.get("lang","id") == "en" else "secondary"
    )

if lang_id:
    st.session_state["lang"] = "id"
if lang_en:
    st.session_state["lang"] = "en"

lang = st.session_state.get("lang", "id")
lang_label = "Indonesia" if lang == "id" else "English"
st.markdown(
    f'<p class="lang-note">· Bahasa aktif: <b>{lang_label}</b></p>',
    unsafe_allow_html=True
)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CONTROLS
# ─────────────────────────────────────────────
st.markdown('<p class="control-label">Tipe User</p>', unsafe_allow_html=True)
user_type = st.radio(
    "", ["🆕 User Baru", "👤 User Lama"],
    horizontal=True, label_visibility="collapsed"
)

selected_raw = None
if user_type == "👤 User Lama":
    st.markdown('<p class="control-label" style="margin-top:1rem;">Kategori Terakhir Dibeli</p>', unsafe_allow_html=True)

    # Only show categories that exist in the similarity matrix
    valid_cats = [c for c in all_categories if c in similarity_df.index]
    display_options = sorted([translate(c, lang) for c in valid_cats])
    selected_display = st.selectbox("", options=display_options, label_visibility="collapsed")
    selected_raw = raw_from_display(selected_display, lang, valid_cats)

    other_lang      = "en" if lang == "id" else "id"
    other_label     = translate(selected_raw, other_lang)
    other_lang_name = "English" if other_lang == "en" else "Indonesia"
    st.markdown(
        f'<p class="lang-note">· {other_lang_name}: <b>{other_label}</b>'
        f' &nbsp;·&nbsp; raw: <b>{selected_raw}</b></p>',
        unsafe_allow_html=True
    )

col1, col2 = st.columns(2)
with col1:
    st.markdown('<p class="control-label" style="margin-top:1rem;">Jumlah Rekomendasi</p>', unsafe_allow_html=True)
    n_rec = st.slider("", 3, 10, 5, label_visibility="collapsed")
with col2:
    st.markdown('<p class="control-label" style="margin-top:1rem;">Bobot Collaborative Filtering</p>', unsafe_allow_html=True)
    cf_w = st.slider("", 0.0, 1.0, 0.7, 0.1, label_visibility="collapsed")

pop_w = round(1.0 - cf_w, 1)
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
run = st.button("Tampilkan Rekomendasi", type="primary")

# ─────────────────────────────────────────────
# RESULTS
# ─────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)

if not run:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">🎯</div>
        Pilih tipe user dan klik <b>Tampilkan Rekomendasi</b>
    </div>
    """, unsafe_allow_html=True)
else:
    results = hybrid_recommend(
        selected_raw if user_type == "👤 User Lama" else None,
        similarity_df, pop_scores, popularity_df,
        n=n_rec, cf_w=cf_w, pop_w=pop_w
    )

    rec_type = results["type"].iloc[0]
    is_cold  = rec_type == "popularity"

    if is_cold:
        badge_html = (
            '<span class="result-type-badge" style="background:#0c1a0c;'
            'color:#4ade80;border:1px solid #166534;">popularity-based</span>'
        )
        sub_text = "Menampilkan kategori terpopuler untuk user baru"
    else:
        seed_display = translate(selected_raw, lang)
        badge_html = (
            '<span class="result-type-badge" style="background:#0c1929;'
            'color:#38bdf8;border:1px solid #1e3a5f;">hybrid · CF + popularity</span>'
        )
        sub_text = f"Berdasarkan pola pembelian: <b style='color:#e2e8f0;'>{seed_display}</b>"

    st.markdown(f"""
    <div class="result-header">
        <span class="result-title">Rekomendasi</span>
        {badge_html}
    </div>
    <p style="font-size:12px;color:#475569;margin:-4px 0 16px;">
        {sub_text} &nbsp;·&nbsp; CF {cf_w} + Pop {pop_w}
    </p>
    """, unsafe_allow_html=True)

    max_score = results["score"].max() if results["score"].max() > 0 else 1
    for i, row in results.iterrows():
        bar_pct      = int((row["score"] / max_score) * 100)
        display_name = translate(row["category"], lang)
        raw_name     = row["category"]
        other_lang   = "en" if lang == "id" else "id"
        other_name   = translate(raw_name, other_lang)

        st.markdown(f"""
        <div class="rec-item">
            <span class="rec-rank">#{i+1:02d}</span>
            <div class="rec-main">
                <p class="rec-name">{display_name}</p>
                <p class="rec-raw">{other_name} &nbsp;·&nbsp; {raw_name}</p>
            </div>
            <div class="rec-right">
                <div class="score-bar-wrap">
                    <div class="score-bar-fill" style="width:{bar_pct}%;"></div>
                </div>
                <span class="rec-score">{row['score']:.4f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Score breakdown (top result)
    top = results.iloc[0]
    st.markdown(f"""
    <div class="breakdown-row">
        <div class="bd-card">
            <p class="bd-val" style="color:#38bdf8;">{top['cf_score']:.4f}</p>
            <p class="bd-lbl">CF Score</p>
            <p class="bd-sub">kemiripan pola belanja</p>
        </div>
        <div class="bd-card">
            <p class="bd-val" style="color:#818cf8;">{top['pop_score']:.4f}</p>
            <p class="bd-lbl">Popularity</p>
            <p class="bd-sub">seberapa laris kategori</p>
        </div>
        <div class="bd-card">
            <p class="bd-val" style="color:#4ade80;">{top['score']:.4f}</p>
            <p class="bd-lbl">Hybrid Score</p>
            <p class="bd-sub">skor akhir rekomendasi #1</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Chart
    st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)
    plt.rcParams.update({
        "figure.facecolor": "#0d1117", "axes.facecolor": "#0d1117",
        "axes.edgecolor": "#0f172a",   "axes.labelcolor": "#475569",
        "xtick.color": "#334155",      "ytick.color": "#475569",
        "text.color": "#94a3b8",       "grid.color": "#0f172a",
        "grid.linestyle": "--",
    })
    fig, ax = plt.subplots(figsize=(7, 3.2))
    labels = [
        (translate(r["category"], lang)[:22] + "…"
         if len(translate(r["category"], lang)) > 22
         else translate(r["category"], lang))
        for _, r in results.iterrows()
    ]
    if not is_cold:
        cf_contrib  = results["cf_score"] * cf_w
        pop_contrib = results["pop_score"] * pop_w
        ax.barh(labels[::-1], cf_contrib.values[::-1],
                color="#1e40af", height=0.5, label=f"CF × {cf_w}")
        ax.barh(labels[::-1], pop_contrib.values[::-1],
                color="#0c4a6e", height=0.5, left=cf_contrib.values[::-1],
                label=f"Pop × {pop_w}")
        ax.legend(fontsize=9, framealpha=0, labelcolor="#64748b")
    else:
        ax.barh(labels[::-1], results["score"].values[::-1],
                color="#166534", height=0.5)

    ax.set_xlabel("Score", fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", labelsize=9)
    ax.tick_params(axis="x", labelsize=9)
    ax.xaxis.grid(True, alpha=0.3)
    ax.set_axisbelow(True)
    fig.tight_layout(pad=1.5)
    st.pyplot(fig)
    plt.close()

    # Method info box
    st.markdown("""
    <div class="info-box">
        <div class="info-row">
            <span class="info-key">CF Score</span>
            <span>Kemiripan pola pembelian antar kategori — dihitung dari Truncated SVD di latent space, <b>hanya dari user terpercaya</b>.</span>
        </div>
        <div class="info-row">
            <span class="info-key">Popularity</span>
            <span>Seberapa laris kategori tersebut — 70% frekuensi pembelian + 30% rata-rata review bersih.</span>
        </div>
        <div class="info-row">
            <span class="info-key">Hybrid Score</span>
            <span>Skor akhir gabungan · semakin tinggi = tampil lebih atas dalam daftar rekomendasi.</span>
        </div>
        <div class="info-row">
            <span class="info-key">Trust Filter</span>
            <span>User dengan pola review mencurigakan diberi bobot rendah (0.1–0.9) sehingga tidak mengkontaminasi model CF.</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TRUST SCORE STATISTICS (always visible)
# ─────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<p class="section-label">📊 Statistik Trust Score User</p>', unsafe_allow_html=True)

n_clean    = int((trust_df["trust_score"] == 1.0).sum())
n_suspect  = int((trust_df["trust_score"] < 1.0).sum())
n_untrust  = int((trust_df["trust_score"] == 0.1).sum())
total      = len(trust_df)

pct_clean   = n_clean / total * 100
pct_suspect = n_suspect / total * 100
pct_untrust = n_untrust / total * 100

st.markdown(f"""
<div class="trust-grid">
    <div class="trust-card">
        <p class="trust-val" style="color:#4ade80;">{n_clean:,}</p>
        <p class="trust-lbl">User Bersih</p>
        <p class="trust-sub">trust = 1.0 &nbsp;·&nbsp; {pct_clean:.1f}%</p>
    </div>
    <div class="trust-card">
        <p class="trust-val" style="color:#fac775;">{n_suspect:,}</p>
        <p class="trust-lbl">Mencurigakan</p>
        <p class="trust-sub">trust &lt; 1.0 &nbsp;·&nbsp; {pct_suspect:.1f}%</p>
    </div>
    <div class="trust-card">
        <p class="trust-val" style="color:#f87171;">{n_untrust:,}</p>
        <p class="trust-lbl">Tidak Dipercaya</p>
        <p class="trust-sub">trust = 0.1 &nbsp;·&nbsp; {pct_untrust:.1f}%</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Distribution table
dist = (
    trust_df["trust_score"]
    .value_counts()
    .sort_index(ascending=False)
    .reset_index()
)
dist.columns = ["Trust Score", "Jumlah User"]
dist["Persentase"] = (dist["Jumlah User"] / total * 100).map(lambda x: f"{x:.2f}%")

st.dataframe(
    dist,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Trust Score":  st.column_config.NumberColumn(format="%.2f"),
        "Jumlah User":  st.column_config.NumberColumn(format="%d"),
        "Persentase":   st.column_config.TextColumn(),
    }
)

# Trust distribution bar chart
plt.rcParams.update({
    "figure.facecolor": "#0d1117", "axes.facecolor": "#0d1117",
    "axes.edgecolor": "#0f172a",   "axes.labelcolor": "#475569",
    "xtick.color": "#475569",      "ytick.color": "#475569",
    "text.color": "#94a3b8",       "grid.color": "#0f172a",
    "grid.linestyle": "--",
})
fig2, ax2 = plt.subplots(figsize=(7, 2.2))
color_map = {1.0: "#166534", 0.5: "#854f0b", 0.1: "#7f1d1d"}
x_vals  = dist["Trust Score"].tolist()
y_vals  = dist["Jumlah User"].tolist()
colors  = [color_map.get(float(v), "#334155") for v in x_vals]
ax2.bar([str(v) for v in x_vals], y_vals, color=colors, width=0.5)
ax2.set_xlabel("Trust Score", fontsize=9)
ax2.set_ylabel("Jumlah User", fontsize=9)
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.yaxis.grid(True, alpha=0.3)
ax2.set_axisbelow(True)
fig2.tight_layout(pad=1.2)
st.pyplot(fig2)
plt.close()

# Info footnote
st.markdown("""
<div class="info-box" style="margin-top:0.8rem;">
    <div class="info-row">
        <span class="info-key">trust = 1.0</span>
        <span>User dengan pola review normal — kontribusi penuh ke model CF.</span>
    </div>
    <div class="info-row">
        <span class="info-key">trust &lt; 1.0</span>
        <span>Terdeteksi anomali (review cepat, rating ekstrem, dll) — bobotnya dikurangi proporsional.</span>
    </div>
    <div class="info-row">
        <span class="info-key">trust = 0.1</span>
        <span>Pola sangat mencurigakan — hampir tidak berkontribusi ke matrix CF yang digunakan.</span>
    </div>
</div>
""", unsafe_allow_html=True)