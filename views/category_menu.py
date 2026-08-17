import discord
from typing import Optional
from services.role_service import role_service
from utils.embeds import build_embed
from utils.emoji import resolve_emoji
from views.role_selection import RoleSelectionView
from views.base_view import BaseEphemeralView


class CategoryMenuView(BaseEphemeralView):
    def __init__(self, guild: Optional[discord.Guild] = None):
        super().__init__()
        for category in role_service.categories:
            btn = discord.ui.Button(
                label=category.name,
                custom_id=f"cat_{category.id}",
                style=discord.ButtonStyle.secondary,
                emoji=resolve_emoji(category.emoji, guild),
            )
            btn.callback = self.make_callback(category.id)
            self.add_item(btn)

    @staticmethod
    def make_callback(category_id: str):
        async def callback(interaction: discord.Interaction):
            guild = interaction.guild
            member = interaction.user
            if not isinstance(member, discord.Member) or guild is None:
                await interaction.response.send_message(
                    "This menu only works on a server.", ephemeral=True
                )
                return

            # Always get the fresh category from service (important for hot reload!)
            category = role_service.get_category_by_id(category_id)
            if category is None:
                await interaction.response.send_message(
                    "Category not found. Please update the menu.", ephemeral=True
                )
                return

            await interaction.response.defer(ephemeral=True)

            view = RoleSelectionView(member=member, category=category, guild=guild)
            await view.setup_buttons()

            embed = build_embed(category.embed)

            await interaction.followup.send(
                embed=embed, ephemeral=True, view=view
            )

        return callback
