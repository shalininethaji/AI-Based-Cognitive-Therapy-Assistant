-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'therapist', 'patient')),
    patient_id VARCHAR(100), -- Link for patients
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Ensure therapist_inputs table exists with all required columns
CREATE TABLE IF NOT EXISTS therapist_inputs (
    id SERIAL PRIMARY KEY,
    patient_id VARCHAR(100) NOT NULL,
    patient_name VARCHAR(255),
    mood_level INTEGER,
    stress_level INTEGER,
    anxiety_level INTEGER,
    sleep_quality VARCHAR(50),
    appetite VARCHAR(50),
    social_withdrawal BOOLEAN,
    distortions TEXT,
    cbt_goal TEXT,
    notes TEXT,
    therapist_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create chat_history table
CREATE TABLE IF NOT EXISTS chat_history (
    id SERIAL PRIMARY KEY,
    patient_id VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL, -- 'user' or 'assistant'
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
