import sqlite3
import hashlib

class UserModel:
    def __init__(self):
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def check_credentials(self, username, password):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('SELECT password FROM users WHERE username = ?', (username,))
        result = c.fetchone()
        conn.close()
        if result:
            stored_password = result[0]
            computed_hash = self.hash_password(password)
            print("Stored Password Hash:", stored_password)  # Debugging
            print("Computed Password Hash:", computed_hash)  # Debugging
            return stored_password == computed_hash
        return False

    def add_user(self, username, password):
        try:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, self.hash_password(password)))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False

    def authenticate_user(self, username, password):
        if self.check_credentials(username, password):
            # Generate a session ID (for simplicity, use a hash of the username and password)
            session_id = self.hash_password(username + password)
            return session_id, username
        return None

    def logout_user(self, session_id):
        # Implement logout logic if needed
        pass

    def get_user_id(self, username):
        """
        Retrieve the user_id for a given username.
        """
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('SELECT id FROM users WHERE username = ?', (username,))
        result = c.fetchone()
        conn.close()
        if result:
            return result[0]  # Return the user_id
        return None  # Return None if the username is not found