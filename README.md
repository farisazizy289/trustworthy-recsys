# 🛒 Trustworthy E-Commerce Recommendation System

> SVD Collaborative Filtering + Fake Review Detection untuk rekomendasi yang tidak hanya personal, tapi juga terpercaya

![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat-square&logo=python)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.3+-orange?style=flat-square)
![Pandas](https://img.shields.io/badge/pandas-2.0+-green?style=flat-square)

---

## 🌏 Latar Belakang

Sistem rekomendasi hanya sebaik datanya. Jika review pengguna dipenuhi manipulasi — bintang 5 palsu untuk produk buruk, atau bintang 1 untuk menjatuhkan kompetitor — maka rekomendasi yang dihasilkan pun menyesatkan pengguna.

**Trustworthy Recsys** hadir dengan pendekatan berbeda: sebelum melatih model, sistem ini terlebih dahulu mendeteksi dan menetralisir review mencurigakan, sehingga sinyal yang digunakan untuk rekomendasi mencerminkan preferensi pengguna yang sesungguhnya.

---

## ✨ Fitur

- 🕵️ **Fake Review Detection** — 3 sinyal kecurangan: extreme-only reviewer, burst reviewer, dan duplicate text reviewer
- 🔐 **Trustworthy Interaction Matrix** — bobot interaksi dikalikan trust score user, bukan binary 0/1
- 🤖 **SVD Collaborative Filtering** — latent space 50 dimensi, lebih robust dari KNN pada sparse matrix
- 🔄 **Hybrid Recommendation** — gabungan SVD (70%) + popularity score (30%)
- 🆕 **Cold-Start Handler** — fallback ke popularity-based untuk user baru tanpa riwayat
- 📊 **Evaluasi Kuantitatif** — Precision@K, Recall@K, Catalog Coverage

---

## 🧠 Arsitektur & Pipeline

```
Raw Data (orders + reviews + products)
            ↓
    FAKE REVIEW DETECTION
    ┌─────────────────────────────────────┐
    │ Sinyal 1: Extreme-Only Reviewer     │
    │ → semua bintang 5 atau semua 1      │
    │                                     │
    │ Sinyal 2: Burst Reviewer            │
    │ → banyak review dalam < 1 hari      │
    │                                     │
    │ Sinyal 3: Duplicate Text Reviewer   │
    │ → teks review identik di banyak     │
    │   order berbeda                     │
    └─────────────────────────────────────┘
            ↓
    TRUST SCORE per user (0.0 - 1.0)
    trusted_score = review_score × trust_score
            ↓
    TRUSTWORTHY INTERACTION MATRIX
    (user × kategori, bobot trusted_score)
            ↓
    SVD COLLABORATIVE FILTERING
    (50 latent dimensions)
            ↓
    COSINE SIMILARITY antar kategori
            ↓
    HYBRID RECOMMENDATION
    (SVD 70% + Popularity 30%)
            ↓
    Rekomendasi Terpercaya
```

### Kenapa SVD, bukan KNN langsung?

| | KNN Biasa | SVD |
|---|---|---|
| Input | Sparse matrix (binary 0/1) | Dense latent space |
| Similarity | Mendekati 0 (vektor tegak lurus) | Meaningful cosine similarity |
| Skalabilitas | Lambat pada data besar | Efisien |
| Noise | Sensitif | Robust (dimensionality reduction) |

---

## 📊 Hasil Evaluasi

| Metrik | Standard | Trustworthy |
|---|---|---|
| Precision@5 | - | - |
| Recall@5 | - | - |
| Catalog Coverage | 93.88%+ | Terjaga |

> Nilai aktual ditampilkan di output notebook setelah training.

### Fake Review yang Terdeteksi

| Sinyal | Deskripsi |
|---|---|
| Extreme-Only | User yang 100% beri bintang 5 atau 100% bintang 1 |
| Burst | Banyak review dalam rentang waktu < 24 jam |
| Duplicate Text | Teks review identik dikirim ke multiple order |

---

## 🗂️ Struktur Project

```
trustworthy-recsys/
├── trustworthy_recsys.ipynb       # Notebook training lengkap
├── app.py                         # Streamlit web application
├── requirements.txt               # Python dependencies
├── svd_trusted_model.pkl          # Trained SVD model (trustworthy)
├── category_similarity_matrix.csv # Similarity matrix antar kategori
├── popularity_df.csv              # Popularity scores
├── trust_df.csv                   # Trust score per user
└── README.md                      # Dokumentasi ini
```

---

## 📦 Dataset

**Brazilian E-Commerce Public Dataset by Olist**
- Source: [Kaggle — olistbr](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- File yang digunakan:
  - `olist_orders_dataset.csv`
  - `olist_order_items_dataset.csv`
  - `olist_products_dataset.csv`
  - `olist_order_reviews_dataset.csv`
  - `olist_customers_dataset.csv`

---

## ⚙️ Training Pipeline

```
1. Load & join 5 tabel dataset
2. EDA — distribusi kategori, review score, aktivitas user
3. Fake Review Detection (3 sinyal)
4. Hitung trust score per user
5. Filter: user aktif >= 3 transaksi, kategori >= 5 user unik
6. Buat Trustworthy Interaction Matrix
   (trusted_score = review_score × trust_score)
7. SVD Truncated (50 komponen) pada trustworthy matrix
8. Cosine similarity antar kategori di latent space
9. Popularity scoring (frekuensi 60% + rata-rata score 40%)
10. Hybrid recommendation function
11. Evaluasi Precision@K, Recall@K, Catalog Coverage
12. Simpan model & artifacts
```

---

## 🚀 Cara Menjalankan

### Lokal

```bash
git clone https://github.com/farisazizy289/trustworthy-recsys.git
cd trustworthy-recsys

pip install -r requirements.txt
streamlit run app.py
```

---

## ⚠️ Limitasi & Catatan

- Model dilatih pada data e-commerce Brazil — pola perilaku pengguna bisa berbeda dengan konteks Indonesia
- Fake review detection berbasis heuristik — bukan ground truth label
- Threshold trust score bisa di-tune sesuai kebutuhan bisnis
- Cold-start problem masih ada untuk kategori baru yang belum punya interaksi

---

## 🔮 Pengembangan Selanjutnya

- [ ] Integrasi NLP untuk deteksi sentimen review text
- [ ] Real-time fake review flagging via API
- [ ] Personalized recommendation (user-level, bukan hanya category-level)
- [ ] A/B testing framework untuk bandingkan standard vs trustworthy
- [ ] Badge "Verified Review" di frontend

---

## 👤 Author

**Faris Azizy**
- GitHub: [@farisazizy289](https://github.com/farisazizy289)
- Portfolio: Apple Developer Academy Indonesia Applicant

---

## 📄 Lisensi

MIT License

---

> *"The goal is not just to recommend what users might like, but to recommend what they can trust."*
>
> Trustworthy Recsys dibangun dengan keyakinan bahwa kepercayaan pengguna adalah fondasi dari sistem rekomendasi yang baik.