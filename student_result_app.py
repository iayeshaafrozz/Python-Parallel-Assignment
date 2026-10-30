"""Multithreaded Student Result Processing System
Technique used (Chapter 2): producer-consumer with queue.Queue and threads.
A Teacher thread (producer) puts student marks into a queue, and several
Grader threads (consumers) calculate totals, percentages and grades in parallel.
"""

from threading import Thread, Lock
from queue import Queue
import time

NUM_GRADERS = 3

STUDENTS = [
    ("Ali Khan", [78, 85, 69, 90, 74]),
    ("Sara Ahmed", [92, 88, 95, 91, 89]),
    ("Hamza Malik", [55, 62, 48, 70, 58]),
    ("Fatima Noor", [81, 76, 84, 79, 88]),
    ("Usman Raza", [40, 35, 52, 44, 38]),
    ("Zainab Iqbal", [67, 72, 65, 80, 71]),
    ("Bilal Shah", [95, 98, 92, 97, 99]),
    ("Hira Tariq", [59, 64, 61, 57, 66]),
]


def get_grade(percentage):
    if percentage >= 85:
        return "A"
    if percentage >= 70:
        return "B"
    if percentage >= 55:
        return "C"
    if percentage >= 40:
        return "D"
    return "F"


class Teacher(Thread):
    """Producer: submits student marks to the queue."""

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        for roll_no, (name, marks) in enumerate(STUDENTS, start=1):
            self.queue.put((roll_no, name, marks))
            print("[Teacher] Submitted marks of %s" % name)
            time.sleep(0.3)
        # one stop signal for each grader
        for _ in range(NUM_GRADERS):
            self.queue.put(None)


class Grader(Thread):
    """Consumer: calculates result of each student."""

    def __init__(self, queue, results, lock):
        Thread.__init__(self)
        self.queue = queue
        self.results = results
        self.lock = lock

    def run(self):
        while True:
            task = self.queue.get()
            if task is None:
                self.queue.task_done()
                break
            roll_no, name, marks = task
            time.sleep(0.5)  # simulate processing time
            total = sum(marks)
            percentage = total / len(marks)
            grade = get_grade(percentage)
            with self.lock:
                self.results.append((roll_no, name, total, percentage, grade))
            print("    [%s] Processed %s -> Grade %s" % (self.name, name, grade))
            self.queue.task_done()


if __name__ == "__main__":
    queue = Queue()
    results = []
    lock = Lock()

    start = time.time()

    teacher = Teacher(queue)
    graders = [Grader(queue, results, lock) for _ in range(NUM_GRADERS)]

    teacher.start()
    for g in graders:
        g.start()

    teacher.join()
    for g in graders:
        g.join()

    elapsed = time.time() - start

    print("\n" + "=" * 58)
    print("%-5s %-15s %-7s %-10s %-5s" % ("Roll", "Name", "Total", "Percent", "Grade"))
    print("=" * 58)
    for roll_no, name, total, pct, grade in sorted(results):
        print("%-5d %-15s %-7d %-10.2f %-5s" % (roll_no, name, total, pct, grade))
    print("=" * 58)
    print("Processed %d students using %d grader threads in %.2f seconds"
          % (len(results), NUM_GRADERS, elapsed))
