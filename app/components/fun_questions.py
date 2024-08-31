from app.components.questions import quiz_data
from app.components.working_ydb import WorkingDataBase
from app.components.keyboards import  generate_options_keyboard

db = WorkingDataBase()

async def get_question(message, user_id):

    question_index, correct_answers = db.get_quiz_data_user(user_id) 
    
    opts = db.get_question(question_index)
    kb = generate_options_keyboard(opts)
    await message.answer(f"{quiz_data[question_index]['question']}", reply_markup=kb)  

async def new_quiz(message):
    user_id = message.from_user.id # достали id user
    current_question_index = 0 # сбрасываем значение в 0 
    answers = [0,0,0,0,0,0,0,0,0,0]# сбрасываем значение в 0 
    db.update_quiz_index(user_id, current_question_index, answers)
    # запрашиваем новый вопрос для квиза
    await get_question(message, user_id)
    

