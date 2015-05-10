from sklearn.svm import SVR
import numpy
import csv
import matplotlib.pyplot as plt

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
    reg = SVR(kernel='rbf')
    reviews = list()
    print('Importing Data')
    with open('out.csv') as csvfile:
        reader = csv.reader(csvfile,delimiter=',')
        for row in reader:
            reviews.append(Review(row))
    print('Extracting X and Y')
    funnyX=map(lambda a: [a.sentiment],reviews)
    funnyY=map(lambda a: a.funny_norm,reviews)

    svr_rbf = reg.fit(funnyX,funnyY)

    plt.scatter(funnyX,funnyY, color='black')
    plt.plot(X,svr_rbf,color='blue')

    plt.xlim((-1,1))
    
    plt.show()
    