
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import language_tool_python

# Инициализация инструмента проверки языка
lang_tool = language_tool_python.LanguageToolPublicAPI('ru-RU')

# Включаем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

import os
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Безопасный способ

# === Упрощение стиля ===
def simplify_text(text: str) -> str:
    replacements = {
        "в связи с тем, что": "потому что",
        "осуществляется": "делается",
        "является": "",
        "следует отметить, что": "",
        "в настоящий момент": "сейчас",
        "имеется": "есть",
        "путем": "через",
        "осуществлять": "делать",
        "настоящим": "этим"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

# === Обработка сообщений ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    original_text = update.message.text

    # Шаг 1: Проверка грамматики и пунктуации
    matches = lang_tool.check(original_text)
    corrected_text = language_tool_python.utils.correct(original_text, matches)

    # Шаг 2: Упрощение стиля
    simplified_text = simplify_text(corrected_text)

    # Ответ пользователю
    await update.message.reply_text(simplified_text)

# === /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я FixRano Language Bot. Пришли мне текст — я поправлю ошибки и сделаю его чище.")

# === main ===
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Бот запущен...")
    app.run_polling()

if __name__ == '__main__':
    main()
