
from dataclasses import dataclass

@dataclass
class City:
    name: str
    longitude: float
    latitude: float 


    def __eq__(self, value: object) -> bool:
        return self.name == value