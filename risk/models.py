from __future__ import annotations
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from typing import Dict, Set, List

class Player:
    """Represents a player in the game."""
    def __init__(self, name: str):
        self.name = name
        self.territories: List[Territory] = []

    def __str__(self) -> str:
        return self.name

class Territory:
    """Represents a single territory on the map."""
    def __init__(self, name: str):
        self.name = name
        self.owner: Optional[Player] = None
        self.armies: int = 0

    def __str__(self) -> str:
        owner_name = self.owner.name if self.owner else "None"
        return f"{self.name} (Owner: {owner_name}, Armies: {self.armies})"

class Map:
    """Represents the game map, containing all territories and their connections."""
    def __init__(self):
        self.territories: Dict[str, Territory] = {}
        self.adjacencies: Dict[str, Set[str]] = {}

    def add_territory(self, territory: Territory):
        """Adds a territory to the map."""
        if territory.name not in self.territories:
            self.territories[territory.name] = territory
            self.adjacencies[territory.name] = set()

    def add_connection(self, territory_name1: str, territory_name2: str):
        """Adds a connection between two territories."""
        if territory_name1 in self.territories and territory_name2 in self.territories:
            self.adjacencies[territory_name1].add(territory_name2)
            self.adjacencies[territory_name2].add(territory_name1)
        else:
            raise ValueError("One or both territories not found in map.")

    def get_territory(self, name: str) -> Territory:
        """Gets a territory by its name."""
        return self.territories[name]
