from telegram import Update
from telegram.ext import ContextTypes

# Хранилище промптов пользователей (в памяти, без GitHub)
user_prompts = {}

async def setprompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /setprompt."""
    if not context.args:
        await update.message.reply_text(
            "⚠️ Укажите текст промпта после команды.\n\n"
            "Пример:\n"
            "/setprompt Ты — Фантом, ядро ИИ. Отвечай кратко."
        )
        return

    # Сохраняем промпт пользователя
    user_id = update.effective_user.id
    user_prompts[user_id] = " ".join(context.args)

    await update.message.reply_text("✅ Промпт сохранён!")