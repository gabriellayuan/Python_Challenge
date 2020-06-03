# import modules
import csv
import os
import sys

# data structures to store information we have read in
months = set() # count months (remove assumption of 1 month per role)
greatestincreasemonths = set() # store the greatest increase months in case multiple 
greatestdecreasemonths = set() # store the greatest decrease months in case multiple 
rowcount = 0
totalbalance = 0
totalchange = 0
prevrow = 0
greatestincrease = 0
greatestdecrease = 0

# set csv file location and check that it exists
budget_data = os.path.join("Resources","budget_data.csv")
if(not os.path.exists(budget_data)):
    sys.exit("Could not locate resource file: " + budget_data)

# open the csv file for reading
with open(budget_data) as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')

    # read header row
    csv_header = next(csvreader)

    # for each row: 
    #   Count the number of rows/months
    #   Add value to the running total
    #   Calculate the change from prior row and use this to set new maximums, as well as keep running total for calculating average
    for row in csvreader:
        
        # for counting number of entries/rows (used for generating average)
        rowcount += 1
        
        # for counting number of unique months (assuming it might not always be the number of rows)
        month = row[0]
        months.add(month)

        # for determinig the value
        pnl = int(row[1])
        totalbalance = totalbalance + pnl

        # determine the largest increase, largest decrease and average change
        if (rowcount > 1):
            change = (pnl - prevrow)
            totalchange += change
            if(rowcount == 2): #the first greatest increase/decrease is the max
                greatestdecrease = pnl
                greatestincrease = pnl
                greatestincreasemonths.add(month)
                greatestdecreasemonths.add(month)
            else: # future increases/decreases will be determined by comparing with current max increase/decrease
                if (change > greatestincrease): # handle a new greatest increase
                    greatestincrease = change
                    greatestincreasemonths.clear()
                    greatestincreasemonths.add(month)
                elif (change < greatestdecrease): # handle a new greatest decrease
                    greatestdecrease = change
                    greatestdecreasemonths.clear()
                    greatestdecreasemonths.add(month)
                else: #handle where more than one month has same increase/decrease as current greatest
                    if (greatestincrease == change):
                        greatestincreasemonths.add(month)
                        print ("Adding month: " + month + "\tvalue: " + change)
                    elif (greatestdecrease == change):
                        greatestdecreasemonths.add(month)

        prevrow = pnl #now set previous row to be current row

    averagechange = totalchange / (rowcount - 1)

    # print to stdout then file
    output_file = os.path.join("analysis","output.txt")
    with open(output_file, 'w') as f:
        for x in range(2):
            print("Financial Analysis")
            print("----------------------------")
            print("Total Months: " + str(len(months)))
            print("Total: $" +  str(totalbalance))
            print("Average Change: $" + "{:.2f}".format(averagechange))
            print("Greatest Increase in Profits: " + ",".join([str(s) for s in greatestincreasemonths]) + " ($" + str(greatestincrease) + ")")
            print("Greatest Decrease in Profits: " + ",".join([str(s) for s in greatestdecreasemonths]) + " ($" + str(greatestdecrease) + ")")
            sys.stdout = f

