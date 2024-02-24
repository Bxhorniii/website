-- Create the 'user' table
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
);

-- Create the 'text_mapping' table
CREATE TABLE text_mapping (
    short_id TEXT PRIMARY KEY,
    original_text TEXT NOT NULL,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES user (id)
);
