from enum import Enum, auto
from pathlib import Path
from typing import Callable, TypeAlias

from loguru import logger
from pandas import DataFrame, read_csv

from graph_solver.models.travel import Travel
from graph_solver.save_map import create_map


class SolveType(str, Enum):
    GENETIC = auto()
    CHRISTOFIDES = auto()


class SolverNotImplementedError(NotImplementedError):
    pass


SolveFunc: TypeAlias = Callable[[DataFrame], Travel]


def main(input_path: Path, output_path: Path | None, solver: SolveFunc) -> float:
    cities_data = read_csv(input_path)
    best_travel = solver(cities_data)
    france_map = create_map(best_travel)

    travel_display = "\n".join([f"- {city.name}" for city in best_travel.as_list][:-1])
    if output_path is not None:
        logger.info(f"Best distance found: {best_travel.total_distance:.2f}")
        logger.info(f"Best Travel:\n{travel_display}")
        france_map.save(output_path)
        logger.info(f"Successfully saved map to {output_path}")
    return best_travel.total_distance
