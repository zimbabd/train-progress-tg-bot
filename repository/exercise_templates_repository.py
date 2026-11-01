import sqlite3

class ExerciseTemplatesRepository:
    def __init__(self, db_path):
        self.db_path = db_path
        self.create_table()

    def create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            query = '''
            CREATE TABLE IF NOT EXISTS exercise_templates (
                template_id INTEGER PRIMARY KEY,
                template_name TEXT
            )
            '''
            conn.execute(query)

    def fill_table(self):
        # Add exercises only if the table is empty
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('SELECT COUNT(*) FROM exercise_templates')
            count = cursor.fetchone()[0]

            if count == 0:  # If there are no records in the table, perform an insertion
                query = '''
                INSERT INTO exercise_templates (template_name)
                VALUES
                ('run'),
                ('squats'),
                ('push_ups'),
                ('plank'),
                ('jumping_rope')
                '''
                conn.execute(query)
                conn.commit()

    def get_all_templates(self):
        with sqlite3.connect(self.db_path) as conn:
            query = 'SELECT * FROM exercise_templates'
            cursor = conn.execute(query)
            return [{'template_id': row[0], 'template_name': row[1]} for row in cursor.fetchall()]

    def get_template_by_id(self, template_id):
        with sqlite3.connect(self.db_path) as conn:
            query = 'SELECT * FROM exercise_templates WHERE template_id = ?'
            cursor = conn.execute(query, (template_id,))
            row = cursor.fetchone()
            if row:
                return {
                    'template_id': row[0],
                    'template_name': row[1]
                }
            return None
    def close(self):
        self.conn.close()