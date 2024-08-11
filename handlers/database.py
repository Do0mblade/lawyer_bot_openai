

## ТЕСТ ДБ

import sqlite3

class Database():
    def __init__(self):
      self.connection = sqlite3.connect('my_database.db')
      self.cursor = self.connection.cursor()

      self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                     id INTEGER PRIMARY KEY,
                     user_id INTEGER NOT NULL,
                     thread_id TEXT
                     )""")
      self.connection.commit()
      
      self.cursor.execute("SELECT * FROM users")
      print(self.cursor.fetchall())
      
    async def check_user_in_db(self, user_id):
       self.cursor.execute(f"SELECT id FROM users WHERE user_id = {user_id}")
       return bool(self.cursor.fetchone())

    async def get_thread_id(self, user_id):
       self.cursor.execute(f"SELECT thread_id FROM users WHERE user_id = {user_id}")
       return self.cursor.fetchone()
       


    async def create_user(self, user_id, thread_id):
       self.cursor.execute(f"INSERT INTO users (user_id, thread_id) VALUES ({user_id}, '{thread_id}')")
       self.connection.commit()







