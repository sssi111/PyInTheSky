import time
import threading
import multiprocessing


def fib(n):
    if n <= 1:
        return n
    else:
        return fib(n-1) + fib(n-2)


def main():
    n = 35
    repeats = 10

    start_sync = time.time()
    for _ in range(repeats):
        fib(n)
    sync_time = time.time() - start_sync

    threads = []
    start_thread = time.time()
    for _ in range(repeats):
        t = threading.Thread(target=fib, args=(n,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    thread_time = time.time() - start_thread

    processes = []
    start_process = time.time()
    for _ in range(repeats):
        p = multiprocessing.Process(target=fib, args=(n,))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    process_time = time.time() - start_process

    with open("results.txt", "w") as f:
        f.write(f"Sync: {sync_time:.2f} s\n")
        f.write(f"Threads: {thread_time:.2f} s\n")
        f.write(f"Processes: {process_time:.2f} s\n")


if __name__ == '__main__':
    main()
