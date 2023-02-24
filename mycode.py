import csv
from collections import defaultdict
import sys

def parse_csv(csv_file):
    transactions = [] # stores all the transactions
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            transactions.append({"payer" : row["payer"],
                               "points": int(row["points"]),
                               "timestamp" : row["timestamp"]}) # adds all necessary information to list as a set
    transactions.sort(key=lambda x: x['timestamp']) # sorts by timestamp so it is formatted properly
    return transactions
            
def spend(points_to_spend, transactions):
    balances = defaultdict(int)
    remaining_points = points_to_spend
    i = 0;
    while i < len(transactions):
        payer = transactions[i]["payer"] # grabs current payer
        points = transactions[i]["points"] # grabs current points
        balances[payer] # sets up dictionary associated with payer
        
        remaining_points -= points # subtract current points from remaining_points
        
        if remaining_points < 0: # if remaining points is less than 0, want to start adding up remaining balances for payers
            balances[payer] -= remaining_points # since remaining points is negative, this will "add"
            i += 1
            while i < len(transactions):
                payer = transactions[i]["payer"]
                points = transactions[i]["points"]
                balances[payer] += points # adding up remaining balances
                i += 1;
            for key in balances:
                if balances[key] < 0:
                    balances[key] = 0 # we do not want payer's points to go negative
            break
            
        i += 1
    
    return dict(balances)



points = sys.argv[1] # takes in system args
file = str(sys.argv[2])

parsed_csv = parse_csv(file)
balances = spend(int(points), parsed_csv)
print(balances)