from dataclasses import dataclass
from functools import cached_property
from typing import TypeAlias

from graph_solver.models.city import City
from graph_solver.models.road import Road

Itineracy: TypeAlias = dict[int, Road]


@dataclass
class Travel:
    itineracy: Itineracy

    @cached_property
    def total_distance(self) -> float:
        return sum(road.distance for road in self.itineracy.values())

    @cached_property
    def as_list(self) -> list[City]:
        return [road.first_city for road in self.itineracy.values()]


def create_travel(cities: list[City]) -> Travel:
    itineracy: Itineracy = {}
    index = 0
    while index != len(cities) - 1:
        itineracy[index] = Road(cities[index], cities[index + 1])
        index += 1
    first_city = itineracy[0].first_city
    itineracy.update({index + 1: Road(cities[index], first_city)})
    travel = Travel(itineracy)
    return travel
