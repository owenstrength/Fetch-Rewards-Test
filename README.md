# Fetch Rewards Test
### Problem Statement:

Our users have points in their accounts. Users only see a single balance in their account. But for reporting purposes, we actually track their points per payer. In our system, each transaction record contains: **payer** (string), **points** (integer), **timestamp** (date). For earning points, it is easy to assign a payer. We know which actions earned the points. And thus, which partner should be paying for the points. When a user spends points, they don't know or care which payer the points come from. But, our accounting team does care how the points are spent. 

**There are two rules for determining what points to "spend" first:**
	 
1. We want the oldest points to be spent first (oldest based on transaction timestamp, not the order they’re received) 
2. We want no payer's points to go negative
	 

**We expect your code to** 
1. Read the transactions from a CSV file. 
2. Spend points based on the argument using the rules above. 
3. Return all payer point balances.

## Running My Code

My solution is written in Python 3.10. This does not come pre-installed on your local machine. You can download Python and follow the instructions [here](https://www.python.org/downloads/)

Once Python is installed, open this directory on your machine and run main.py and pass 2 arguments. The first being the number of points you would like to spend, and the second being the name of the input file.

The first argument must be an **integer**. 
The second argument must be a **string** of a file that exists.

For example, to spend 5000 points, it would look like this: 

    python3 main.py 5000 transactions.csv

**The program will throw errors** 
 1. If the file name is invalid or does not exist.
 2. If the requested amount of points to spend is more than the points available. 
 3. If the points to spend is not an integer.

## Assignment #2

Assignment #2 is located in `summary.txt`
