import sqlite3
import datetime
from datetime import datetime

current_time = datetime.now()

conn = sqlite3.connect('data/data.db')
cursor = conn.cursor()

def create_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            user_name TEXT,
            user_first_name TEXT,
            user_last_name TEXT,
            phone INTEGER
        )
    ''')
    conn.commit()

def add_user(user_id, user_name):
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    existing_user = cursor.fetchone()
    if existing_user is None:
        cursor.execute('''
            INSERT INTO users (user_id, user_name)
            VALUES (?, ?)
        ''', (user_id, user_name))
        conn.commit()
        
def check_user(uid):
    cursor.execute(f'SELECT * FROM Users WHERE user_id = {uid}')
    user = cursor.fetchone()
    if user:
        return True
    return False
    
def check_user_language(user_id):
    cursor.execute('SELECT lang FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None
    
def update_user_language(user_id, lang):
    cursor.execute('''
        UPDATE users
        SET lang = ?
        WHERE user_id = ?
    ''', (lang, user_id))
    conn.commit()

def update_downloads(user_id, platform):
    platform_column = {
        'instagram': 'insta',
        'tiktok': 'tiktik',
        'youtube': 'youtube',
        'pinterest': 'pint'
    }.get(platform)
    
    if not platform_column:
        raise ValueError("Invalid platform")
    
    # Update the SQL query to handle conflicts properly
    query = f"""
    INSERT INTO downloads (user_id, {platform_column}) 
    VALUES (?, 1) 
    ON CONFLICT(user_id) 
    DO UPDATE SET {platform_column} = {platform_column} + 1
    """
    
    cursor.execute(query, (user_id,))
    conn.commit()
    
    
def get_statistics(user_id):
    
    cursor.execute("SELECT insta, tiktik, youtube, pint FROM downloads WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()

    
    if row:
        return {
            'instagram': row[0],
            'tiktok': row[1],
            'youtube': row[2],
            'pinterest': row[3]
        }
    else:
        return None