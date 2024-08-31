import os
import json
import logging
from aiogram import Bot, Dispatcher, types
from app.components import router
from app.components.working_ydb import WorkingDataBase

from app.components.questions import quiz_data
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv("API_TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
dp.include_router(router)

db = WorkingDataBase()
db.add_questions(quiz_data)

async def process_event(event):
    try:
        update = types.Update.model_validate(json.loads(event['body']), context={"bot": bot})
        await dp.feed_update(bot, update)
    except Exception as e:
        logging.error(f"Error processing event: {e}")

async def webhook(event, context):
    if event['httpMethod'] == 'POST':
        await process_event(event)
        return {'statusCode': 200, 'body': 'ok'}
    if event['httpMethod'] == 'GET':
        return {'statusCode': 200, 'body': 'ok'}

    return {'statusCode': 405}
