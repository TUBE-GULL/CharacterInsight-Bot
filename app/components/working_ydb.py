import os
import ydb
import json

class WorkingDataBase:
    
    def __init__(self, timeout=30) -> None:
        # Используем переменные окружения для конфигурации
        ydb_database = os.getenv('YDB_DATABASE')
        ydb_endpoint = os.getenv('YDB_ENDPOINT')
        
        if not ydb_database or not ydb_endpoint:
            raise ValueError("Database configuration is missing. Check your environment variables.")

        driver_config = ydb.DriverConfig(
            ydb_endpoint,
            ydb_database,
            credentials=ydb.credentials_from_env_variables(),
            root_certificates=ydb.load_ydb_root_certificate(),
        )
        
        try:
            self.driver = ydb.Driver(driver_config)
            self.driver.wait(timeout=timeout)
            self.session = self.driver.table_client.session().create()
        except TimeoutError:
            print("Connect failed to YDB: Timeout")
        except Exception as e:
            print(f"An error occurred while connecting: {e}")
            self.session = None

    # ok !
    def update_quiz_index(self, user_id: int, index: int, answers: list):
        if self.session is None:
            print("No active session. Cannot write to database.")
            return
        try:
            self.session.transaction(ydb.SerializableReadWrite()).execute(
                f"""
                    UPSERT INTO quiz_state 
                    (user_id, question_index, correct_answers, past_result) 
                    VALUES({user_id}, {index}, '{json.dumps(answers)}', ' ');
                """,
                commit_tx=True,
            )
            print("Data successfully written to database.")
        except Exception as e:
            print(f"An error occurred while writing to the database: {e}")

    #
    def get_quiz_data_user(self, user_id: int):
        if self.session is None:
            print("No active session. Cannot read from database.")
            return None

        try:
            result = self.session.transaction(ydb.SerializableReadWrite()).execute(
                f"""
                    SELECT question_index, correct_answers 
                    FROM quiz_state 
                    WHERE user_id = {user_id};
                """,
                commit_tx=True,
            )

            if result and result[0].rows:
                row = result[0].rows[0]
                question_index = row['question_index']
                correct_answers = json.loads(row['correct_answers'])  # correct_answers is stored as a JSON string
                print(correct_answers)
                return question_index, correct_answers
            else:
                # Initialize a new record if not found
                current_question_index = 0
                answers = [0] * 10  # Reset to default answers list
                self.update_quiz_index(user_id, current_question_index, answers)
                return current_question_index, answers
        except Exception as e:
            print(f"An error occurred while reading from the database: {e}")
            return None

       
    def write_database(self, user_id: int, value: any, column: str) -> None:
        if self.session:
            try:
                # Determine if the value needs to be quoted (for strings, etc.)
                if isinstance(value, str):
                    value = f"'{value}'"
                
                with self.session.transaction(ydb.SerializableReadWrite()) as tx:
                    # Safely construct the query string
                    query = f"""
                        UPSERT INTO quiz_state 
                        (user_id, {column}) 
                        VALUES ({user_id}, {value});
                    """
                    tx.execute(query, commit_tx=True)
                
                print("Data successfully written to the database.")
            except Exception as e:
                print(f"An error occurred while writing to the database: {e}")
       

    def add_questions(self, quiz_data):
        if self.session is None:
            print("No active session. Cannot write to the database.")
            return None

        try:
            for idx, qn in enumerate(quiz_data):
                id = idx  # Generate a unique ID for each question
                question = json.dumps(qn).replace('"', '\\"')  # Escape double quotes
                
                query = f"""
                    UPSERT INTO quiz_question 
                    (id, question) 
                    VALUES ({id}, "{question}");
                """
                self.session.transaction(ydb.SerializableReadWrite()).execute(
                    query,
                    commit_tx=True
                )
                print(f"Data for id {id} successfully written to the database.")
        
        except Exception as e:
            print(f"Произошла ошибка при записи в базу данных для id {id}: {e}")
        

    

    def get_question(self, id):
        if self.session is None:
            print("No active session. Cannot read from the database.")
            return None
    
        try:
            query = f"""
                SELECT question 
                FROM quiz_question 
                WHERE id = {id};
            """
            result_sets = self.session.transaction(ydb.SerializableReadWrite()).execute(
                query,
                commit_tx=True
            )
    
            if result_sets:
                question_json = result_sets[0].rows[0]["question"]
                question_data = json.loads(question_json.replace('\\"', '"'))  # Reverse escaping
                return question_data
            else:
                print(f"No question found with id {id}.")
                return None
    
        except Exception as e:
            print(f"Произошла ошибка при чтении из базы данных для id {id}: {e}")
            return None

    def close(self):
        if self.driver:
            self.driver.stop()
