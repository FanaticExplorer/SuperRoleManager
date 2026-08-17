from dataclasses import dataclass, field
from typing import Optional, Union


@dataclass
class EmbedConfig:
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    color: Optional[int] = None
    footer: Optional[str] = None


@dataclass
class ButtonConfig:
    label: str
    emoji: Union[str, int, None] = None


@dataclass
class RoleEntry:
    id: int
    name: Optional[str]
    emoji: Union[str, int, None]


@dataclass
class Category:
    id: str
    name: str
    multi_select: bool
    roles: list[RoleEntry]
    embed: EmbedConfig
    emoji: Optional[str] = None


@dataclass
class MainMenuConfig:
    """The public, persistent message posted by `role!setup`."""

    embed: EmbedConfig
    button: ButtonConfig


def _default_main_menu() -> MainMenuConfig:
    return MainMenuConfig(
        embed=EmbedConfig(title="Self roles"),
        button=ButtonConfig(label="Get started"),
    )


def _default_category_menu() -> EmbedConfig:
    return EmbedConfig(title="Pick a category")


@dataclass
class BotConfig:
    categories: list[Category] = field(default_factory=list)
    main_menu: MainMenuConfig = field(default_factory=_default_main_menu)
    category_menu: EmbedConfig = field(default_factory=_default_category_menu)
