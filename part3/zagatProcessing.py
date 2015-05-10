import csv
import os
import argparse
from tokenizer import tokenizer



if __name__ == '__main__':
    states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
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
        if args.output == 'Yelp':
            [sentiment,city,state] = row
            if state not in states:
                continue
        elif args.output == 'Zagat':
            [sentiment,state,city] = row
        city = ' '.join(tokenizer(city))
        city = city+':'+state
        sentiment = float(sentiment)
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
