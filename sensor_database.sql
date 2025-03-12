CREATE TABLE IF NOT EXISTS sensor_data (
    timestamp TEXT DEFAULT (datetime('now')),
    tag TEXT,
    value REAL,
    PRIMARY KEY (timestamp, tag)
);

CREATE TABLE IF NOT EXISTS tags (
    tag TEXT PRIMARY KEY
);
