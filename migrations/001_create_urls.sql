-- Create the urls table for the URL shortener service
CREATE TABLE IF NOT EXISTS urls (
    short_code VARCHAR(16) PRIMARY KEY,
    original_url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
