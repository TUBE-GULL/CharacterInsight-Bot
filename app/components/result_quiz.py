from aiogram.types import CallbackQuery
from collections import Counter
from app.components.working_ydb import WorkingDataBase

db = WorkingDataBase()


async def result_quiz(callback: CallbackQuery, correct_answers: list[str]):
    result = {'A': 'Экстравертный, общительный, энергичный.',
              'B': 'Интровертный, спокойный, вдумчивый.',
              'C': 'Креативный, нестандартный, открытый новому.',
              'D': 'Рациональный, организованный, прагматичный.'}
    
    await callback.message.answer("Это был последний вопрос. Квиз завершен!")
    counter =  Counter(correct_answers)
    most_common_symbol = counter.most_common(1)[0][0]
    
    db.write_database(callback.from_user.id, result[most_common_symbol], 'past_result')
    await callback.message.answer(f"Скорее всего, вы: {result[most_common_symbol]}")

# A: Экстравертный, общительный, энергичный.
# B: Интровертный, спокойный, вдумчивый.
# C: Креативный, нестандартный, открытый новому.
# D: Рациональный, организованный, прагматичный.