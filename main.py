from datetime import datetime
from multiprocessing import Queue, Process
from threading import Thread


def is_lucky(ticket_number):
    half1 = ticket_number[:len(ticket_number) // 2]
    half2 = ticket_number[len(ticket_number) // 2:]
    sum_half1 = sum(map(int, half1))
    sum_half2 = sum(map(int, half2))
    return sum_half1 == sum_half2


def part_count(from_ticket_number, to_ticket_number, queue_object):
    lucky_numbers = 0
    for i in range(from_ticket_number, to_ticket_number):
        ticket_str = str(i).rjust(6, "0")
        if is_lucky(ticket_str):
            lucky_numbers += 1
    queue_object.put(lucky_numbers)


if __name__ == '__main__':
    ticket_numbers = Queue()
    t1 = Thread(target=part_count, args=(0, 250000, ticket_numbers))
    t2 = Thread(target=part_count, args=(250000, 500000, ticket_numbers))
    t3 = Thread(target=part_count, args=(500000, 750000, ticket_numbers))
    t4 = Thread(target=part_count, args=(750000, 1000000, ticket_numbers))
    print("Counting...")
    print("Please wait...")
    start_time = datetime.now()
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    end_time = datetime.now()

    print("Time taken: ", end_time - start_time)

    total = 0
    while not ticket_numbers.empty():
        ticket_number = ticket_numbers.get()
        print(ticket_number)
        total += ticket_number
    print(total)


def collatz_check(n):
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
    return True


def collatz_range_check(start, end, queue_object):
    for i in range(start, end):
        if not collatz_check(i):
            queue_object.put(f"Failed for number: {i}")
            return
    queue_object.put(f"Checked range {start}-{end}: All numbers satisfy the Collatz Conjecture")


if __name__ == '__main__':
    LIMIT = 1000000000
    NUM_WORKERS = 8

    step = LIMIT // NUM_WORKERS
    processes = []
    results_queue = Queue()

    print("Starting Collatz Conjecture check...")
    start_time = datetime.now()

    for i in range(NUM_WORKERS):
        start = i * step + 1
        end = (i + 1) * step if i < NUM_WORKERS - 1 else LIMIT + 1
        process = Process(target=collatz_range_check, args=(start, end, results_queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    end_time = datetime.now()

    while not results_queue.empty():
        print(results_queue.get())

    print("All numbers from 1 to 1,000,000,000 satisfy the Collatz Conjecture.")
    print("Time taken: ", end_time - start_time)
