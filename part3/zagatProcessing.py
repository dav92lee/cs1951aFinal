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
    cityMeanDict = dict()
    stateMeanDict = dict()
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
        mean = v[0]/v[1]
        # citycsv.writerow([mean,k])
        cityMeanDict[k] = mean
    for k in stateDict:
        v = stateDict[k]
        mean = v[0]/v[1]
        # statecsv.writerow([mean,k])
        stateMeanDict[k] = mean



    #go back to top for variance
    csvInput.seek(0)
    for row in inputcsv:
        [sentiment,city,state] = row
        sentiment = float(sentiment)
        if state not in states:
            continue
        city = city+':'+state
        if city in cityDict:
            crrnt = cityDict[city]
            sentiment_diff = ((sentiment - float(cityMeanDict[city])))**2
            cityDict[city] = [crrnt[0]+sentiment_diff,crrnt[1]+1]
        else:
            sentiment_diff = ((sentiment - float(cityMeanDict[city])))**2
            cityDict[city] = [sentiment_diff,1]
        if state in stateDict:
            crrnt = stateDict[state]
            sentiment_diff = ((sentiment - float(stateMeanDict[state])))**2
            stateDict[state] = [crrnt[0]+sentiment_diff,crrnt[1]+1.0]
        else:
            sentiment_diff = ((sentiment - float(stateMeanDict[state])))**2
            stateDict[state] = [sentiment_diff,1.0]
    for k in cityDict:
        v = cityDict[k]
        mean = cityMeanDict[k]
        var = v[0]/v[1]
        citycsv.writerow([mean,var,k])
    for k in stateDict:
        v = stateDict[k]
        mean = stateMeanDict[k]
        var = v[0]/v[1]
        statecsv.writerow([mean,var,k])

