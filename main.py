

from pathlib import Path
from src.solver.algorythm_christofide import algorythm_output
from src.solver.genetic_algorythm import genetic_algorithm


def main() -> None:
    algorythm_output("data/input/france_cities.csv", "data/output/map_travel_christofide.html")
    genetic_algorithm("data/input/france_cities.csv", "data/output/map_travel_genetic.html")

if __name__ == '__main__':
    main()