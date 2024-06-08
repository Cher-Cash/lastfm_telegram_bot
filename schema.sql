-- Create users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR,
    lastfm VARCHAR,
    chat_id INTEGER
);

-- Create played table
CREATE TABLE played (
    id INTEGER PRIMARY KEY,
    song VARCHAR,
    artist VARCHAR,
    user_id INTEGER,
    created_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

