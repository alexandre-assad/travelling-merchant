from functools import partial
from os import mkdir
from pathlib import Path

from graph_solver.solve import main as solve_graph
from graph_solver.solvers import christofide_algorithm, genetic_algorithm


def main() -> None:
    input_path = Path("data/france_cities.csv")
    tmp_path = Path("tmp/")
    if not tmp_path.exists():
        mkdir(tmp_path)

    gen_out_path = tmp_path / "gen_out.html"
    gen_algo_with_params = partial(
        genetic_algorithm, generations=1000, number_merchant=100
    )
    solve_graph(input_path, gen_out_path, gen_algo_with_params)

    christofide_path = tmp_path / "chris_out.html"
    solve_graph(input_path, christofide_path, christofide_algorithm)


if __name__ == "__main__":
    main()
