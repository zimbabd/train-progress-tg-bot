import sqlite3
from model.user_model import User  # import user model


class UserRepository:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_table()

    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            registration_date DATE DEFAULT (date('now'))
        )
        '''
        self.conn.execute(query)
        self.conn.commit()

    def add_user(self, user):
        query = '''
        INSERT INTO users (user_id, username, first_name)
        VALUES (?, ?, ?)
        '''
        self.conn.execute(query, (
        user.user_id, user.username, user.first_name))
        self.conn.commit()

    def get_user(self, user_id):
        query = 'SELECT * FROM users WHERE user_id = ?'
        cursor = self.conn.execute(query, (user_id,))
        row = cursor.fetchone()

        if row:
            return User(
                user_id=row[0],
                username=row[1],
                first_name=row[2],
            )
        return None

    def close(self):
        self.conn.close()
