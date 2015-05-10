from bs4 import BeautifulSoup
import os
from sentiment import Sentiment
import csv

if __name__ == '__main__':
    files = os.listdir('./zagat')
    csvFile = open('out.csv','w')
    writer = csv.writer(csvFile)
    sentiment = Sentiment()
    for f in files:
        with open('./zagat/'+f) as review:
            soup = BeautifulSoup(review)
            review_city = soup.find(itemprop='addressLocality').text
            review_state = soup.find(itemprop='addressRegion').text
            review_text = soup.find(itemprop='reviewBody').text
            review_sent = sentiment.getSentiment(review_text)
            writer.writerow([str(review_sent),review_state,review_city])
    close(csvFile)
    
            
