from telegram.ext import Application, CommandHandler, MessageHandler, filters
from core.handlers.start import start, help_command
from core.handlers.mission import mission, status
from core.handlers.memory import cleanmem, increase_context, decrease_context
from core.handlers.prompt import setprompt, user_prompts
from core.config import Config
from services.openrouter import OpenRouterService
import logging

class PhantomBot:
    def __init__(self):
        self.app = Application.builder().token(Config.TELEGRAM_TOKEN).build()
        self.openrouter = OpenRouterService()
        self._setup_handlers()
        # Хранилище контекста и его размера
        self.context_history = {}
        self.context_sizes = {}  # Размер контекста для каждого пользователя

    def _setup_handlers(self):
        # Команды
        self.app.add_handler(CommandHandler("start", start))
        self.app.add_handler(CommandHandler("help", help_command))
        self.app.add_handler(CommandHandler("mission", mission))
        self.app.add_handler(CommandHandler("status", status))
        self.app.add_handler(CommandHandler("cleanmem", cleanmem))
        self.app.add_handler(CommandHandler("increase_context", increase_context))
        self.app.add_handler(CommandHandler("decrease_context", decrease_context))
        self.app.add_handler(CommandHandler("setprompt", setprompt))

        # Обработка сообщений
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_message))

    async def _handle_message(self, update, context):
        """Обработка сообщений с контекстом."""
        user_id = update.effective_user.id
        user_text = update.message.text

        try:
            # Показываем статус "печатает"
            await update.message.chat.send_action(action="typing")

            # Получаем контекст пользователя
            user_context = self.context_history.get(user_id, [])
            user_context.append({"role": "user", "content": user_text})

            # Генерируем ответ
            ai_response = await self.openrouter.generate_text(
                prompt=user_text,
                context=user_context
            )

            # Сохраняем ответ в контекст
            user_context.append({"role": "assistant", "content": ai_response})

            # Получаем размер контекста (по умолчанию 6)
            context_size = self.context_sizes.get(user_id, 6)
            self.context_history[user_id] = user_context[-context_size:]

            # Отправляем ответ
            await update.message.reply_text(ai_response)
        except Exception as e:
            logging.error(f"Ошибка обработки сообщения: {e}")
            await update.message.reply_text("❌ Ошибка обработки сообщения.")

    def run(self):
        logging.info("Запуск бота Phantom-Core...")
        self.app.run_polling()