# 🔍 Sales Drop Detective Dashboard

> **An investigative business analytics dashboard** that diagnoses *why* sales dropped — not just *that* they dropped. Built as a real business case study across 2 years, 5 regions, 6 categories, and 4 customer segments.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-name.streamlit.app)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-purple?logo=streamlit)
![Theme](https://img.shields.io/badge/Theme-Black%20×%20Purple%20×%20White-8B5CF6)

---

## 🌐 Live Demo

View: https://sales-drop-detective-dashboard-hycrsn6m7t5ummbpwtheaj.streamlit.app/

---

## 📸 What's Inside

| Tab | What It Shows |
|---|---|
| 📉 **Revenue Trend** | Monthly trend, MoM % change, profit vs revenue divergence, YoY table |
| 🗺️ **Regional Autopsy** | Region lines, heatmap, discount & return rate by region, YoY drop ranking |
| 📦 **Product & Category** | Area chart, YoY bar, top/bottom products, margin treemap |
| 👤 **Customer Deep-Dive** | Segment trends, bubble chart, channel P&L, discount vs return scatter |
| 🔎 **Detective Report** | 5 root-cause clues, evidence table, probability scores, verdict & action plan |

---

## 🚀 Deploy to Live URL (2 Minutes)

### Step 1 — Push to GitHub
```bash
git init
git add .
git commit -m "Initial deploy: Sales Drop Detective"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/sales-detective.git
git push -u origin main
```

### Step 2 — Deploy Free on Streamlit Community Cloud
1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Sign in with GitHub → click **"New app"**
3. Set:
   - **Repository:** `sales-detective`
   - **Branch:** `main`
   - **Main file:** `app.py`
4. Click **Deploy** — live in ~60 seconds ✅

---

## 💻 Run Locally
```bash
git clone https://github.com/YOUR_USERNAME/sales-detective
cd sales-detective
pip install -r requirements.txt
streamlit run app.py
# Opens at http://localhost:8501
```

---

## 🗂️ Project Structure
```
sales-detective/
├── app.py                  # Full app — single file, ~500 lines
├── requirements.txt
├── .streamlit/
│   └── config.toml         # Black × Purple × White theme
└── README.md
```

---

## 🎨 Design
- **Color Palette:** Pure black `#080810` · Deep purple `#7c3aed` · Lavender `#e9d5ff` · White
- **Fonts:** Playfair Display (headings) + Space Grotesk (body)
- **Style:** Editorial dark theme — forensic/investigative aesthetic

---

## 📊 Dataset
Synthetic 2-year sales dataset with **intentional drops injected** for detective storytelling:
- South region: −45% H2 2024
- Electronics: −40% H2 2024
- Corporate customers: −50% from Sept 2024

All generated inside the app via `numpy`/`pandas` — no CSV files needed.

---

## 🎯 Who This Is For
- 📁 Business analysts building a portfolio
- 🎤 Interviews demonstrating root-cause analytical thinking
- 🏫 MBA / data analytics capstone projects
- 💼 Anyone wanting a real-world dashboard to showcase

---

## 📄 License
MIT — free to use, fork, and customise.

---

<div align="center">
  <strong>Built with 🟣 Streamlit · Deploy free · No server needed</strong>
</div>
