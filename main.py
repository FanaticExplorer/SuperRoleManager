import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from utils.logger import logger
from views.main_menu import MainMenuView
from services.role_service import role_service

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")


class SuperRoleManager(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        super().__init__(command_prefix="role!", intents=intents, help_command=None)

    async def on_ready(self):
        self.add_view(MainMenuView())
        logger.info("Persistent views loaded.")
        try:
            self.load_extension("cogs.role_menu")
        except Exception as e:
            logger.error(f"Failed to load extension cogs.role_menu: {e}")

        if self.user:
            logger.info(f"Logged in as {self.user} (ID: {self.user.id})")
        else:
            logger.info("Logged in.")

        logger.info(f"Loaded {len(role_service.categories)} categories from config.")


if __name__ == "__main__":
    if not TOKEN:
        logger.error("BOT_TOKEN not found in .env file.")
    else:
        import asyncio

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        bot = SuperRoleManager()
        bot.run(TOKEN)
