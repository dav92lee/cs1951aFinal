import sys
import json
from tokenizer import tokenizer

SENTIMENT_FILE='AFINN/AFINN-111.txt'

class Sentiment:
    def __init__(self):
        self.sent_dict=dict()
        sent_file = open(SENTIMENT_FILE)
        for line in sent_file:
            term,score = line.split('\t')
            term_token = tokenizer(term)[0]
            sent_dict[term_token] = float(score)
    def getSentiment(self,text):
        text_tokens = tokenizer(text)
        score = 0.0
        for token in text_tokens:
            if token in self.sent_dict:
                score += sent_dict[token]
        return score/(len(text_tokens)*5)
