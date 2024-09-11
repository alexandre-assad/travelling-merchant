

from pathlib import Path
from random import choice, randint, shuffle
from typing import Dict, List, Tuple, TypeAlias

from src.domain.dataclass.city import City
from src.domain.dataclass.road import Road
from src.domain.dataclass.travel import Travel
from src.parser.csv_parser import parse_csv_to_list_city

def _generate_travel_from_parent(parent_travels: List[Travel], start_city: City) -> Dict[int, Road]:
    final_travel = {}
    all_cities = [road.first_city for road in parent_travels[0].itinerary.values()]
    all_cities.remove(start_city)
    
    road_index = 0
    while len(all_cities) > 0:
        parent_roads = []
        for travel in parent_travels:
            for road in travel.itinerary.values():
                if road.first_city == start_city and road.second_city in all_cities:
                    parent_roads.append(road) 
        if len(parent_roads) < 1:
            random_city = choice(all_cities)
            final_travel[road_index] = Road(start_city, random_city)
            start_city = random_city
            all_cities.remove(start_city)
        else:
            parent_roads = sorted(parent_roads, key=lambda x: x.distance)
            final_travel[road_index] = parent_roads[0]
            start_city = parent_roads[0].second_city
            all_cities.remove(start_city)
        road_index += 1
    return final_travel
  


def _generate_two_travel(parent_travels: List[Travel]) ->  List[Travel]:
    final_travels = []
    for travel in parent_travels:
        start_city = travel.itinerary[0].first_city
        final_travels.append(Travel(_generate_travel_from_parent(parent_travels, start_city)))
    return final_travels


def _find_new_mixed_travels(best_travels: List[Travel]) ->  List[Travel]:
    for parent_index in range(0, len(best_travels), 2):
        children_travels = _generate_two_travel(best_travels)
        best_travels += children_travels
    return best_travels


def _generate_random_travel(cities: List[City]) -> Travel:
    
    itineracy = {}
    start_city = choice(cities)

    current_city = start_city
    index = 0
    shuffle(cities)
    for index, city in enumerate(cities):
        itineracy[index] = Road(current_city, city)
        current_city = city
    
    itineracy[index+1] = Road(current_city, start_city)
    return Travel(itineracy)    



def _first_genetic_generation(cities: List[City], number_merchant: int) -> List[Travel]:
    travels = []
    for _ in range(number_merchant):
        travels.append(_generate_random_travel(cities.copy()))
    return sorted(travels, key= lambda x: x.total_distance, reverse=True)[:round(number_merchant/2)]


def genetic_algorithm(file_path: str, generations: int = 500, number_merchant: int = 100, mutation_rate_percent: int = 5) -> List[Travel]:
    best_travels = []
    cities = parse_csv_to_list_city(file_path)

    half_best_travels = _first_genetic_generation(cities.copy(), number_merchant)
    best_travels.append(half_best_travels[0])

    for generation in range(1, generations):
        print(generation)
        travels = _find_new_mixed_travels(half_best_travels)
        # travels = genetic_mutation(travels, mutation_rate_percent)
        half_best_travels = sorted(travels, key= lambda x: x.total_distance, reverse=True)[:round(number_merchant/2)]
        best_travels.append(half_best_travels[0])

    return best_travels


