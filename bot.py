# bot.py
import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = "8400969993:AAEpt8RHiH3Dct1tx-nFj-3g1AyDQyX-3r8"

#{топик_id: [список_разрешённых_тегов]}
TOPIC_RULES = {
    7: ["#Письки", "#письки"],
    50: ["#Сиськи", "#Сиськи"],
    60: ["#Члены", "#члены"]
}

async def enforce_rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message:
        return

    chat_id = message.chat_id
    thread_id = getattr(message, "message_thread_id", None)
    text = (message.text or "").lower()  

    print(f"📩 Новое сообщение | chat_id={chat_id} | thread_id={thread_id} | text='{text}'")

    if thread_id in TOPIC_RULES:
        allowed_tags = [tag.lower() for tag in TOPIC_RULES[thread_id]]

        # Проверяем, содержит ли сообщение хотя бы один разрешённый тег
        if not any(tag in text for tag in allowed_tags):
            try:
                await message.delete()
                print(f"🚫 Сообщение удалено: отсутствуют разрешённые теги {allowed_tags}")
            except Exception as e:
                print(f"⚠️ Ошибка при удалении: {e}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, enforce_rules))

print("Бот запущен.")
app.run_polling()
