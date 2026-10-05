# SYNTHSOMA &mdash; Clinical Reference Intelligence Platform

SynthSoma is a full-stack Python Flask and Machine Learning healthcare reference web application. It integrates four logically independent clinical inference and reference modules backed by pre-trained machine learning architectures, real clinical datasets, persistent relational databases, authenticated user sessions, role-based administration, automated branded PDF report generation, and CSV data export capabilities.

---

## 🌟 Core Modules

### 1. Disease Prediction Engine
- **Input**: User selects or inputs symptoms from a 131-symptom feature space.
- **Model**: `models/ml/complete_disease_system.pkl` and `models/ml/disease_system_encoder.pkl`.
- **Classifiers Supported**:
  - K-Nearest Neighbors (Cosine) *(Default calibrated standard)*
  - Random Forest Classifier
  - Multinomial Naive Bayes
  - Logistic Regression
  - Support Vector Machine (SVC)
  - XGBoost Classifier
- **Output**: Predicted disease pathology, calibrated confidence score (where supported), symptom breakdown, cross-referenced precautions, risk factors, epidemiological occurrence, and reference pharmaceutical compounds.

### 2. Medicine Reference Engine
- **Input**: Disease / pathology name string.
- **Model**: `models/ml/medicine_by_disease_model.pkl` and `models/ml/medicine_encoder.pkl`.
- **Architecture**: MultiOutput Classifier over fitted TF-IDF vectorizer (ngram range 1-2) with MultiLabelBinarizer decoding (62 medicine classes).
- **Output**: Reference medicine formulations, active chemical compositions, and clinical descriptions from the built-in pharmaceutical catalog.
- **Medical Compliance**: Non-prescriptive reference protocol with clear health disclaimers; no synthetic dosages are fabricated.

### 3. Suggest Precaution Engine
- **Input**: Disease name string.
- **Model**: `models/ml/disease_precaution_model.pkl` and `models/ml/precaution_encoder.pkl`.
- **Architecture**: MultiOutput Classifier over TF-IDF vectorizer (ngram range 1-2) with MultiLabelBinarizer decoding (96 precaution classes).
- **Output**: Actionable clinical and lifestyle precautions, preventive self-care guidelines, and daily hygiene recommendations.

### 4. Analyse Risk Factor Engine
- **Input**: Disease name string.
- **Model**: `models/ml/disease_risk_model.pkl` and `models/ml/disease_risk_encoder.pkl`.
- **Architecture**: Cosine Nearest Neighbors (n_neighbors=1) using character n-gram TF-IDF vectorization (char_wb, ngram range 2-4).
- **Output**: Matched disease profile, cosine similarity score, primary clinical risk factors, and epidemiological occurrence frequencies across 100 comprehensive profiles.

---

## 🔒 Authentication & Access Control

- **Registration Fields**: Full Name, unique User ID, Gmail / Email (unique), Phone Number, Location, Password, and Password Confirmation.
- **Password Security**: Passwords are securely hashed with PBKDF2/SHA256 via Werkzeug (`generate_password_hash`). Plain-text passwords are never stored or displayed.
- **Access Gating**: All prediction engines, history logs, PDF downloads, and CSV exports require authentication (`@login_required`).
- **User Dashboard**: Registered users manage personal predictions, download PDF reports, export personal CSV logs, update profiles, and change passwords.
- **History Isolation**: Normal users can only inspect their own prediction history.
- **Admin Role**: Admin is a normal user with elevated administrative privileges. Server-side validation (`@admin_required`) guarantees that non-admin users receive HTTP 403 Forbidden on administrative endpoints. Passwords are never shown to administrators.
- **Admin Dashboard**:
  - Real-time counters: Total Users, Total Predictions, Total Disease Classes.
  - **Top Predicted Diseases &mdash; Last 7 Days**: Dynamically queried and aggregated strictly from real database records within `datetime.utcnow() - timedelta(days=7)`.
  - **Top Predicted Medicines &mdash; Last 7 Days**: Dynamically queried and aggregated strictly from real database records within `datetime.utcnow() - timedelta(days=7)`.
  - Full user registry and audit logs for all four modules with multi-parameter filtering (User ID, Module, Keyword, Date range).

