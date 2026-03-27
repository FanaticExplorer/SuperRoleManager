import discord
from discord.ext import commands
from views.main_menu import MainMenuView
from services.role_service import role_service
from utils.logger import logger

class RoleMenu(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="setup")
    @commands.has_permissions(administrator=True)
    async def setup_menu(self, ctx: commands.Context):
        """Создает главное меню ролей"""
        if not role_service.categories:
            await ctx.send("Конфиг ролей пуст. Проверьте `roles.yaml`.")
            return

        embed = discord.Embed(
            title="Меню ролей", 
            description="Нажмите на кнопку ниже, чтобы выбрать ваши роли.", 
            color=0x5865F2
        )
        view = MainMenuView()
        await ctx.send(embed=embed, view=view)

def setup(bot: commands.Bot):
    bot.add_cog(RoleMenu(bot))
    logger.info("RoleMenu cog loaded.")

