
from dataclasses import dataclass
from functools import cached_property
from typing import Dict

from src.domain.dataclass.city import City
from src.domain.dataclass.road import Road


@dataclass
class Travel:
    itineracy: Dict[int, Road]

    @cached_property
    def total_distance(self) -> float:
        return sum(road.distance for road in self.itineracy.values())
    
    @cached_property
    def itineray_cities(self) -> list[City]:
        return  [road.first_city for road in self.itineracy.values()] + [self.itineracy[19].second_city]