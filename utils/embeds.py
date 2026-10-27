import discord

from models.role_config import EmbedConfig


def build_embed(conf: EmbedConfig) -> discord.Embed:
    """Render an EmbedConfig from the YAML into a Discord embed."""
    embed = discord.Embed(
        title=conf.title,
        description=conf.description,
        color=conf.color,
    )
    if conf.image:
        embed.set_image(url=conf.image)
    if conf.footer:
        embed.set_footer(text=conf.footer)
    return embed
