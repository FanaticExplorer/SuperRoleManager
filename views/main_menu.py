import discord
from discord.ui import Button
from typing import Optional

from services.role_service import role_service
from utils.embeds import build_embed
from utils.emoji import resolve_emoji
from views.category_menu import CategoryMenuView

# Changing this orphans every menu already posted to a channel.
MAIN_MENU_BUTTON_ID = "persistent_main_menu_button"


class MainMenuButton(Button):
    def __init__(self, guild: Optional[discord.Guild] = None):
        conf = role_service.main_menu.button
        super().__init__(
            label=conf.label,
            emoji=resolve_emoji(conf.emoji, guild),
            style=discord.ButtonStyle.primary,
            custom_id=MAIN_MENU_BUTTON_ID,
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        view = CategoryMenuView(guild=interaction.guild)
        embed = build_embed(role_service.category_menu)

        await interaction.followup.send(embed=embed, ephemeral=True, view=view)


class MainMenuView(discord.ui.View):
    def __init__(self, guild: Optional[discord.Guild] = None):
        super().__init__(timeout=None)
        self.add_item(MainMenuButton(guild))
