import sqlite3

conn = sqlite3.connect('menstrual.db')
conn.execute('''CREATE TABLE periods
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              start_date TEXT NOT NULL,
              end_date TEXT NOT NULL,
              cycle_length INTEGER NOT NULL);''')
conn.close()