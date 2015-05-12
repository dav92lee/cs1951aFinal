from sklearn import linear_model
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
    
    funnyX=map(lambda a: [a.sentiment],reviews)
    funnyY=map(lambda a: a.cool,reviews)

    reg=linear_model.LinearRegression()

    reg.fit(funnyX,funnyY)
    
    print('Making Graph')
    plt.scatter(map(lambda a: a[0],funnyX),funnyY,color='black')
    plt.plot(funnyX,reg.predict(funnyX),color='blue',linewidth=3)

    plt.xlim((-1,1))
    
    plt.show()
    
