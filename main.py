from functools import partial
from os import mkdir, system
from pathlib import Path

from matplotlib.colors import Normalize
import matplotlib.pyplot as plt
import seaborn as sns  # type: ignore
from pandas import DataFrame, read_csv

from graph_solver.solve import main as solve_graph
from graph_solver.solvers import christofide_algorithm, genetic_algorithm



def run_gen_algo_batch(save_path: Path) -> None:
    input_path = Path("data/france_cities.csv")
    tmp_path = Path("tmp/")
    if not tmp_path.exists():
        mkdir(tmp_path)

    generations_range = range(10, 1001, 10)
    merchants_range = [5, 10, 25, 50, 75, 100]
    results = []

    for merchants in merchants_range:
        for generations in generations_range:
            gen_algo_with_params = partial(
                genetic_algorithm, generations=generations, number_merchant=merchants
            )
            distance = solve_graph(input_path, None, gen_algo_with_params)
            results.append(
                {
                    "generations": generations,
                    "merchants": merchants,
                    "distance": distance,
                }
            )

    res = DataFrame(results)
    res.to_csv(save_path, index=False)

def generate_plot_from_df(results: DataFrame) -> None:
    plt.figure(figsize=(12, 6))

    sns.scatterplot(
            data=results,
            x="generations",
            y="merchants",
            size="distance",
            hue="distance",
            sizes=(20, 400),
            palette="coolwarm",
            alpha=0.6,
            legend=False,
        )

    ax = plt.gca()

    norm = Normalize(results['distance'].min(), results['distance'].max())
    sm = plt.cm.ScalarMappable(cmap="coolwarm", norm=norm)
    sm.set_array([])

    plt.colorbar(sm, ax=ax)

    plt.title("Distance by Generations and Number of Merchants")
    plt.xlabel("Generations")
    plt.ylabel("Number of Merchants")
    plt.xscale("log")
    plt.yscale("linear")
    plt.grid()
    tmp_path = Path("tmp/")
    output_path = tmp_path / "distance_vs_generations_merchants_colored.png"
    plt.savefig(output_path)
    plt.close()

def save_algo_gen() -> None:
    tmp_path = Path("tmp/")
    if not tmp_path.exists():
        mkdir(tmp_path)
    res_path = tmp_path / "results.csv"
    # run_gen_algo_batch(res_path)
    results = read_csv(res_path, index_col=None)
    generate_plot_from_df(results)


def run_gen_algo() -> None:
    input_path = Path("data/france_cities.csv")
    tmp_path = Path("tmp/")
    html_output_path = tmp_path / "gen_algo.html"
    if not tmp_path.exists():
        mkdir(tmp_path)
    algo_gen = partial(genetic_algorithm, generations = 500, number_merchant=5)
    solve_graph(input_path, html_output_path, algo_gen)
    system(f"chromium {html_output_path}")


def run_christofide() -> None:
    input_path = Path("data/france_cities.csv")
    tmp_path = Path("tmp/")
    if not tmp_path.exists():
        mkdir(tmp_path)
    christofide_path = tmp_path / "chris_out.html"
    solve_graph(input_path, christofide_path, christofide_algorithm)
    system(f"chromium {christofide_path}")


if __name__ == "__main__":
    # save_algo_gen()
    # run_christofide()
    run_gen_algo()