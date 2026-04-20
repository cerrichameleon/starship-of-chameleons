from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Starship:
    name: str
    captain: str
    ship_class: str = "Explorer"
    status: str = "active"
    crew_count: int = 0


@dataclass
class Fleet:
    name: str
    commander: str
    ships: list[Starship] = field(default_factory=list)
    flagship: str | None = None

    def add_ship(self, ship: Starship) -> None:
        self.ships.append(ship)
        if self.flagship is None:
            self.flagship = ship.name

    def fleet_status(self) -> dict:
        return {
            "name": self.name,
            "commander": self.commander,
            "flagship": self.flagship,
            "ship_count": len(self.ships),
            "ships": [ship.__dict__ for ship in self.ships],
        }
