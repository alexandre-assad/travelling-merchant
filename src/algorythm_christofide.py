import pandas as pd
import folium
import networkx as nx
import os
from math import radians, sin, cos, sqrt, atan2
from itertools import combinations

#Haversine distance
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Hearth radius
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

#matrix of Cities distance
def compute_distance_matrix(data):
    num_villes = len(data)
    distance_matrix = {}
    for i, j in combinations(range(num_villes), 2):
        lat1, lon1 = data.iloc[i]['Latitude'], data.iloc[i]['Longitude']
        lat2, lon2 = data.iloc[j]['Latitude'], data.iloc[j]['Longitude']
        distance = haversine(lat1, lon1, lat2, lon2)
        distance_matrix[(i, j)] = distance
        distance_matrix[(j, i)] = distance
    return distance_matrix

#Christofides algorytm
def christofides_tsp(data, distance_matrix):
    G = nx.Graph()

    #ajout des arêtes ans le graph
    for (i, j), dist in distance_matrix.items():
        G.add_edge(i, j, weight=dist)

    # 1.arbre couvrant minimum (MST)
    mst = nx.minimum_spanning_tree(G)

    # 2.les sommets de degré impair dans le MST
    odd_degree_nodes = [v for v in mst.nodes() if mst.degree(v) % 2 == 1]

    # 3.un couplage parfait minimal pour les sommets impairs
    subgraph_odd = G.subgraph(odd_degree_nodes)
    min_weight_matching = nx.algorithms.matching.min_weight_matching(subgraph_odd, weight='weight')

    # 4.  multigraphe Eulerien
    multigraph = nx.MultiGraph(mst)
    multigraph.add_edges_from(min_weight_matching)

    # 5.cycle Eulerien dans le multigraphe
    eulerian_circuit = list(nx.eulerian_circuit(multigraph))

    # 6.retirer les doublons
    visited = set()
    hamiltonian_path = []
    for u, v in eulerian_circuit:
        if u not in visited:
            visited.add(u)
            hamiltonian_path.append(u)

    # retour sur la ville de départ
    hamiltonian_path.append(hamiltonian_path[0])

    return hamiltonian_path

#la distance totale
def calculer_distance_totale(itinerary, data):
    distance_totale = 0
    for i in range(len(itinerary) - 1):
        ville1 = data.iloc[itinerary[i]]
        ville2 = data.iloc[itinerary[i + 1]]
        lat1, lon1 = ville1['Latitude'], ville1['Longitude']
        lat2, lon2 = ville2['Latitude'], ville2['Longitude']
        distance = haversine(lat1, lon1, lat2, lon2)
        distance_totale += distance
    return distance_totale

#matrice des distances
distance_matrix = compute_distance_matrix(data)

#itinéraire avec l'algorithme de Christofides
itinerary = christofides_tsp(data, distance_matrix)

#distance totale de l'itinéraire généré
distance_totale = calculer_distance_totale(itinerary, data)
print(f"Distance totale de l'itinéraire : {distance_totale:.2f} km")

#centrer la carte sur la France (coordonnées approximatives)
map_france = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

#les étapes de l'itinéraire dans la console et ajout des marqueurs sur la carte
print("Étapes de l'itinéraire :")
for i, city_idx in enumerate(itinerary):
    city_name = data.iloc[city_idx]['Ville']
    city_lat = data.iloc[city_idx]['Latitude']
    city_lon = data.iloc[city_idx]['Longitude']
    
   
    print(f"{i + 1} - {city_name}")
    
    #popup
    folium.Marker(
        [city_lat, city_lon],
        popup=f"{i + 1} - {city_name}",
        icon=folium.Icon(color="pink", icon="info-sign")
    ).add_to(map_france)

# les lignes de l'itinéraire
city_coordinates = [(data.iloc[i]['Latitude'], data.iloc[i]['Longitude']) for i in itinerary]
folium.PolyLine(city_coordinates, color="blue", weight=2.5, opacity=1).add_to(map_france)

# création de fichier HTML
sortie_html = ""
map_france.save(sortie_html)
print(f"La carte a été sauvegardée sous le nom '{sortie_html}'")