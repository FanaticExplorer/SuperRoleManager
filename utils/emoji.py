
import discord
from discord import PartialEmoji

from utils.logger import logger


def resolve_emoji(
    value: str | int | None,
    guild: discord.Guild | None = None,
) -> PartialEmoji | str | None:
    """
    Turn a raw YAML emoji value into something a button can render.

    Custom emoji from a guild the bot cannot see are dropped: Discord rejects
    the whole message with a 400 rather than falling back to a placeholder, so
    one stale ID would otherwise take the entire menu down.

    "-1" (none) and "0" (role icon) both resolve to None here; the role icon
    lookup needs a Role object and lives in RoleService.
    """
    if value is None:
        return None

    raw = str(value).strip()
    if not raw or raw in ("-1", "0"):
        return None

    if raw.isdigit():
        emoji_id = int(raw)
        if guild is not None and guild.get_emoji(emoji_id) is None:
            logger.warning(f"Emoji ID {emoji_id} not available to the bot, omitting")
            return None
        return PartialEmoji(name="e", id=emoji_id)

    parsed = PartialEmoji.from_str(raw)
    if (
        parsed.is_custom_emoji()
        and parsed.id is not None
        and guild is not None
        and guild.get_emoji(parsed.id) is None
    ):
        logger.warning(f"Emoji {raw} not available to the bot, omitting")
        return None

    return raw
