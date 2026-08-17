import yaml
from pathlib import Path
from typing import Any, Optional

from models.role_config import (
    BotConfig,
    ButtonConfig,
    Category,
    EmbedConfig,
    MainMenuConfig,
    RoleEntry,
)
from utils.logger import logger


def _parse_color(value: Any) -> Optional[int]:
    if isinstance(value, str):
        text = value.strip()
        if text.startswith("#"):
            text = text[1:]
        try:
            return int(text, 16)
        except ValueError:
            logger.warning(f"Invalid embed color: {value!r}, ignoring")
            return None
    return value


def _parse_embed(data: Any, default_title: str) -> EmbedConfig:
    data = data or {}
    return EmbedConfig(
        title=data.get("title", default_title),
        description=data.get("description"),
        image=data.get("image"),
        color=_parse_color(data.get("color")),
        footer=data.get("footer"),
    )


def _parse_main_menu(data: Any) -> MainMenuConfig:
    data = data or {}
    button_data = data.get("button") or {}
    return MainMenuConfig(
        embed=_parse_embed(data.get("embed"), "Self roles"),
        button=ButtonConfig(
            label=button_data.get("label", "Get started"),
            emoji=button_data.get("emoji"),
        ),
    )


def _parse_categories(data: Any) -> list[Category]:
    categories = []
    for cat_data in data or []:
        roles = [
            RoleEntry(
                id=role_data.get("id"),
                name=role_data.get("name"),
                emoji=role_data.get("emoji"),
            )
            for role_data in cat_data.get("roles", [])
        ]

        categories.append(
            Category(
                id=str(cat_data.get("id")),
                name=cat_data.get("name", "Unnamed Category"),
                multi_select=bool(cat_data.get("multi_select", False)),
                embed=_parse_embed(cat_data.get("embed"), "Select roles"),
                roles=roles,
                emoji=cat_data.get("emoji"),
            )
        )
    return categories


def load_config(file_path: str = "config/roles.yaml") -> BotConfig:
    path = Path(file_path)
    if not path.exists():
        logger.critical(f"Config file not found: {file_path}")
        return BotConfig()

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        logger.exception(f"Error reading config: {e}")
        return BotConfig()

    if not data or "categories" not in data:
        logger.critical("Invalid config format: 'categories' key missing")
        return BotConfig()

    config = BotConfig(
        categories=_parse_categories(data["categories"]),
        main_menu=_parse_main_menu(data.get("main_menu")),
        category_menu=_parse_embed(data.get("category_menu"), "Pick a category"),
    )

    logger.debug(f"Loaded {len(config.categories)} categories from config.")
    return config
