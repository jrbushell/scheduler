#!/usr/bin/env python3
# https://docs.scipy.org/doc/scipy-0.18.1/reference/generated/scipy.optimize.linear_sum_assignment.html
#
# Maybe also
# https://docs.google.com/spreadsheets/d/0B4IcqARhSzjrUkhRcDVJM2lSaGs/edit?resourcekey=0-snG31ABO-xuU7LWgo1fl8Q&gid=994695874#gid=994695874

import numpy as np
from scipy.optimize import linear_sum_assignment

timeslots = [
    "0900",
    "1000",
    "1100",
    "1200",
    "1300",
    "1400"
]

people = [
    "alice",
    "bob",
    "chas",
    "dave"
]

spare = len(timeslots) - len(people)
assert spare >= 0

# 0 = available
# 1 = unavailable
constraints = [ [1 for _ in range(len(people))] + [0 for _ in range(spare) ] for _ in range(len(timeslots)) ]

print(constraints)

def set_available(person, timeslot):
    constraints[timeslots.index(timeslot)][people.index(person)] = 0

set_available("alice", "1200")
set_available("bob",   "0900")
set_available("bob",   "1100")
set_available("bob",   "1300")
set_available("chas",  "1000")
set_available("chas",  "1300")
set_available("chas",  "1400")
set_available("dave",  "0900")
set_available("dave",  "1200")

print(constraints)

# assert constraints == [
#     [1,0,1,0,0,0],
#     [1,1,0,1,0,0],
#     [1,0,1,1,0,0],
#     [0,1,1,0,0,0],
#     [1,0,0,1,0,0],
#     [1,1,0,1,0,0]
# ]

cost = np.array(constraints)
row_indexes, col_indexes = linear_sum_assignment(cost)

for i in range(len(row_indexes)):
    print(row_indexes[i], col_indexes[i])

for i, col_index in enumerate(col_indexes):
    print(timeslots[i], people[col_index] if col_index < len(people) else "spare")

