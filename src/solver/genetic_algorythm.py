

from pathlib import Path
from random import choice, randint, shuffle
from typing import Dict, List, Tuple, TypeAlias

from src.domain.dataclass.city import City
from src.domain.dataclass.road import Road
from src.domain.dataclass.travel import Travel
from src.parser.csv_parser import parse_csv_to_list_city

def _generate_travel_from_parent(first_travel: Travel, second_travel: Travel) -> Dict[int, Road]:
    intineracy = {}
    random_treshold = randint(8,14)
    all_cities = set(first_travel.itineray_cities)

    parents_set_cities = set(first_travel.itineray_cities[:random_treshold] + second_travel.itineray_cities[random_treshold:]) 
    visited_cities = set(parents_set_cities)
    cities_left = list(all_cities - visited_cities)
    shuffle(cities_left)
    parents_set_cities = list(parents_set_cities) + cities_left

    current_city = parents_set_cities[0]
    parents_set_cities = parents_set_cities[1:]
    for index, city in enumerate(parents_set_cities):
        intineracy[index] = Road(current_city, city)
        current_city = city

    return intineracy
    
def _generate_two_travel(parent_travels: List[Travel]) ->  List[Travel]:
    final_travels = []
    final_travels.append(Travel(_generate_travel_from_parent(parent_travels[0], parent_travels[1])))
    final_travels.append(Travel(_generate_travel_from_parent(parent_travels[1], parent_travels[0])))
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

    for _ in range(1, generations):
        travels = _find_new_mixed_travels(half_best_travels)
        # travels = genetic_mutation(travels, mutation_rate_percent)
        half_best_travels = sorted(travels, key= lambda x: x.total_distance, reverse=True)[:round(number_merchant/2)]
        best_travels.append(half_best_travels[0])

    print(best_travels[-1].total_distance)
    return best_travels


