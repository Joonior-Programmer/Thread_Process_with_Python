from concurrent.futures import ProcessPoolExecutor, as_completed
import urllib.request
import certifi


def visit(url, timeout):
    with urllib.request.urlopen(url=url, timeout=timeout, cafile=certifi.where()) as conn:
        return conn.read()


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
        # Key = Future, Value = URL
        future_to_url = {executor.submit(visit, url, 5): url for url in urls}

        print(future_to_url)

        for future in as_completed(future_to_url):
            url = future_to_url[future]

            try:
                print(f"{url} : {len(future.result())} Bytes")
            except:
                print(f"{url} is not available to open")


if __name__ == "__main__":
    main()