import time
from collections.abc import Callable


def perf_time(fn: Callable[[], None]) -> None:
    st = time.process_time()
    fn()
    et = time.process_time()
    print("CPU Execution time:", et - st, "seconds")
