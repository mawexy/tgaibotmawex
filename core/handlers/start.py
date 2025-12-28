from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 *Добро пожаловать*\\.\n"
        "Я — **MiMo**, ваше ядро ИИ\\.\n"
        "Используйте `/help` для списка команд\\.",
        parse_mode="MarkdownV2"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "📜 *Доступные команды:*\n"
        "• `/start` — Начать операцию\n"
        "• `/help` — Показать помощь\n"
        "• `/mission <текст>` — Записать миссию\n"
        "• `/status` — Проверить статус ядра\n"
        "• `/cleanmem` — Очистить память\n"
        "• `/setprompt <текст>` — Настроить промпт для ИИ"
    )
    await update.message.reply_text(help_text, parse_mode="MarkdownV2")