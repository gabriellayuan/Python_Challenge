# import modules
import csv
import os
import sys

# data structures to store information we have read in
rowcount = 0
candidateVotes = {} # for storing unique candidates and their number of votes

# set csv file location and check that it exists
election_data = os.path.join("Resources","election_data.csv")
if(not os.path.exists(election_data)):
    sys.exit("Could not locate resource file: " + election_data)

# open the csv file for reading
with open(election_data) as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')

    # read header row
    csv_header = next(csvreader)

    # for each row: 
    #   Count the number of rows (votes cast)

    for row in csvreader:
        
        # for counting number of rows (votes cast)
        rowcount += 1

        #store the vote for the candidate
        candidate = row[2]
        if candidate in candidateVotes:
            candidateVotes[candidate] += 1
        else:
            candidateVotes[candidate] = 1


# print to stdout then file
output_file = os.path.join("analysis","output.txt")
with open(output_file, 'w') as f:
    for x in range(2):
        print("Election Results")
        print("-------------------------")
        print("Total Votes: " + str(rowcount))
        print("-------------------------")
       
        first = True
        winner = ""
        for k in sorted(candidateVotes.items(), key=lambda x: x[1], reverse=True):
            if(first):
                winner = k[0]
                first = False
            pctwon = k[1] / rowcount * 100
            print(k[0] + ": " + "{:.3f}".format(pctwon) + "% (" + str(k[1]) + ")")

        print("-------------------------")
        print("Winner: " + winner)
        print("-------------------------")

        sys.stdout = f