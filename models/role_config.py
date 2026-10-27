from dataclasses import dataclass, field


@dataclass
class EmbedConfig:
    title: str
    description: str | None = None
    image: str | None = None
    color: int | None = None
    footer: str | None = None


@dataclass
class ButtonConfig:
    label: str
    emoji: str | int | None = None


@dataclass
class RoleEntry:
    id: int
    name: str | None
    emoji: str | int | None


@dataclass
class Category:
    id: str
    name: str
    multi_select: bool
    roles: list[RoleEntry]
    embed: EmbedConfig
    emoji: str | None = None


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
