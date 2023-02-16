#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This program uses the transaction record and an amount of points to spend. The program will spend the payers points based on these restrictions
    ● the oldest points must be spent first (oldest based on transaction timestamp, not the order they're received)
    ● no payer's points should go negative

@author Owen Strength
"""

import os
import sys
import csv
import json
from collections import namedtuple


def main():

    # command line arguments
    points_to_spend, file_name = sys.argv[1], sys.argv[2]

    try:
        points_to_spend = int(points_to_spend)
    except:
        print(f"Error: The input amount to spend must be of type Integer.",
              file=sys.stderr)
        exit()

    # using a named tuple for easier readability
    # Storing the tuples in transaction data
    transaction = namedtuple("Transaction", ["Payer", "Points", "Timestamp"])
    transaction_data = []

    # using a dict (hashmap) to store all of the final balances for each of the payer
    # using a dict because each payer has a unique name. if the name is the same, the data must correspond to the same payer
    # the dict will look like {"Payer": [points_spent, total_points]}
    final_balances = {}

    # if an invalid/nonexistent file is given return an error
    if not os.path.exists(file_name):
        print(f"Error: File {file_name} does not exist.", file=sys.stderr)
        exit()

    # import csv transaction data into a list of tuples
    with open(file_name, newline="") as csvfile:
        transaction_reader = csv.reader(csvfile, delimiter=",")
        next(transaction_reader)
        for row in transaction_reader:
            transaction_data.append(transaction(row[0], int(row[1]), row[2]))

    # sorting the transaction_data list by the tuples timestamp value with the earliest time being last. Time complexity is O (n log n).
    # this allows to use the transaction_data list as a stack. removing items once we see them is O(1) time complexity.
    # alternatively we could use a pointer to keep track of where we are in the list because we are not adding any new data.
    # I am using a stack because it is more memory efficient and cleaner to read.
    transaction_data.sort(key=lambda x: x[2], reverse=True)

    # if there are any negative point values, we add the inverse of that to the amount of points we need to spend.
    # we are also checking if we have the points available to spend the amount given by the input.
    # this prevents any negative balances.
    largest_possible_balance = 0
    for curr in transaction_data:
        if curr.Points < 0:
            points_to_spend -= curr.Points
        else:
            largest_possible_balance += curr.Points

    if largest_possible_balance < points_to_spend:
        print(f"Error: The input amount to spend cannot be larger than total available balance of {largest_possible_balance} points.",
              file=sys.stderr)
        exit()

    # iterates through every item in the transaction_data stack which is already sorted based on the timestamp.
    # then we check if we have not spent all of our points. If not, we subject a payers points from the points_to_spend variable and
    # add them to our final balance dictionary.If we already have spent enough points than we keep track of the remaining points in
    # the stack and add them to our final balance dictionary.
    # this is the main logic for spending points.
    while transaction_data:

        # removes last item from stack and returns it
        curr = transaction_data.pop()

        # if the amount of points is negative ignore it (we already dealt with it)
        if curr.Points < 0:
            continue

        if points_to_spend > 0:

            # if in our final_balances dictionary we will update it's current values
            if curr.Payer in final_balances:

                # if the transaction objects points are greater than the points we need to spend, only use the amount of points we need
                if (points_to_spend - curr.Points) >= 0:
                    points_to_spend -= curr.Points
                    final_balances[curr.Payer] = [final_balances[curr.Payer][0] +
                                                  curr.Points, final_balances[curr.Payer][1] + curr.Points]
                else:
                    final_balances[curr.Payer] = [final_balances[curr.Payer][0] +
                                                  points_to_spend, final_balances[curr.Payer][1] + curr.Points]
                    points_to_spend = 0

            # if not in our final_balances dictionary we use the current transaction object's data
            else:

                # if the transaction objects points are greater than the points we need to spend, only use the amount of points we need
                if (points_to_spend - curr.Points) >= 0:
                    points_to_spend -= curr.Points
                    final_balances[curr.Payer] = [curr.Points, curr.Points]
                else:
                    final_balances[curr.Payer] = [points_to_spend, curr.Points]
                    points_to_spend = 0

        # if we need to spend more points spend them, else only update the final_balances dictionary
        else:
            if curr.Payer in final_balances:
                final_balances[curr.Payer][1] += curr.Points
            else:
                final_balances[curr.Payer][1] = curr.Points

    # this calculates the final balance by subtracting the total points per payer from the spent points per payer
    for item in final_balances.keys():
        final_balances[item] = final_balances[item][1] - \
            final_balances[item][0]

    # this prints the final data to the terminal as a JSON object, which isn't that useful.
    json_object = json.dumps(final_balances, indent=4)
    print(json_object)

    # this exports our JSON file so we can easily access our data
    with open("output.json", "w") as outfile:
        outfile.write(json_object)

    return json_object


if __name__ == "__main__":
    main()
