from telegram import Update
from telegram.ext import ContextTypes

async def cleanmem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Очистка контекста диалога."""
    user_id = update.effective_user.id
    if user_id in context.bot.context_history:
        del context.bot.context_history[user_id]
        await update.message.reply_text("🧹 Контекст очищен!")
    else:
        await update.message.reply_text("⚠️ Контекст пуст.")

async def increase_context(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Увеличение размера контекста."""
    user_id = update.effective_user.id
    current_size = context.bot.context_sizes.get(user_id, 6)
    new_size = min(current_size + 2, 20)  # Максимум 20 сообщений
    context.bot.context_sizes[user_id] = new_size
    await update.message.reply_text(f"✅ Размер контекста увеличен до {new_size} сообщений.")

async def decrease_context(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Уменьшение размера контекста."""
    user_id = update.effective_user.id
    current_size = context.bot.context_sizes.get(user_id, 6)
    new_size = max(current_size - 2, 2)  # Минимум 2 сообщения
    context.bot.context_sizes[user_id] = new_size
    await update.message.reply_text(f"✅ Размер контекста уменьшен до {new_size} сообщений.")