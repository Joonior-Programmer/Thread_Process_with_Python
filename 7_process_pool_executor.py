from concurrent.futures import ProcessPoolExecutor, as_completed
import urllib.request
import certifi
import os
from multiprocessing import current_process, Process
from time import time


def visit(url, timeout):
    with urllib.request.urlopen(url=url, timeout=timeout, cafile=certifi.where()) as conn:
        print(f"{url}: {len(conn.read())}Bytes")


def count(process):
    process_name = current_process().name
    pid = os.getpid()
    for i in range(10000):
        print(f"Process:{process} Process Name:{process_name} PID:{pid}, work = {i}\n", end="")
    return process


def main():
    # Visit url lists
    urls = ["http://bcit.ca", "http://www.ubc.ca/", "http://www.sfu.ca/", "http://www.stanford.edu/",
            "http://naver.com", "http://daum.net", "http://notion.so", "https://www.kakaocorp.com/page/"] * 3

    # You can specify max_worker for ProcessPoolExecutor()

    with ProcessPoolExecutor(max_workers=20) as executor:
        # Example 1
        # Key = Future, Value = URL

        start = time()
        future_to_url = {executor.submit(visit, url, 5): url for url in urls}

        # print(future_to_url)

        for future in as_completed(future_to_url):
            future.done()

        print(f"{time() - start} seconds to visit {len(urls)} websites")



        # Example 2
        # futures = [executor.submit(count, i) for i in range(1, 15)]
        #
        # for future in as_completed(futures):
        #     print(f"{future.result()} done")

    # Visit Website without pool executor
    # start = time()
    # tasks = []
    # for url in urls:
    #     p = Process(target=visit, args=(url, 5))
    #     p.start()
    #     tasks.append(p)
    #
    # for task in tasks:
    #     task.join()
    #
    # print(f"{time() - start} seconds to visit {len(urls)} websites")

if __name__ == "__main__":
    main()
