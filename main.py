import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from services.role_service import role_service
from utils.config_watcher import config_watcher
from utils.logger import logger
from views.main_menu import MainMenuView

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
        logger.debug("Persistent views loaded.")
        try:
            self.load_extension("cogs.role_menu")
        except discord.ExtensionError as e:
            logger.exception(f"Failed to load extension cogs.role_menu: {e}")

        if self.user:
            logger.info(f"Logged in as {self.user} (ID: {self.user.id})")

        logger.debug(f"Loaded {len(role_service.categories)} categories from config.")

        # Start the config watcher for hot reload
        config_watcher.start()


if __name__ == "__main__":
    if not TOKEN:
        logger.critical("BOT_TOKEN not found in .env file.")
    else:
        import asyncio

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        bot = SuperRoleManager()
        bot.run(TOKEN)
