from dataclasses import dataclass
from math import atan2, cos, pi, sin, sqrt

from src.domain.dataclass.city import City

def degree_to_radius(degree: float) -> float:
    return degree * pi / 180

@dataclass
class Road:
    first_city: City
    second_city: City

    @property
    def distance(self) -> float:
        earth_radius = 6371
        latitude_degree = degree_to_radius(self.second_city.latitude - self.first_city.latitude) 
        longitude_degree = degree_to_radius(self.second_city.longitude - self.first_city.longitude)
        haversin_expression = sin(latitude_degree/2) * sin(latitude_degree/2) + sin(degree_to_radius(self.first_city.latitude)) * sin(degree_to_radius(self.second_city.latitude)) * cos(longitude_degree) * cos(longitude_degree)
        haversin_distance = 2 *atan2(sqrt(haversin_expression), sqrt(1 - haversin_expression))
        return earth_radius * haversin_distance
