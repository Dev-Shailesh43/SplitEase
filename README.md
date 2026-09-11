# SplitEase 2.0 — Campus FinTech & Intelligent Expense Minimization Platform

> **Production-grade, privacy-first peer-to-peer expense sharing, group ledger, and graph debt settlement engine built for campus communities and hackathons.**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![React 18](https://img.shields.io/badge/React-18.3-61DAFB?logo=react&logoColor=black)](https://reactjs.org)
[![Google Gemini](https://img.shields.io/badge/AI-Google_Gemini-4285F4?logo=google&logoColor=white)](https://ai.google.dev)
[![Firebase](https://img.shields.io/badge/Firebase-Sync_Active-FFCA28?logo=firebase&logoColor=black)](https://firebase.google.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🚀 Overview

SplitEase 2.0 replaces cumbersome traditional spreadsheets and legacy expense apps with an intelligent, privacy-first financial platform. It delivers real-time group pod management, bilateral direct settlements via dynamic Indian UPI QR codes, AI-assisted receipt auditing powered by Google Gemini, and automated graph debt minimization.

---

## ✨ Key Features

- **🛡️ Privacy-First Pod Isolation**: Campus members only see pods, expenses, and chats they are members of. No unauthorized data leakage across campus groups.
- **⚡ Bilateral Debt Minimization Engine**: Deterministic graph algorithm simplifies circular multi-party debts into the absolute minimum number of direct transactions.
- **📱 Dynamic Indian UPI QR Codes**: Generates standard NPCI-compliant UPI QR codes (`upi://pay?pa=...`) for instant settlement using GPay, PhonePe, Paytm, and BHIM.
- **🤖 Google Gemini AI Copilot & Receipt OCR**:
  - Natural language chatbot answering spending queries and budgeting questions.
  - OCR receipt scanner extracting merchant names, dates, categories, and itemized amounts from receipt images.
- **🔐 Multi-Role Access Control**: Granular roles (System Admin, Pod Owner, Pod Admin, Campus Member) with an Admin Portal for pod moderation and system telemetry.
- **💬 Real-Time Pod Chat & 1-on-1 Peer DMs**: Chat with roommates, travel companions, and friends with inline expense tagging and receipt attachments.
- **📂 Secure Campus Vault**: Group document repository for storing hotel vouchers, trip tickets, rental agreements, and bills.
- **🔄 Dual-Engine Architecture**: Local SQLite persistence with transactional consistency + real-time dual sync to Firebase Cloud Firestore.

---

## 🏛️ System Architecture

```text
┌────────────────────────────────────────────────────────────┐
│                    SplitEase 2.0 Web SPA                   │
│         (React 18 + Precision Neo-Brutalist Design)        │
└──────────────┬─────────────────────────────▲───────────────┘
               │ HTTP REST                   │ Realtime Sync
               ▼                             ▼
┌──────────────────────────────┐     ┌───────────────────────┐
│     Python Server Daemon     │     │   Firebase Firestore  │
│  Controllers → Repositories  │     │   (Dual Cloud Sync)   │
└──────────────┬───────────────┘     └───────────────────────┘
               │
      ┌────────┴────────┐
      ▼                 ▼
┌───────────┐     ┌──────────────┐
│  SQLite   │     │ Google Gemini│
│ Local DB  │     │  Flash API   │
└───────────┘     └──────────────┘
```

---

## 🛠️ Tech Stack

- **Frontend**: React 18, Chart.js, QRCode.js, Vanilla CSS Design System (Sharp-Corner Neo-Brutalist Fintech Aesthetic)
- **Backend**: Python HTTP Server (Modular Controller-Repository Pattern)
- **Database**: SQLite (`splitease_v2.db`) + Firebase Firestore Dual Sync
- **AI / OCR**: Google Gemini API (`gemini-flash-latest`)
- **Authentication**: Bearer token session protocol with salted SHA-256 password hashing

---

## 🏁 Quick Start

### 1. Prerequisites
- Python 3.10 or higher
- Modern Web Browser (Chrome, Edge, Firefox, Safari)

### 2. Run Application
```bash
# Clone the repository
git clone https://github.com/Dev-Shailesh43/SplitEase.git
cd SplitEase

# Start the full-stack server
python server.py
```

Open your browser and navigate to:
**`http://localhost:5000`**

---

## 🔑 Pre-Seeded Hackathon Accounts

| Role | Name | Email / Login | Password |
| :--- | :--- | :--- | :--- |
| **System Admin** | Aman Sharma | `aman@campus.edu` | `admin123` |
| **Campus Member** | Rahul Verma | `rahul@campus.edu` | `rahul123` |
| **Campus Member** | Priya Patel | `priya@campus.edu` | `priya123` |
| **Campus Member** | Rohit Sharma | `rohit@campus.edu` | `rohit123` |

*(You can also register brand new custom accounts with custom UPI IDs and passwords on the Sign Up tab).*

---

## 🧪 Automated Verification & Test Suite

Run the full end-to-end test suite:

```bash
# Privacy-first isolation policy test
python test_privacy_policy.py

# Authentication and session token test
python test_auth_system.py

# Settlement and account balance test
python test_account_settlement_apis.py

# End-to-end integration test
python test_e2e.py
```

---

## 📄 License

This project is licensed under the MIT License.
