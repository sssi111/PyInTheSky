import os
import math
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def compute_chunk(f, a, step, start, end):
    return sum(f(a + i * step) * step for i in range(start, end))

def task_wrapper(args):
    return compute_chunk(*args)

def integrate(f, a, b, *, n_jobs=1, n_iter=10000000, executor_class=ThreadPoolExecutor):
    step = (b - a) / n_iter
    chunk_size = n_iter // n_jobs
    
    tasks = []
    for i in range(n_jobs):
        start = i * chunk_size
        end = start + chunk_size
        if i == n_jobs - 1:
            end = n_iter
        tasks.append((f, a, step, start, end))
    
    with executor_class(max_workers=n_jobs) as executor:
        results = executor.map(task_wrapper, tasks)
        return sum(results)

def benchmark():
    cpu_count = os.cpu_count()
    max_jobs = cpu_count * 2
    header = "Executor,Workers,Time"
    
    with open("results.csv", "w") as f:
        f.write(f"{header}\n")
        
        for executor in [ThreadPoolExecutor, ProcessPoolExecutor]:
            for n_jobs in range(1, max_jobs + 1):
                start = time.perf_counter()
                integrate(math.cos, 0, math.pi/2, 
                         n_jobs=n_jobs,
                         n_iter=10_000_000,
                         executor_class=executor)
                duration = time.perf_counter() - start
                
                line = f"{executor.__name__},{n_jobs},{duration:.4f}"
                f.write(f"{line}\n")
                print(line)

if __name__ == "__main__":
    benchmark()
