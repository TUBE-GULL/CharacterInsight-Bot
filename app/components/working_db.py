import aiosqlite 
import json
from typing import Union 

class QuizeDatabase:
   
    def __init__(self, db_name='quiz.db') -> None:
        self.db_name = db_name


    async def create_table(self):
        # Создаеь соединение с базой данных (если она не сущ то она будет создана)
        async with aiosqlite.connect(self.db_name) as db:
            # Выполняем SQL-запрос к базе данных
            await db.execute('''
                CREATE TABLE IF NOT EXISTS quiz_state (
                    user_id INTEGER PRIMARY KEY, 
                    question_index INTEGER DEFAULT 0, 
                    correct_answers TEXT DEFAULT '['','','','','','','','','','']',
                    past_result TEXT
                    )
                ''')#Добавил число правильных ответов: 0 - не верно,  1 - верно  
            await db.commit()# Сохраняем изменения


    async def update_quiz_index(self, user_id:int, index:int, answers:list):
        async with aiosqlite.connect(self.db_name) as db:
            # Вставляем новую запись или заменяем ее, если с данным user_id уже существует
            print(answers)
            answers_json = json.dumps(answers)
            await db.execute('''UPDATE quiz_state  
                            SET question_index = ?, 
                            correct_answers = ? 
                            WHERE user_id = ?
                            ''', (index, answers_json, user_id))
            await db.commit()# Сохраняем изменения


    async def get_quiz_data_user(self, user_id):
     # Подключаемся к базе данных
     async with aiosqlite.connect(self.db_name) as db:
        # Получаем запись для заданного пользователя()
        async with db.execute('SELECT user_id, question_index, correct_answers FROM quiz_state WHERE user_id = ?', (user_id,)) as cursor:
            # Возвращаем результат
            results = await cursor.fetchone()
            if results is not None:
                user_Id, question_index, correct_answers = results
                correct_answers = json.loads(correct_answers)  # correct_answers хранится как строка JSON
                return question_index, correct_answers
            else:
                 # Если пользователь не найден, создаем новую запись
                 await db.execute('INSERT INTO quiz_state (user_id, question_index, correct_answers) VALUES (?, ?, ?)', 
                                  (user_id, 0, json.dumps([0]*10)))
                 await db.commit()
                 return 0, [0]*10  # Возвращаем начальные значения
   
    
    # запись любого зн 
    async def write_database(self, user_id:int, value:Union[str, int], column:str ):

        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(f'UPDATE quiz_state SET {column}=? WHERE user_id=?',
                             (value, user_id))
            await db.commit()


    # чтения любого зн 
    async def read_database(self, user_id: Union[str, int], column:str ):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute(f'SELECT {column} FROM quiz_state WHERE user_id = ?', (user_id,)) as cursor:
                results = await cursor.fetchone()
                if results is not None:
                    return results[0]
                else:
                    return None 
