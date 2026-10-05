-- SynthSoma Database Schema (SQLite)

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id VARCHAR(80) UNIQUE NOT NULL,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    phone VARCHAR(30) NOT NULL,
    location VARCHAR(120) NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    role VARCHAR(20) DEFAULT 'user' NOT NULL,
    reset_token VARCHAR(100),
    reset_token_expiry DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id VARCHAR(80) NOT NULL,
    module VARCHAR(50) NOT NULL,
    input_summary TEXT NOT NULL,
    result_summary TEXT NOT NULL,
    details_json TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS disease_predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prediction_id INTEGER,
    user_id VARCHAR(80) NOT NULL,
    selected_symptoms TEXT NOT NULL,
    predicted_disease VARCHAR(120) NOT NULL,
    confidence REAL,
    model_used VARCHAR(80) NOT NULL,
    risk_factors TEXT,
    precautions TEXT,
    medicines TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (prediction_id) REFERENCES predictions(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS medicine_predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prediction_id INTEGER,
    user_id VARCHAR(80) NOT NULL,
    disease_input VARCHAR(120) NOT NULL,
    predicted_medicines TEXT NOT NULL,
    medicine_details TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (prediction_id) REFERENCES predictions(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS precaution_predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prediction_id INTEGER,
    user_id VARCHAR(80) NOT NULL,
    disease_input VARCHAR(120) NOT NULL,
    precautions TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (prediction_id) REFERENCES predictions(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS risk_factor_predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prediction_id INTEGER,
    user_id VARCHAR(80) NOT NULL,
    disease_input VARCHAR(120) NOT NULL,
    matched_disease VARCHAR(120) NOT NULL,
    risk_factors TEXT NOT NULL,
    occurrence VARCHAR(200),
    clinical_notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (prediction_id) REFERENCES predictions(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_users_user_id ON users(user_id);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_predictions_user_id ON predictions(user_id);
CREATE INDEX IF NOT EXISTS idx_predictions_module ON predictions(module);
CREATE INDEX IF NOT EXISTS idx_predictions_created_at ON predictions(created_at);
