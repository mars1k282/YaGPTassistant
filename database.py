import sqlite3

class Database:
    def __init__(self, db_name='bot.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usage (
                user_id INTEGER PRIMARY KEY,
                character_count INTEGER
            )
        ''')
        self.conn.commit()

    def get_usage(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT character_count FROM usage WHERE user_id=?', (user_id,))
        row = cursor.fetchone()
        return row[0] if row else 0

    def update_usage(self, user_id, character_count):
        current_count = self.get_usage(user_id)
        if current_count == 0:
            cursor = self.conn.cursor()
            cursor.execute('INSERT INTO usage (user_id, character_count) VALUES (?, ?)', (user_id, character_count))
        else:
            cursor = self.conn.cursor()
            cursor.execute('UPDATE usage SET character_count=? WHERE user_id=?', (current_count + character_count, user_id))
        self.conn.commit()