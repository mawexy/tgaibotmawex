import aiohttp
import logging
from core.config import Config
import re

class OpenRouterService:
    def __init__(self):
        self.api_key = Config.OPENROUTER_API_KEY
        self.model = "xiaomi/mimo-v2-flash:free"

    async def generate_text(self, prompt: str, context: list = None) -> str:
        """Генерация ответа с контекстом и экранированием."""
        messages = []
        if context:
            messages.extend(context)
        messages.append({"role": "user", "content": prompt})

        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "model": self.model,
            "messages": messages
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    json=payload,
                    headers=headers
                ) as response:
                    data = await response.json()
                    if "choices" in data and len(data["choices"]) > 0:
                        ai_response = data["choices"][0]["message"]["content"]
                        # Убираем все Markdown-символы (если не нужно форматирование)
                        ai_response = re.sub(r'[*_~`]', '', ai_response)
                        return ai_response
                    else:
                        return "❌ Ошибка: неверный формат ответа."
        except Exception as e:
            logging.error(f"Ошибка OpenRouter: {e}")
            return "❌ Ошибка генерации ответа."