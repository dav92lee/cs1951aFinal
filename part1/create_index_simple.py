import sys
import argparse
import json
import string
import csv
from nltk.corpus import stopwords
from porter_stemmer import PorterStemmer

# GLOBAL VARIABLES
stopwords_list = stopwords.words("english")
punc = string.punctuation
punc_table = {ord(c): None for c in punc}
stemmer = PorterStemmer()
out_dict = {}
response_per_batch = 100

def main():
	# =====================
	# ARGUMENT HANDLING
	# =====================
	parser = argparse.ArgumentParser()
	parser.add_argument('-input', help='Path to review data (do not use default files)')
	parser.add_argument('-test', action='store_true', help='use default test data set')
	opts = parser.parse_args()
	############################################################

	isTest = False
	if (opts.test):
		isTest = True
	review_filepath = opts.input


	# =====================
	# OPEN FILES
	# =====================
	if (opts.input == None):
		dataset_filepath = "../data/extracted/yelp_dataset_challenge_academic_dataset/" 

		if(isTest):
			test_dataset_filepath = "../data/extracted/yelp_phoenix_academic_dataset/" 
			dataset_filepath = test_dataset_filepath

		review_filepath = dataset_filepath+"yelp_academic_dataset_review.json"

	f_in = open(review_filepath, 'r')
		
	

	output_filename = "out.txt"
	if isTest:
		output_filename = "outtest.txt"

	f_out = open(output_filename, "w")


	# =====================
	# LOOP THROUGH FILE
	# =====================
	line_num = 0
	for review in f_in:
		print line_num
		review_obj = json.loads(review)
		text = review_obj["text"]
		review_id = line_num
		line_num += 1
		business_id = review_obj["business_id"]

		#tokenizer outputs a list of (word, index) tuples from the inputted text string
		word_tup_arr = tokenizer(text)
		
		for word in word_tup_arr:
			index_arr = word_tup_arr[word]
			cur_review = (business_id, review_id, index_arr)
			if word not in out_dict:
				out_dict[word] = []
			out_dict[word].append(cur_review)

	print "read complete"

	# =====================
	# OUTPUT FILE
	# =====================
	f_in.close()
	csv_writer = csv.writer()
	#/loop through dict
	for word in out_dict:
		word_tuple = out_dict[word]
		csv_writer.writerow([word, word_tuple])







# =====================
# TOKENIZER
# =====================

def tokenizer(text):
	word_tup_arr = {}
	word_arr = []

	# PARSING/PROCESSING ENTIRE TEXT
		# ---
	# [] Lowercase
	text = text.lower()
	# [] Remove Punctuation
	text = text.translate(punc_table)

	text = text.replace("\n", " ")
	words = text.split(" ")
	index = -1  #first index will be 0
	for word in words:
		index += 1
		# PARSING/PROCESSING SINLGE WORDS
		# ---
		# [] Stemming 
		word = stemmer.stem(word, 0, len(word)-1)
		# [] Remove Stopwords
		if word in stopwords_list:
			continue
		# ADD TO WORD TUP LIST
		if len(word) == 0:
			continue
		if word not in word_arr:
			word_arr.append(word)
			word_tup_arr[word] = []
		word_tup_arr[word].append(index)

	return word_tup_arr




#===========================================
# Run Code
#===========================================


if __name__ == '__main__':
	main()


