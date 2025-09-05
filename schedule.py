#!/usr/bin/env python3
# https://docs.scipy.org/doc/scipy-0.18.1/reference/generated/scipy.optimize.linear_sum_assignment.html
#
# CSV values must be in the range 0-10
# - 0 = unavailable
# - 10 = best
# - empty cell is the same as 0

import csv
import sys
import numpy as np
from scipy.optimize import linear_sum_assignment

UNAVAILABLE = 0
BEST_CHOICE = 10

people = []
timeslots = []
constraints = []

with open(sys.argv[1]) as csvfile:
    for row in csv.reader(csvfile):
        if not people:
            people = row[1:]
        else:
            timeslots.append(row[0])
            constraints.append(row[1:])

spare = len(timeslots) - len(people)
assert spare >= 0, "There are more people than timeslots!"

for t in range(len(timeslots)):
    # Validate data
    for p in range(len(people)):
        if constraints[t][p]:
            try:
                constraints[t][p] = int(constraints[t][p])
                assert UNAVAILABLE <= constraints[t][p] <= BEST_CHOICE
            except (ValueError, AssertionError):
                print(f"ERROR: Data for {people[p]} at {timeslots[t]} is invalid")
                sys.exit(1)
        else:
            constraints[t][p] = UNAVAILABLE

    # Add padding
    constraints[t] += [BEST_CHOICE for _ in range(spare)]

# Solve the matrix
cost = np.array(constraints)
row_indexes, col_indexes = linear_sum_assignment(cost, maximize=True)

# Print the timetable
for i, col_index in enumerate(col_indexes):
    timeslot = timeslots[i]
    person = people[col_index] if col_index < len(people) else None

    if person:
        value = constraints[timeslots.index(timeslot)][people.index(person)]
        non_optimal = value < BEST_CHOICE
    else:
        value = None
        non_optimal = False

    print(timeslot, person or "--", f"-- non-optimal choice [{value}/{BEST_CHOICE}]" if non_optimal else "")

