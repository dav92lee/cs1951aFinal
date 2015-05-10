import csv
import os
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-input',help='Path to csv')
    parser.add_argument('-output',help='Output file suffix')
    args = parser.parse_args()
    csvInput = open(args.input,'r')
    cityOutput = open('cities'+args.output+'.csv','w')
    stateOutput = open('states'+args.output+'.csv','w')
    inputcsv = csv.reader(csvInput)
    citycsv = csv.writer(cityOutput)
    statecsv = csv.writer(stateOutput)
    cityDict = dict()
    stateDict = dict()
    for row in inputcsv:
        [sentiment,state,city] = row
        sentiment = float(sentiment)
        city = city+':'+state
        if city in cityDict:
            crrnt = cityDict[city]
            cityDict[city] = [crrnt[0]+sentiment,crrnt[1]+1]
        else:
            cityDict[city] = [sentiment,1]
        if state in stateDict:
            crrnt = stateDict[state]
            stateDict[state] = [crrnt[0]+sentiment,crrnt[1]+1.0]
        else:
            stateDict[state] = [sentiment,1.0]
    for k in cityDict:
        v = cityDict[k]
        citycsv.writerow([v[0]/v[1],k])
    for k in stateDict:
        v = stateDict[k]
        statecsv.writerow([v[0]/v[1],k])
