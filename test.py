#!/usr/bin/env python3
# https://docs.scipy.org/doc/scipy-0.18.1/reference/generated/scipy.optimize.linear_sum_assignment.html
#
# Maybe also
# https://docs.google.com/spreadsheets/d/0B4IcqARhSzjrUkhRcDVJM2lSaGs/edit?resourcekey=0-snG31ABO-xuU7LWgo1fl8Q&gid=994695874#gid=994695874

import csv
import sys
import numpy as np
from scipy.optimize import linear_sum_assignment

people = []
timeslots = []
data = []

with open(sys.argv[1]) as csvfile:
    for row in csv.reader(csvfile):
        if not people:
            people = row[1:]
        else:
            timeslots.append(row[0])
            data.append(row[1:])

# print(timeslots)
# print(people)

spare = len(timeslots) - len(people)
assert spare >= 0

# 0 = available
# 1 = unavailable
constraints = [
    [1 for _ in range(len(people))] + [0 for _ in range(spare) ]
    for _ in range(len(timeslots))
]

# print(constraints)

for t in range(len(timeslots)):
    for p in range(len(people)):
        if bool(data[t][p]):
            constraints[t][p] = 0

# print(constraints)

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

# for i in range(len(row_indexes)):
#     print(row_indexes[i], col_indexes[i])
#
for i, col_index in enumerate(col_indexes):
    timeslot = timeslots[i]
    person = people[col_index] if col_index < len(people) else None
    if person:
        bad_choice = constraints[timeslots.index(timeslot)][people.index(person)] != 0
    else:
        bad_choice = False

    print(timeslot, person or "--", "!!" if bad_choice else "")

