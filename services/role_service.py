import discord
from typing import Optional
from discord import PartialEmoji
from models.role_config import BotConfig, Category, EmbedConfig, MainMenuConfig, RoleEntry
from utils.logger import logger
from utils.config_loader import load_config
from utils.emoji import resolve_emoji


class RoleService:
    def __init__(self):
        self.config: BotConfig = BotConfig()
        self.reload_config()

    def reload_config(self):
        self.config = load_config()

    @property
    def categories(self) -> list[Category]:
        return self.config.categories

    @property
    def main_menu(self) -> MainMenuConfig:
        return self.config.main_menu

    @property
    def category_menu(self) -> EmbedConfig:
        return self.config.category_menu

    def get_category_by_id(self, category_id: str) -> Optional[Category]:
        for cat in self.categories:
            if cat.id == category_id:
                return cat
        return None

    @staticmethod
    def get_user_roles_in_category(
        member: discord.Member, category: Category
    ) -> list[discord.Role]:
        cat_role_ids = {r.id for r in category.roles}
        return [r for r in member.roles if r.id in cat_role_ids]

    @staticmethod
    def has_role(member: discord.Member, role_id: int) -> bool:
        return any(r.id == role_id for r in member.roles)

    @staticmethod
    async def add_role(member: discord.Member, role_id: int):
        try:
            role = member.guild.get_role(role_id)
            if not role:
                logger.warning(f"Role {role_id} not found in guild.")
                return
            await member.add_roles(role)
            logger.debug(f"[+] {member} received role {role.name} ({role_id})")
        except discord.Forbidden as e:
            logger.warning(f"No permissions to assign role {role_id} to member {member}: {e}")
            raise
        except discord.HTTPException as e:
            logger.exception(f"HTTP error assigning role {role_id}: {e}")
            raise

    @staticmethod
    async def remove_role(member: discord.Member, role_id: int):
        try:
            role = member.guild.get_role(role_id)
            if not role:
                logger.warning(f"Role {role_id} not found in guild.")
                return
            await member.remove_roles(role)
            logger.debug(f"[-] {member} lost role {role.name} ({role_id})")
        except discord.Forbidden as e:
            logger.warning(f"No permissions to remove role {role_id} from member {member}: {e}")
            raise
        except discord.HTTPException as e:
            logger.exception(f"HTTP error removing role {role_id}: {e}")
            raise

    async def handle_single_select(
        self, member: discord.Member, category: Category, new_role: RoleEntry
    ):
        current_roles = self.get_user_roles_in_category(member, category)
        # Remove other roles in category
        for r in current_roles:
            if r.id != new_role.id:
                await self.remove_role(member, r.id)

        if self.has_role(member, new_role.id):
            await self.remove_role(
                member, new_role.id
            )  # Toggle off if they click current
        else:
            await self.add_role(member, new_role.id)

    async def handle_multi_select(self, member: discord.Member, role: RoleEntry):
        if self.has_role(member, role.id):
            await self.remove_role(member, role.id)
        else:
            await self.add_role(member, role.id)

    @staticmethod
    async def resolve_name(role_entry: RoleEntry, guild_role: discord.Role) -> str:
        if role_entry.name:
            return role_entry.name
        return guild_role.name if guild_role else "Unknown Role"

    @staticmethod
    async def resolve_emoji(
        role_entry: RoleEntry,
        guild_role: discord.Role,
        guild: Optional[discord.Guild] = None,
    ) -> Optional[PartialEmoji | str]:
        if role_entry.emoji is None:
            return None

        if str(role_entry.emoji).strip() == "0":
            if guild_role:
                guild_emoji = getattr(guild_role, "emoji", None)
                if guild_emoji:
                    return guild_emoji
            return None

        return resolve_emoji(role_entry.emoji, guild)


role_service = RoleService()
