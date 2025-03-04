import sqlite3
import bcrypt

class DatabaseManager:
    def __init__(self, db_name='users.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Table des utilisateurs
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            email TEXT UNIQUE
        )''')
        
        # Table des notes
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            title TEXT,
            content TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(username) REFERENCES users(username)
        )''')
        self.conn.commit()

    def register_user(self, username, password, email):
        # Hachage du mot de passe
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        try:
            self.cursor.execute(
                'INSERT INTO users (username, password, email) VALUES (?, ?, ?)', 
                (username, hashed_password, email)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def validate_login(self, username, password):
        self.cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
        result = self.cursor.fetchone()
        
        if result:
            stored_password = result[0]
            return bcrypt.checkpw(password.encode('utf-8'), stored_password)
        return False

    def add_note(self, username, title, content):
        self.cursor.execute(
            'INSERT INTO notes (username, title, content) VALUES (?, ?, ?)', 
            (username, title, content)
        )
        self.conn.commit()

    def get_user_notes(self, username):
        self.cursor.execute('SELECT id, title, content, created_at FROM notes WHERE username = ?', (username,))
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()