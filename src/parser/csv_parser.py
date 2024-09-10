from pathlib import Path
from typing import List

from pandas import read_csv

from src.domain.dataclass.city import City

def parse_csv_to_list_city(file_path: str) -> List[City]:
    cities = []
    dataframe = read_csv(file_path)
    for _, row in dataframe.iterrows():
        cities.append(City(name=row["Ville"], longitude=row['Longitude'], latitude=row['Latitude']))
    return cities