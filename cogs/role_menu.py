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
        """Creates the main role menu"""
        if not role_service.categories:
            await ctx.send("Role config is empty. Check `roles.yaml`.")
            return

        embed = discord.Embed(
            title="Приветствуем вас в данном канале! <a:FP_hiii:1384959468831248484>",
            description="Хотите что бы люди побольше узнали о вас, или желаете получать важные уведомления о активностях на сервере?\nЗдесь вы можете выбрать интересующие вас роли!",
            color=0xf8ce72,
        )
        embed.set_image(url="https://cdn.discordapp.com/attachments/1018534366797889536/1487464645651464392/1embed.jpg?ex=69c93ce7&is=69c7eb67&hm=9dd8d414b950f0a7842786172e552f870aa0dc3993a0148de0b4dcd77899ae4d&")
        embed.set_footer(text="В случае неполадок пишите fanaticexplorer")
        view = MainMenuView()
        await ctx.send(embed=embed, view=view)


def setup(bot: commands.Bot):
    bot.add_cog(RoleMenu(bot))
    logger.debug("RoleMenu cog loaded.")
