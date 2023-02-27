from concurrent.futures import ProcessPoolExecutor, as_completed
import urllib.request
import certifi
import os
from multiprocessing import current_process


def visit(url, timeout):
    with urllib.request.urlopen(url=url, timeout=timeout, cafile=certifi.where()) as conn:
        return conn.read()


def count(process):
    process_name = current_process().name
    pid = os.getpid()
    for i in range(10000):
        print(f"Process:{process} Process Name:{process_name} PID:{pid}, work = {i}\n")
    return process


def main():
    # Visit url lists
    urls = ["http://naver.com",
            "http://daum.net",
            "https://bcit.ca",
            "https://tunib.ai/",
            "http://not.exist",
            "http://apple.com",
            "http://notion.so",
            "http://zoom.us"
            ]

    # You can specify max_worker for ProcessPoolExecutor()
    with ProcessPoolExecutor() as executor:
        # Example 1
        # Key = Future, Value = URL
        # future_to_url = {executor.submit(visit, url, 5): url for url in urls}
        #
        # print(future_to_url)
        #
        # for future in as_completed(future_to_url):
        #     url = future_to_url[future]
        #
        #     try:
        #         print(f"{url} : {len(future.result())} Bytes")
        #     except:
        #         print(f"{url} is not available to open")

        # Example 2
        futures = [executor.submit(count, i) for i in range(1,15)]

        for future in as_completed(futures):
            print(f"{future.result()} done")


if __name__ == "__main__":
    main()