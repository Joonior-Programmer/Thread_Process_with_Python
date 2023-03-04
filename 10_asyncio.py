import asyncio
from time import time, sleep


""" NOTE: Tested with Python 3.11 """

async def async_count_example(n: int, job: str):
    for i in range(1, n + 1):
        print(f"{job}: {i}")
        await asyncio.sleep(0.5)


async def run_async_count_example():
    start = time()
    job1 = asyncio.create_task(async_count_example(3, "First"))
    job2 = asyncio.create_task(async_count_example(2, "Second"))
    job3 = asyncio.create_task(async_count_example(1, "Third"))
    await asyncio.wait({job1, job2, job3})
    print(f"AsyncIO spent {time() - start} Seconds")


def sync_count_example(n: int, job: str):
    for i in range(1, n + 1):
        print(f"{job}: {i}")
        sleep(0.5)


def run_sync_count_example():
    start = time()
    sync_count_example(3, "First")
    sync_count_example(2, "Second")
    sync_count_example(1, "Third")
    print(f"Sync spent {time() - start} Seconds")


def main():
    run_sync_count_example()
    asyncio.run(run_async_count_example())


if __name__ == "__main__":
    main()
