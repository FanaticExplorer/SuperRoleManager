from discord.ext import commands
from views.main_menu import MainMenuView
from services.role_service import role_service
from utils.embeds import build_embed
from utils.logger import logger


class RoleMenu(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="setup")
    @commands.has_permissions(administrator=True)
    async def setup_menu(self, ctx: commands.Context):
        """Creates the main role menu"""
        if not role_service.categories:
            await ctx.send("Role config is empty. Check `roles.yaml`.")
            return

        embed = build_embed(role_service.main_menu.embed)
        view = MainMenuView(guild=ctx.guild)
        await ctx.send(embed=embed, view=view)


def setup(bot: commands.Bot):
    bot.add_cog(RoleMenu(bot))
    logger.debug("RoleMenu cog loaded.")
