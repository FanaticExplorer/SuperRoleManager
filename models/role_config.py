from dataclasses import dataclass
from typing import Optional, Union

@dataclass
class EmbedConfig:
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    color: Optional[int] = None

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
