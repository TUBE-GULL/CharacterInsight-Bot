from aiogram import F,Router
from aiogram.filters import CommandStart,Command
from aiogram.types import Message,CallbackQuery,FSInputFile

#import Models 
from app.components.working_ydb import WorkingDataBase
from app.components.fun_questions import new_quiz, get_question
from app.components.keyboards import start_keyboard
from app.components.questions import quiz_data
from app.components.result_quiz import result_quiz

router = Router()
db = WorkingDataBase()


@router.message(CommandStart())
async def start(message:Message):
    # Прикрепляем кнопки к сообщению
    await message.answer("Добро пожаловать в квиз", reply_markup=start_keyboard)
    photo_url = "https://storage.yandexcloud.net/imag-bot/image.png"
    await message.answer_photo(photo_url)
    
@router.message(Command('quiz'))
async def cmd_quiz(message:Message):
    await message.answer("Давайте начнем квиз Первый вопрос: ...")
    

@router.message(F.text == "Начать игру")
@router.message(Command('quiz'))
async def cmd_quiz(message: Message):
    await message.answer(f"Давайте начнем квиз")
    await new_quiz(message)

@router.callback_query(F.data.startswith("answer"))
async def wrong_answer(callback: CallbackQuery):
    
    _, answer_user = callback.data.split("_")

    # Получение Данные о пользователе 
    question_index, correct_answers = db.get_quiz_data_user(callback.from_user.id)
    
    # Сохраняем данные о выборе пользователя
    new_correct_answers = correct_answers
    new_correct_answers[question_index] = answer_user
    
    question_index += 1
    db.update_quiz_index(callback.from_user.id, question_index, new_correct_answers)

    # Проверяем достигнут ли конец тест на Pythonа
    if question_index < len(quiz_data): 
        # Следующий вопрос
        await get_question(callback.message, callback.from_user.id)
    else: 
        await result_quiz(callback, correct_answers)
              
       