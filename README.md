# Graph Solver

`Graph Solver` is a Python-based command-line tool designed to solve optimization problems in graph theory, particularly focusing on algorithms like the **Christofides** and **genetic algorithms**. The tool processes city data to determine optimal travel routes.

## Installation

```sh
git clone https://github.com/yourusername/graph-solver.git
cd graph-solver
poetry install
poetry run python main.py
```

## Usage

To use the **Graph Solver**, run the main script from the command line:

```sh
python main.py
```

### Input Data

- The tool expects input data in **CSV format**. The default input file is `data/france_cities.csv`.

### Output

Results will be saved in the `tmp/` directory:
- **Genetic Algorithm Output**: `tmp/gen_out.html`
- **Christofides Algorithm Output**: `tmp/chris_out.html`

## Profiling

The project includes profiling capabilities to monitor execution time and memory usage:

- The `@profile` decorator can be applied to any function to log its performance metrics.

### Example of a Profiled Function

```python
@profile
def christofide_algorithm(cities_data: DataFrame) -> Travel:
    distance_matrix = _compute_distance_matrix(cities_data)
    order = _christofides_tsp(distance_matrix)
    travel = _create_travel_from_indexes(order, cities_data)
    return travel
```

## Strategy Pattern

The project utilizes the **strategy pattern** for solving algorithms, allowing for easy extension and integration of new algorithms:

- **Solver Implementations**: Located in `graph_solver/solvers/`, containing implementations for various algorithms.
