from time import perf_counter
from functools import wraps
from typing import Any
#No stubs
from memory_profiler import memory_usage #type: ignore
from loguru import logger

def profile(func: Any) -> Any:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        mem_before = memory_usage()[0]

        start_time = perf_counter()
        result = func(*args, **kwargs)
        end_time = perf_counter()

        mem_after = memory_usage()[0]

        elapsed_time = end_time - start_time
        mem_used = mem_after - mem_before

        logger.info(f"Execution time: {elapsed_time * 1e6:.2e} µs")
        logger.info(f"Memory used: {mem_used:.2f} MiB\n")

        return result

    return wrapper
