import aiohttp
import asyncio
from time import time, sleep
import ssl
import certifi


""" Compare with the file named '7_process_pool_executor.py' and
                                '2_thread_with_thread_pool_executor'  """


async def visit_web_page(url: str, session: aiohttp.ClientSession, ssl):
    try:
        async with session.get(url, ssl=ssl) as response:
            print(f"{response.content} : {url}")
    except Exception as e:
        print(e)


async def visit_web_pages(urls: list[str]):
    start = time()
    context = ssl.create_default_context(cafile=certifi.where())
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.ensure_future(visit_web_page(url, session, context))
            tasks.append(task)

        await asyncio.gather(*tasks, return_exceptions=True)
    print(f"{time() - start} Seconds to visit {len(urls)} websites")


def main():
    urls = ["http://bcit.ca", "http://www.ubc.ca/", "http://www.sfu.ca/", "http://www.stanford.edu/",
            "http://naver.com", "http://daum.net", "http://notion.so", "https://www.kakaocorp.com/page/"] * 3

    asyncio.run(visit_web_pages(urls))


if __name__ == "__main__":
    main()
