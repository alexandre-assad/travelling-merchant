from random import randint, shuffle

from pandas import DataFrame

from graph_solver.models.city import City
from graph_solver.models.road import Road
from graph_solver.models.travel import Itineracy, Travel, create_travel
from graph_solver.profilers import profile


def _create_inteneracy(first_travel: Travel, second_travel: Travel) -> Itineracy:
    intineracy = {}
    random_treshold = randint(8, 14)
    all_cities = set(first_travel.as_list)

    parents_set_cities = set(
        first_travel.as_list[:random_treshold] + second_travel.as_list[random_treshold:]
    )
    visited_cities = set(parents_set_cities)
    cities_left = list(all_cities - visited_cities)
    shuffle(cities_left)
    updated_cities = list(parents_set_cities) + cities_left

    selected_city = updated_cities[0]
    leftover_cities = updated_cities[1:]

    for index, city in enumerate(leftover_cities):
        intineracy[index] = Road(selected_city, city)
        selected_city = city

    return intineracy


def _generate_two_travel(parent_travels: list[Travel]) -> list[Travel]:
    final_travels = []
    final_travels.append(
        Travel(_create_inteneracy(parent_travels[0], parent_travels[1]))
    )
    final_travels.append(
        Travel(_create_inteneracy(parent_travels[1], parent_travels[0]))
    )
    return final_travels


def _find_new_mixed_travels(best_travels: list[Travel]) -> list[Travel]:
    for _ in range(0, len(best_travels), 2):
        children_travels = _generate_two_travel(best_travels)
        best_travels += children_travels
    return best_travels


def _first_genetic_generation(cities: list[City], number_merchant: int) -> list[Travel]:
    travels = []
    for _ in range(number_merchant):
        random_cities = cities.copy()
        shuffle(random_cities)
        travels.append(create_travel(random_cities))
    return sorted(travels, key=lambda x: x.total_distance, reverse=True)[
        : round(number_merchant / 2)
    ]


def _find_best_travel(
    cities: list[City], generations: int, number_merchant: int
) -> Travel:
    best_travels = []
    half_best_travels = _first_genetic_generation(cities.copy(), number_merchant)
    best_travels.append(half_best_travels[0])
    for _ in range(1, generations):
        travels = _find_new_mixed_travels(half_best_travels)
        half_best_travels = sorted(
            travels, key=lambda x: x.total_distance, reverse=True
        )[: round(number_merchant / 2)]
        best_travels.append(half_best_travels[0])
    best_travel = best_travels[-1]
    return best_travel


def _df_to_cities(cities_data: DataFrame) -> list[City]:
    cities = []
    for _, row in cities_data.iterrows():
        cities.append(
            City(
                name=row["Ville"], longitude=row["Longitude"], latitude=row["Latitude"]
            )
        )
    return cities


@profile
def genetic_algorithm(
    cities_data: DataFrame,
    generations: int,
    number_merchant: int,
) -> Travel:
    cities = _df_to_cities(cities_data)
    best_travel = _find_best_travel(cities, generations, number_merchant)
    return best_travel
