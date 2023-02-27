from multiprocessing import Process, Value, current_process, Lock
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
import time


def add_one_not_sharing(v: int, process: int):
    process_name = current_process().name
    pid = os.getpid()
    for _ in range(10000):
        v += 1
        print(f"Process:{process}, PID: {pid}, PName: {process_name}, Value = {v}\n", end="")
    print(f"Process:{process}, PID: {pid}, PName: {process_name} Done")


def add_one_sharing(v: Value, process: int, lock):
    process_name = current_process().name
    pid = os.getpid()
    for _ in range(10000):
        lock.acquire()
        v.value += 1
        lock.release()
        print(f"Process:{process}, PID: {pid}, PName: {process_name}, Value = {v.value}\n", end="")
    print(f"Process:{process}, PID: {pid}, PName: {process_name} Done")


def main():
    # Shared X
    # value = 0
    #
    # with ProcessPoolExecutor() as executor:
    #     futures = [executor.submit(add_one_not_sharing(value, i)) for i in range(1,11)]
    #
    #     for future in as_completed(futures):
    #         future.done()
    #
    # print(f"Final Value = {value}")

    # Shared O with Lock
    # value = Value('i', 0)
    #
    # with ProcessPoolExecutor() as executor:
    #     futures = [executor.submit(add_one_sharing(value, i)) for i in range(1,11)]
    #
    #     for future in as_completed(futures):
    #         future.done()

    # Shared O without Lock
    """ As You can see, if there is no lock, the value might be the case as you expected"""
    value = Value('i', 0)

    # If you want to use Lock, Uncomment lock features in the add_one_sharing function
    lock = Lock()

    processes = []
    for i in range(1, 11):
        p = Process(target=add_one_sharing, args=(value, i, lock))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()

    print(f"Final Value = {value.value}")


if __name__ == "__main__":
    main()
