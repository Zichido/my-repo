import os
import threading
import asyncio
import nest_asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# ----------------------------
# Переменная окружения с токеном
# ----------------------------
TOKEN = "8400969993:AAEpt8RHiH3Dct1tx-nFj-3g1AyDQyX-3r8"  # можно заменить на os.getenv("TOKEN")
if not TOKEN:
    raise SystemExit("❌ ERROR: TOKEN не задан!")

# ----------------------------
# Правила топиков
# ----------------------------
TOPIC_RULES = {
    536997: ["#канал", "#Канал"],
    537034: ["#магическаябитва", "#ролевая", "#флуд"],
    537025: ["#китайфд", "#ролевая", "#флуд"],
    537022: ["#человекбензопила", "#ролевая", "#флуд"],
    537017: ["#всефд", "#ролевая", "#флуд"],
    537014: ["#бсд", "#ролевая", "#флуд"],
    537011: ["#хср", "#ролевая", "#флуд"],
    537008: ["#геншин", "#ролевая", "#флуд"],
    537003: ["#ориджинал", "#ролевая"],
    537044: ["книги", "ролевая", "флуд"],
    537041: ["#токийскиемстители","ролевая","флуд"],
    537050: ["неттемы","флуд","ролевая"],
    537053: ["#ритмигры","флуд","ролевая"],
    537056: ["вува","ролевая","флуд"],
    537062: ["zzz","ролевая","флуд"],
    537059: ["кпоп","ролевая","флуд"],
    537064: ["ищуролку","ищуфлуд"],
    537066: ["#ищуадмина"]  
}

# ----------------------------
# Логика бота
# ----------------------------
async def enforce_rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message:
        return

    thread_id = getattr(message, "message_thread_id", None)
    text = (message.text or "").lower()

    if thread_id in TOPIC_RULES:
        allowed_tags = [t.lower() for t in TOPIC_RULES[thread_id]]
        if not any(tag in text for tag in allowed_tags):
            try:
                await message.delete()
                print(f"🚫 Сообщение удалено в топике {thread_id}: нет разрешённого тега {allowed_tags}")
            except Exception as e:
                print(f"⚠️ Ошибка при удалении сообщения: {e}")

# ----------------------------
# Fake HTTP-сервер для Render Free
# ----------------------------
class PingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

def start_fake_server():
    port = int(os.environ.get("PORT", 10000))  # Render назначает PORT автоматически
    httpd = HTTPServer(("0.0.0.0", port), PingHandler)
    print(f"🌐 Fake server started on port {port}")
    httpd.serve_forever()

# ----------------------------
# Основная функция бота
# ----------------------------
async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, enforce_rules))
    print("🟢 Бот запущен и слушает топики...")
    await app.run_polling()

# ----------------------------
# Запуск
# ----------------------------
if __name__ == "__main__":
    # 1. Запускаем fake сервер в отдельном потоке
    threading.Thread(target=start_fake_server, daemon=True).start()

    # 2. Исправляем проблему "loop already running" в VSCode/Windows
    nest_asyncio.apply()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
