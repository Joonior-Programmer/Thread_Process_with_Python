import os
from multiprocessing import Process, current_process

""" Unlike Multi-Thread in Python (because of GIL), Multi-Process will work in parallel 

    Ex.

    Multi-Thread -> Thread 3 -> Thread 2 -> Thread 5 etc...

    Multi-Processing ->         Process 1 -> Process 3 -> Process 7 etc..
                                Process 2 -> Process 8 -> Other     etc..
                            Other Program -> Process 6 -> Other     etc..
                                Process 9 -> Other     -> Process 11 etc..

            Multi-Processing Output Ex.
    Name: 27, Process ID: 58197, -> Work: 9911
    Name: 24, Process ID: 58194, -> Work: 9580
    Name: 27, Process ID: 58197, -> Work: 9912
    Name: 29, Process ID: 58199, -> Work: 9743
    Name: 27, Process ID: 58197, -> Work: 9913
    Name: 29, Process ID: 58199, -> Work: 9744
    Name: 29, Process ID: 58199, -> Work: 9745
    Name: 24, Process ID: 58194, -> Work: 9581
"""




def process_function():
    for i in range(10000):
        pid = os.getpid()
        p_name = current_process().name
        print(f"Name: {p_name}, Process ID: {pid}, -> Work: {i}")

def main():

    container = []

    for i in range(30):
        process = Process(name=str(i), target=process_function)  # Create a child process
        container.append(process)
        process.start()

    for process in container:
        process.join()

if __name__ == "__main__":
    main()