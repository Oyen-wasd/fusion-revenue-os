# 🩺 Fusion Revenue OS — Campaign Doctor

**AI-Powered Diagnostic Layer for Multi-Brand E-Commerce Operations**

&gt; Built for Fusion Cosmetics | 26 Brands | 800 POS | Zero Blind Spots

---

## 🚨 The Problem

Fusion Cosmetics operates 26 e-commerce stores across multiple marketplaces and 800 POS locations. Current reporting is manual, fragmented, and answers "what happened" without explaining "why it happened" or "what to do next."

- **Mustela PMax** bleeds RM 1,115/month at 1.67x ROAS — but nobody knows if it's a creative problem or audience problem
- **Farah's live stream** hits 17.16x ROAS — but nobody knows if those are new customers or repeat buyers
- **NL Alchemist** keeps getting rebooked at 3.5x — but nobody knows if it's the streamer, the slot, or the product

## 🎯 The Solution

The **Campaign Doctor** is the first agent of the Revenue Operating System (ROS). It doesn't just record data. It diagnoses it.

### What It Does

| Feature | Business Impact |
|---|---|
| **Auto-Diagnosis** | Identifies bleeding campaigns, goldmines, and marginal performers in seconds |
| **Funnel-Stage Intelligence** | Knows if PMax is failing because of hook failure or landing page mismatch |
| **Live Session Analysis** | Finds the exact minute to front-load offers based on purchase timing |
| **Brand Portfolio View** | Flags internal cannibalization across 26 brands |
| **CEO Briefing** | Auto-generates daily 7 AM WhatsApp-ready summary |

## 🛠 Tech Stack

- **Frontend:** Streamlit (Python)
- **Visualization:** Plotly
- **Data Processing:** Pandas, NumPy
- **AI Layer:** Deterministic diagnostic engine (LLM enhancement in v0.2)
- **Deployment:** Streamlit Cloud (free tier)
- **Data Source:** CSV upload → API integration (Month 2)

## 📊 Live Demo

**[🚀 Open Campaign Doctor](https://YOUR-URL-HERE.streamlit.app)**

*(Replace with your actual Streamlit Cloud URL)*

## 🖼 Screenshots

![Campaign Diagnostic](https://via.placeholder.com/800x400?text=Campaign+Doctor+Screenshot)
![Live Session Analysis](https://via.placeholder.com/800x400?text=Live+Session+Analyst+Screenshot)

## 🗺 6-Agent ROS Roadmap

This POC deploys Agent 1: **Campaign Doctor**. The full Revenue Operating System includes:

1. ✅ **Campaign Doctor** (v0.1 — THIS BUILD)
2. 🔄 **Money Guardian** — Auto-pause sub-breakeven campaigns
3. 🔄 **Funnel Diagnostician** — Stage-specific failure analysis
4. 🔄 **Streamer Intelligence** — Temporal optimization for live commerce
5. 🔄 **Audience Archaeologist** — New vs. repeat buyer segmentation
6. 🔄 **CEO Briefing** — Daily automated decision briefings

## 🚀 Run Locally

```bash
git clone https://github.com/YOURUSERNAME/fusion-revenue-os.git
cd fusion-revenue-os
pip install -r requirements.txt
streamlit run app.py
