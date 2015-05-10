from bs4 import BeautifulSoup
import os

if __name__ == '__main__':
    files = os.listdir('./zagat')
    for f in files:
        with open(f) as review:
            soup = BeautifulSoup(review)
            print(soup.find(itemprop='adressLocality'))
