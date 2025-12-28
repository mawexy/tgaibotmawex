from github import Github
import json
import logging
from core.config import Config

class GitHubService:
    def __init__(self):
        self.github = Github(Config.GITHUB_TOKEN)
        self.repo = self.github.get_repo(Config.GITHUB_REPO)

    async def load_history(self) -> dict:
        try:
            content = self.repo.get_contents(Config.HISTORY_FILE)
            return json.loads(content.decoded_content.decode())
        except Exception as e:
            logging.error(f"Ошибка загрузки истории: {e}")
            return {}

    async def save_history(self, history: dict):
        try:
            self.repo.update_file(
                Config.HISTORY_FILE,
                "Обновление истории диалогов",
                json.dumps(history, indent=2),
                self.repo.get_contents(Config.HISTORY_FILE).sha
            )
        except Exception as e:
            logging.error(f"Ошибка сохранения истории: {e}")
