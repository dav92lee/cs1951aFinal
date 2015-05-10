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
            tokens = tokenizer(term)
            if len(tokens)>0:
                term_token = tokens[0]
            self.sent_dict[term_token] = float(score)
    def getSentiment(self,text):
        text_tokens = tokenizer(text)
        score = 0.0
        for token in text_tokens:
            if token in self.sent_dict:
                score += self.sent_dict[token]
        if len(text_tokens) == 0:
            return 0
        return score/(len(text_tokens)*5)
        
