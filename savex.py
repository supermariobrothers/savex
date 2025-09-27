import os
import sqlite3
from datetime import datetime, timezone, timedelta
from tqdm import tqdm
import tkinter as tk
from tkinter import filedialog

# === SELECT BASE DIRECTORY ===
root = tk.Tk()
root.withdraw()
BASE_DIR = filedialog.askdirectory(title="Select the Screenshots folder")
if not BASE_DIR:
    print("No folder selected. Exiting.")
    exit()

DB_NAME = "HistoryP.db"

# === DATABASE SETUP ===
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS History (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    FileName TEXT,
    FilePath TEXT UNIQUE,
    DateTime TEXT,
    Type TEXT,
    Host TEXT,
    URL TEXT,
    ThumbnailURL TEXT,
    DeletionURL TEXT,
    ShortenedURL TEXT,
    Tags TEXT
);
""")

# === SCAN DIRECTORIES WITH PROGRESS BAR ===
all_files = []
folders = [f for f in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, f)) and len(f) == 7 and f[4] == "-"]

for folder in tqdm(folders, desc="Scanning folders", unit="folder"):
    folder_path = os.path.join(BASE_DIR, folder)
    for root, _, files in os.walk(folder_path):
        for f in tqdm(files, desc=f"Scanning {folder}", unit="file", leave=False):
            file_path = os.path.join(root, f)
            try:
                mtime = os.path.getmtime(file_path)
                all_files.append((f, file_path, mtime))
            except OSError:
                pass

# Sort files by modification time
all_files.sort(key=lambda x: x[2])

# === INSERT INTO DATABASE WITH PROGRESS BAR, SKIPPING DUPLICATES ===
inserted_count = 0
for fname, fpath, mtime in tqdm(all_files, desc="Inserting files", unit="file"):
    dt = datetime.fromtimestamp(mtime, tz=timezone(timedelta(hours=1)))  # +01:00 timezone
    formatted_dt = dt.isoformat()

    try:
        cursor.execute("""
            INSERT OR IGNORE INTO History (FileName, FilePath, DateTime, Type, Host, URL, ThumbnailURL, DeletionURL, ShortenedURL, Tags)
            VALUES (?, ?, ?, 'Image', NULL, NULL, NULL, NULL, NULL, NULL)
        """, (fname, fpath, formatted_dt))
        if cursor.rowcount > 0:
            inserted_count += 1
    except sqlite3.Error as e:
        print(f"Error inserting {fpath}: {e}")

conn.commit()
conn.close()

print(f"Inserted {inserted_count} new files into {DB_NAME}, skipped {len(all_files) - inserted_count} duplicates.")
