import sqlite3

class TrainingSessionsRepository:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_table()

    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS training_sessions (
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            template_id INTEGER,
            session_date DATE DEFAULT (datetime('now', 'localtime')),
            distance INTEGER DEFAULT NULL,
            pace INTEGER DEFAULT NULL,
            pulse INTEGER DEFAULT NULL,
            quantity INTEGER DEFAULT NULL,
            sets INTEGER DEFAULT NULL,
            weight INTEGER DEFAULT NULL,
            duration INTEGER DEFAULT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (template_id) REFERENCES exercise_templates(template_id)
        )
        '''
        self.conn.execute(query)
        self.conn.commit()

    def add_training_session(self, user_id, template_id, session_date=None, distance=None, pace=None, pulse=None, quantity=None, sets=None,
                             weight=None, duration=None):
        """
       Method for adding a new training session to the database.
        """
        query = '''
        INSERT INTO training_sessions (user_id, template_id, session_date, distance, pace, pulse, quantity, sets, weight, duration)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''

        # Execute the request and pass all parameters
        self.conn.execute(query, (user_id, template_id, session_date, distance, pace, pulse, quantity, sets, weight, duration))
        self.conn.commit()

    def get_session_by_id(self, session_id, user_id):
        query = '''
        SELECT session_id, user_id, template_id, session_date, distance, pace, pulse, quantity, sets, weight, duration
        FROM training_sessions
        WHERE session_id = ? AND user_id = ?
        '''

        cursor = self.conn.execute(query, (session_id, user_id))
        row = cursor.fetchone()
        if row:
            return {
                'session_id': row[0],
                'user_id': row[1],
                'template_id': row[2],
                'session_date': row[3],
                'distance': row[4],
                'pace': row[5],
                'pulse': row[6],
                'quantity': row[7],
                'sets': row[8],
                'weight': row[9],
                'duration': row[10]
            }
        return None

    def get_all_sessions_by_user_id(self, user_id):
        """
        Method for getting all training sessions by user_id.
        """
        query = 'SELECT * FROM training_sessions WHERE user_id = ?'
        cursor = self.conn.execute(query, (user_id,))
        return cursor.fetchall()  # Return all rows matching the query

    def get_last_sessions_by_user_id(self, user_id, limit=5):
        """
        Method for getting the latest workouts by user_id, including the name of the workout and all parameters.
        """
        query = '''
        SELECT ts.session_id, et.template_name, ts.user_id, ts.session_date, ts.distance, ts.pace, ts.pulse, ts.quantity, ts.sets, ts.weight, ts.duration
        FROM training_sessions ts
        JOIN exercise_templates et ON ts.template_id = et.template_id
        WHERE ts.user_id = ?
        ORDER BY ts.session_date DESC
        LIMIT ?
        '''
        cursor = self.conn.execute(query, (user_id, limit))
        return cursor.fetchall()

    def close(self):
        self.conn.close()
