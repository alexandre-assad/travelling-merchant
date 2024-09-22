from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class City:
    name: str
    longitude: float
    latitude: float

    def __eq__(self, value: object) -> bool:
        return self.name == value