---

## 📄 Reports & Data Exports

- **Branded PDF Reports**: Generated via ReportLab (`services/pdf_service.py`), including SynthSoma header branding, unique Report ID, timestamp, patient metadata, primary inferences, confidence gauges, clinical intelligence tables, and mandatory medical disclaimers.
- **CSV Data Exports**:
  - Individual modules (`disease`, `medicine`, `precaution`, `risk_factor`) or master history (`all`).
  - Standard users export only their own records.
  - Administrators can export full system-wide registries.

---

## 🗄️ Preserved Datasets & Models

All original datasets and fitted machine learning artifacts remain intact:

```
SynthSoma/
├── datasets/
│   ├── raw/
│   │   ├── disease_symptoms.csv
│   │   ├── disease_riskFactors.csv
│   │   ├── disease_precaution.csv
│   │   └── disease_medicine.csv
│   ├── cleaned/
│   │   ├── disease_information_cleaned.csv
│   │   ├── medicine_prediction_cleaned.csv
│   │   ├── precaution_cleaned.csv
│   │   └── risk_factor_cleaned.csv
│   └── processed/
│       ├── disease_features.csv
│       ├── medicine_features.csv
│       ├── precaution_features.csv
│       └── risk_factor_features.csv
└── models/ml/
    ├── complete_disease_system.pkl
    ├── disease_system_encoder.pkl
    ├── medicine_by_disease_model.pkl
    ├── medicine_encoder.pkl
    ├── disease_precaution_model.pkl
    ├── precaution_encoder.pkl
    ├── disease_risk_model.pkl
    └── disease_risk_encoder.pkl
```

---

## 🚀 macOS Setup & Installation Instructions

Follow these step-by-step instructions to run SynthSoma natively on macOS:

### 1. Open Terminal and Navigate to Project Root
```bash
cd /path/to/SynthSoma
```

### 2. Create and Activate Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Pytest Test Suite (Optional but Recommended)
```bash
pytest tests/
```
All 14 test modules should pass cleanly.

### 5. Launch the Flask Application
```bash
python3 app.py
```
The application will start on `http://127.0.0.1:5000` (or `http://localhost:5000`).

---

## 🔑 Default Credentials

### Administrator Account (Pre-seeded on startup):
- **User ID**: `admin`
- **Email**: `admin@synthsoma.org`
- **Password**: `Admin@SynthSoma2026!`

*(Admins have full access to both normal prediction workflows and the `/admin/` administration panel)*

### Standard User Account:
You can register any new user account via the `/signup` page, or log in with credentials you create.

---

## 🧪 Smoke Testing Procedure

1. **Start the application**: `python3 app.py`
2. **Access landing page**: Open `http://localhost:5000/` in your browser.
3. **Register new user**: Navigate to `http://localhost:5000/signup`, fill in the 7 fields, and register.
4. **Log in**: Sign in at `http://localhost:5000/login`.
5. **Disease Prediction**: Go to `Clinical Modules` &rarr; `Disease Prediction`, select symptoms (e.g. *Itching*, *Skin Rash*), and click **Run Disease Inference**.
6. **Medicine Reference**: Go to `Medicine Reference`, search *Fungal infection* or *Malaria*, and review formulations and active compounds.
7. **Suggest Precaution**: Go to `Suggest Precautions`, query *Acne* or *Allergy*, and inspect care steps.
8. **Analyse Risk Factor**: Go to `Analyse Risk Factors`, query *Diabetes* or *Gerd*, and examine occurrence rates and risk chips.
9. **Download PDF**: On any result page or from `/reports/`, click **Download PDF Report**.
10. **Export CSV**: Go to `/history/` and click **Export Current View (CSV)**.
11. **Admin Verification**: Sign out and log in as `admin` (`Admin@SynthSoma2026!`). Go to `/admin/` to verify user counts and the rolling 7-day predicted disease and medicine tables.
