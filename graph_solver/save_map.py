# missing stubs
from folium import Icon, Map, Marker, PolyLine  # type: ignore

from graph_solver.models.travel import Travel


def create_map(travel: Travel) -> Map:
    france_location = [46.603354, 1.888334]
    map_france = Map(location=france_location, zoom_start=6)

    for index, road in travel.itineracy.items():
        city = road.first_city
        Marker(
            [city.latitude, city.longitude],
            popup=f"{index + 1} - {city.name}",
            icon=Icon(color="pink", icon="info-sign"),
        ).add_to(map_france)
    last_index = len(travel.itineracy)
    city = travel.itineracy[last_index].second_city
    Marker(
        [city.latitude, city.longitude],
        popup=f"{21} - {city.name}",
        icon=Icon(color="pink", icon="info-sign"),
    ).add_to(map_france)

    city_coordinates = [
        (road.first_city.latitude, road.first_city.longitude)
        for road in travel.itineracy.values()
    ] + [
        (
            travel.itineracy[last_index].second_city.latitude,
            travel.itineracy[last_index].second_city.longitude,
        )
    ]
    PolyLine(city_coordinates, color="blue", weight=2.5, opacity=1).add_to(map_france)
    return map_france
