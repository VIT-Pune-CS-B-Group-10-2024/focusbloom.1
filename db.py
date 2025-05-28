import sqlite3

def init_db():
    conn = sqlite3.connect('mental_health_app.db')
    c = conn.cursor()
    
    # Users Table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )''')
    
    # Todos Table
    c.execute('''CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        task TEXT,
        priority TEXT,
        completed INTEGER DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Habits Table
    c.execute('''CREATE TABLE IF NOT EXISTS habits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        habit TEXT,
        date DATE,
        status INTEGER DEFAULT 0
    )''')
    
    # Journal Table
    c.execute('''CREATE TABLE IF NOT EXISTS journal (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        entry TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Mood Table
    c.execute('''CREATE TABLE IF NOT EXISTS mood (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        score INTEGER,
        notes TEXT,
        created_at DATE DEFAULT CURRENT_DATE
    )''')
    
    # Productivity Table
    c.execute('''CREATE TABLE IF NOT EXISTS productivity (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        pomodoro_count INTEGER,
        screen_time REAL,
        date DATE DEFAULT CURRENT_DATE
    )''')
    
    conn.commit()
    conn.close()
