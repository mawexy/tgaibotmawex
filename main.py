from core.bot import PhantomBot
from core.config import Config

def main():
    Config.setup_logging()
    bot = PhantomBot()
    bot.run()

if __name__ == "__main__":
    main()
