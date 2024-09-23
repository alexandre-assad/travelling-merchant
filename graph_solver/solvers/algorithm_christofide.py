# missing stubs
from itertools import combinations
from math import atan2, cos, radians, sin, sqrt

from networkx import (  # type: ignore
    Graph,
    MultiGraph,
    eulerian_circuit,
    matching,
    minimum_spanning_tree,
)
from pandas import DataFrame

from graph_solver.models.city import City
from graph_solver.models.travel import Travel, create_travel
from graph_solver.profilers import profile


def _haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    )
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance


def _compute_distance_matrix(data: DataFrame) -> dict[tuple[int, int], float]:
    num_villes = len(data)
    distance_matrix = {}
    for i, j in combinations(range(num_villes), 2):
        lat1, lon1 = data.iloc[i]["Latitude"], data.iloc[i]["Longitude"]
        lat2, lon2 = data.iloc[j]["Latitude"], data.iloc[j]["Longitude"]
        distance = _haversine_distance(lat1, lon1, lat2, lon2)
        distance_matrix[(i, j)] = distance
        distance_matrix[(j, i)] = distance
    return distance_matrix


def _christofides_tsp(
    distance_matrix: dict[tuple[int, int], float]
) -> list[tuple[int, int]]:
    graph = Graph()
    for (i, j), dist in distance_matrix.items():
        graph.add_edge(i, j, weight=dist)
    mst = minimum_spanning_tree(graph)
    odd_degree_nodes = [v for v in mst.nodes() if mst.degree(v) % 2 == 1]
    subgraph_odd = graph.subgraph(odd_degree_nodes)
    min_weight_matching = matching.min_weight_matching(subgraph_odd, weight="weight")
    multigraph = MultiGraph(mst)
    multigraph.add_edges_from(min_weight_matching)
    circuit = list(eulerian_circuit(multigraph))
    visited = set()
    hamiltonian_path = []
    for u in circuit:
        if u not in visited:
            visited.add(u)
            hamiltonian_path.append(u)
    hamiltonian_path.append(hamiltonian_path[0])
    return hamiltonian_path


def _create_travel_from_indexes(
    indexes: list[tuple[int, int]], cities_data: DataFrame
) -> Travel:
    iteneracy = []
    for index_tuple in indexes:
        _, city_idx = index_tuple
        name = cities_data.iloc[city_idx]["Ville"]
        lat = cities_data.iloc[city_idx]["Latitude"]
        lon = cities_data.iloc[city_idx]["Longitude"]
        city = City(name, lon, lat)
        iteneracy.append(city)
    travel = create_travel(iteneracy)
    return travel


@profile
def christofide_algorithm(cities_data: DataFrame) -> Travel:
    distance_matrix = _compute_distance_matrix(cities_data)
    order = _christofides_tsp(distance_matrix)
    travel = _create_travel_from_indexes(order, cities_data)
    return travel
