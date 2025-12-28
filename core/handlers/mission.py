from telegram import Update
from telegram.ext import ContextTypes

async def mission(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /mission."""
    if not context.args:
        await update.message.reply_text("⚠️ Укажите текст миссии после команды.")
        return

    mission_text = " ".join(context.args)
    await update.message.reply_text(f"📜 Миссия принята: {mission_text}")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /status."""
    await update.message.reply_text(
        "🔧 *Статус ядра:*\n"
        "• Ядро ИИ: онлайн\n"
        "• Контекст: активен\n"
        "• Память: стабильна",
        parse_mode="MarkdownV2"
    )