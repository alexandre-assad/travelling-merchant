
from dataclasses import dataclass
from typing import Dict

from src.domain.dataclass.road import Road


@dataclass
class Travel:
    itinerary: Dict[int, Road]

    @property
    def total_distance(self) -> float:
        return sum(road.distance for road in self.itinerary.values())