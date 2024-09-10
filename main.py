

from pathlib import Path
from src.solver.genetic_algorythm import genetic_algorithm


def main() -> None:
    genetic_algorithm("data/france_cities.csv")

if __name__ == '__main__':
    main()