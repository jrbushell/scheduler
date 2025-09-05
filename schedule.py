#!/usr/bin/env python3
# https://docs.scipy.org/doc/scipy-0.18.1/reference/generated/scipy.optimize.linear_sum_assignment.html
#
# Maybe also
# https://docs.google.com/spreadsheets/d/0B4IcqARhSzjrUkhRcDVJM2lSaGs/edit?resourcekey=0-snG31ABO-xuU7LWgo1fl8Q&gid=994695874#gid=994695874
#
# CSV values must be in the range 0-10
# - 0 = unavailable
# - 10 = best
# - anything from 1-9 is different levels of "maybe"
# - empty cell is the same as 0

import csv
import sys
import numpy as np
from scipy.optimize import linear_sum_assignment

UNAVAILABLE = 0
BEST_CHOICE = 10

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

spare = len(timeslots) - len(people)
assert spare >= 0, "There are more people than timeslots!"

# Initialise matrix by setting
# - all real timeslots => UNAVAILABLE
# - all dummy timeslots => BEST_CHOICE
constraints = [
    [UNAVAILABLE for _ in range(len(people))] + [BEST_CHOICE for _ in range(spare) ]
    for _ in range(len(timeslots))
]

# Set availability in matrix
for t in range(len(timeslots)):
    for p in range(len(people)):
        if data[t][p]:
            try:
                val = int(data[t][p])
                assert UNAVAILABLE <= val <= BEST_CHOICE
            except (ValueError, AssertionError):
                print(f"ERROR: Data for {people[p]} at {timeslots[t]} is invalid")
                sys.exit(1)
            constraints[t][p] = val

# For solving the matrix, flip the values so that lowest is best
for t in range(len(timeslots)):
    for p in range(len(timeslots)):
        constraints[t][p] = BEST_CHOICE - constraints[t][p]

# Solve the matrix
cost = np.array(constraints)
row_indexes, col_indexes = linear_sum_assignment(cost)

# Print the timetable
for i, col_index in enumerate(col_indexes):
    timeslot = timeslots[i]
    person = people[col_index] if col_index < len(people) else None
    if person:
        bad_choice = constraints[timeslots.index(timeslot)][people.index(person)] != 0
    else:
        bad_choice = False

    print(timeslot, person or "--", "!!" if bad_choice else "")

