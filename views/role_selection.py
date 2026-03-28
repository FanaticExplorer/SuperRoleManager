import discord
from discord.ui import Button
from services.role_service import role_service
from models.role_config import RoleEntry, Category
from views.base_view import BaseEphemeralView
from typing import Optional, Union


class RoleButton(Button):
    def __init__(
        self,
        role_entry: RoleEntry,
        name: str,
        emoji: Optional[Union[str, discord.Emoji, discord.PartialEmoji]],
        style: discord.ButtonStyle,
        category: Category,
    ):
        super().__init__(
            style=style,
            label=name,
            emoji=emoji,
            custom_id=f"role_{category.id}_{role_entry.id}",
        )
        self.role_entry = role_entry
        self.category = category

    async def callback(self, interaction: discord.Interaction):
        if (
            not isinstance(interaction.user, discord.Member)
            or interaction.guild is None
        ):
            await interaction.response.send_message(
                "This menu only works on a server.", ephemeral=True
            )
            return

        try:
            if self.category.multi_select:
                await role_service.handle_multi_select(
                    interaction.user, self.role_entry
                )
            else:
                await role_service.handle_single_select(
                    interaction.user, self.category, self.role_entry
                )
        except (discord.Forbidden, discord.HTTPException):
            await interaction.response.send_message(
                "Error changing role.", ephemeral=True
            )
            return

        new_view = RoleSelectionView(
            member=interaction.user, category=self.category, guild=interaction.guild
        )
        await new_view.setup_buttons()

        if self.view:
            new_view.message = getattr(self.view, "message", None)

        # update message
        await interaction.response.edit_message(view=new_view)


class RoleSelectionView(BaseEphemeralView):
    def __init__(
        self, member: discord.Member, category: Category, guild: discord.Guild
    ):
        super().__init__()
        self.member = member
        self.category = category
        self.guild = guild

    async def setup_buttons(self):
        for role_entry in self.category.roles:
            guild_role = self.guild.get_role(role_entry.id)
            if guild_role is None:
                continue
            name = await role_service.resolve_name(role_entry, guild_role)
            emoji_res = await role_service.resolve_emoji(role_entry, guild_role)

            # Why did I even install ty bruh
            final_emoji: Optional[Union[str, discord.Emoji, discord.PartialEmoji]] = (
                None
            )
            if (
                emoji_res is not None
                and str(emoji_res) != "None"
                and emoji_res != "None"
            ):
                final_emoji = emoji_res

            style = (
                discord.ButtonStyle.success
                if role_service.has_role(self.member, role_entry.id)
                else discord.ButtonStyle.danger
            )
            self.add_item(
                RoleButton(
                    role_entry=role_entry,
                    name=name,
                    emoji=final_emoji,
                    style=style,
                    category=self.category,
                )
            )
