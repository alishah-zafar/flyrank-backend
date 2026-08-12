# Tasks API

A simple Flask REST API for managing tasks, backed by SQLite.

## Database

- **Why SQLite:** Lightweight, file-based, requires no separate server — ideal for a small project like this. Perfect for learning the API layer / data layer separation before moving to a bigger database later.
- **Database file location:** `tasks.db`, created automatically in the project root the first time the app runs.
- **How to run this project:**
```bash
  pip install flask
  python app2.py
```
  The database and `tasks` table are created automatically if missing, and three example tasks are inserted only if the table is empty.

## Database screenshot

(<Screenshot 2026-08-12 162514.png>)

## Example query

```sql
SELECT * FROM tasks WHERE done = 1;
```