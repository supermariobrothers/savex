# 📂 SaveX

**SaveX** is a Python tool for recovering `History.db` by rebuilding it from the files stored inside your **Screenshots** folder. It scans your screenshots chronologically and regenerates the database with the correct structure.

---

## 🚀 Features

* Scans subfolders named in the format `%YYYY%-%MM%` (e.g., `2025-02`).
* Extracts file metadata (filename, full path, last modification timestamp).
* Inserts files into a SQLite database `HistoryP.db`.
* Uses correct ISO8601 datetime format (`YYYY-MM-DDTHH:MM:SS.ssssss+01:00`).
* Automatically skips duplicates based on `FilePath`.
* Progress bars for both **scanning** and **insertion**.
* Lets the user choose the `Screenshots` folder interactively.

---

## 📦 Requirements

Make sure you have Python **3.8+** installed. Then install the required dependencies:

```bash
pip install tqdm
```

---

## 🛠 Usage

1. Run the script:

   ```bash
   python savex.py
   ```

2. A dialog will ask you to select your **Screenshots folder**.

3. The tool will:

   * Scan all `%YYYY%-%MM%` subfolders.
   * Sort files by oldest first.
   * Insert them into `HistoryP.db`.

4. Once finished, the script will print how many files were **inserted** and how many were **skipped** (already in the DB).

---

## 📂 Database Structure

The generated `HistoryP.db` contains a single table:

| Column       | Type    | Description                           |
| ------------ | ------- | ------------------------------------- |
| Id           | INTEGER | Auto-increment primary key            |
| FileName     | TEXT    | The name of the file                  |
| FilePath     | TEXT    | Full absolute path (unique)           |
| DateTime     | TEXT    | File modification timestamp (ISO8601) |
| Type         | TEXT    | Always set to `Image`                 |
| Host         | TEXT    | `NULL`                                |
| URL          | TEXT    | `NULL`                                |
| ThumbnailURL | TEXT    | `NULL`                                |
| DeletionURL  | TEXT    | `NULL`                                |
| ShortenedURL | TEXT    | `NULL`                                |
| Tags         | TEXT    | `NULL`                                |

---

## 📝 Notes

* If you rerun the script, previously inserted files are skipped.
* Database file is always named **`HistoryP.db`** and created in the script directory.

---

## ⚡ Example

```
Inserted 12483 new files into HistoryP.db, skipped 0 duplicates.
```

---

## 📜 License

This project is released under the GNU GPLv3.0 License.
