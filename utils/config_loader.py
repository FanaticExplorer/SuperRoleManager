import yaml
from pathlib import Path
from models.role_config import Category, EmbedConfig, RoleEntry
from utils.logger import logger

def load_config(file_path: str = "config/roles.yaml") -> list[Category]:
    path = Path(file_path)
    if not path.exists():
        logger.error(f"Config file not found: {file_path}")
        return []

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Error reading config: {e}")
        return []

    if not data or "categories" not in data:
        logger.error("Invalid config format: 'categories' key missing")
        return []

    categories = []
    for cat_data in data["categories"]:
        embed_data = cat_data.get("embed", {})
        
        color_val = embed_data.get("color")
        if isinstance(color_val, str) and color_val.startswith("#"):
            color_val = int(color_val[1:], 16)
        elif isinstance(color_val, str) and color_val.startswith("0x"):
            color_val = int(color_val, 16)

        embed = EmbedConfig(
            title=embed_data.get("title", "Select roles"),
            description=embed_data.get("description"),
            image=embed_data.get("image"),
            color=color_val
        )

        roles = []
        for role_data in cat_data.get("roles", []):
            roles.append(RoleEntry(
                id=role_data.get("id"),
                name=role_data.get("name"),
                emoji=role_data.get("emoji")
            ))

        categories.append(Category(
            id=str(cat_data.get("id")),
            name=cat_data.get("name", "Unnamed Category"),
            multi_select=bool(cat_data.get("multi_select", False)),
            embed=embed,
            roles=roles
        ))
        
    logger.info(f"Loaded {len(categories)} categories from config.")
    return categories

