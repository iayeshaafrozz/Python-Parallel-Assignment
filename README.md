# Multithreaded Student Result Processing System

A Python parallel programming assignment that uses **multithreading** to process student results.

## Description

This application simulates a result processing system. A **Teacher** thread (producer) submits student marks into a shared queue, and multiple **Grader** threads (consumers) pick students from the queue and calculate their total marks, percentage and grade at the same time.

## Technique Used (Chapter 2: Thread-Based Parallelism)

The code is based on the **producer-consumer with `queue.Queue`** example from *Python Parallel Programming Cookbook, Second Edition* (Packt), Chapter 2 (`Threading_with_queue.py`).

Concepts used:

- `threading.Thread` subclasses (`Teacher`, `Grader`)
- `queue.Queue` for thread-safe communication between threads
- `threading.Lock` to safely update the shared results list
- `None` as a stop signal so the consumer threads exit cleanly (the original example runs forever)

## What I Changed

| Original example | My application |
|---|---|
| Random numbers as data | Student names and subject marks |
| 1 producer, 3 consumers printing items | 1 Teacher, 3 Graders calculating grades |
| Consumers run forever | Consumers stop using a `None` signal |
| No shared results | Results collected with a `Lock` and shown in a table |

## Grading Scale

| Percentage | Grade |
|---|---|
| 85 and above | A |
| 70 to 84 | B |
| 55 to 69 | C |
| 40 to 54 | D |
| Below 40 | F |

## How to Run

Requirements: Python 3 (no extra libraries needed).

```bash
git clone https://github.com/iayeshaafrozz/Python-Parallel-Assignment.git
cd Python-Parallel-Assignment
python3 student_result_app.py
```

## Sample Output

```
Roll  Name            Total   Percent    Grade
1     Ali Khan        396     79.20      B
2     Sara Ahmed      455     91.00      A
3     Hamza Malik     293     58.60      C
4     Fatima Noor     408     81.60      B
5     Usman Raza      209     41.80      D
6     Zainab Iqbal    355     71.00      B
7     Bilal Shah      481     96.20      A
8     Hira Tariq      307     61.40      C

Processed 8 students using 3 grader threads in 2.61 seconds
```

## Author

Ayesha Afroz, UIT University
