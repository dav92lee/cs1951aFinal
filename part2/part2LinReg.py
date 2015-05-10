from scipy.optimize import curve_fit
import numpy as np
import csv
import matplotlib.pyplot as plt

def curve(x,a,b,c):
    return a*np.exp(-b*x)+c

class Review:
    def __init__(self,row):
        self.sentiment = float(row[0])
        self.funny = int(row[1])
        self.useful = int(row[2])
        self.cool = int(row[3])
        self.funny_norm = float(row[4])
        self.useful_norm = float(row[5])
        self.cool_norm = float(row[6])
        self.stars = int(row[7])
        
if __name__ == '__main__':
    reviews = list()
    print('Importing Data')
    with open('out.csv') as csvfile:
        reader = csv.reader(csvfile,delimiter=',')
        for row in reader:
            reviews.append(Review(row))
    print('Extracting X and Y')
    numReviews = len(reviews)
    tenth = numReviews/1000
    dataShell=list()
    for i in xrange(0,numReviews,tenth):
        dataShell.append(max(reviews[i:i+tenth],key=lambda a: a.funny))

    funnyX=map(lambda a: a.sentiment,dataShell)
    funnyY=map(lambda a: a.funny,dataShell)

    print('Fitting Curve')
    opt,var = curve_fit(curve,np.array(funnyX),np.array(funnyY))

    print('Making Graph')
    plt.scatter(funnyX,funnyY,color='blue')
    plt.plot(funnyX,map(lambda a: curve(a,opt[0],opt[1],opt[2]),funnyX), color='black')

    plt.xlim((-1,1))
    
    plt.show()
    
