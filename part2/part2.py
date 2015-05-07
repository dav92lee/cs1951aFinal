import sys
import argparse
import json
import csv
# from sentiment import getSentiment

# ================
# GLOBAL VARIABLES
# ================
time_normalize_factor = float(2015-2004) #today-yelp's founding date

def parseReviews(review_filepath):
	f_in = open(review_filepath, 'r')
	f_out = open ("out.csv", "w")
	csv_writer = csv.writer(f_out)
	for review in f_in:
		review_obj = json.loads(review)
		text = review_obj["text"]
		date = review_obj["date"]
		votes = review_obj["votes"]
		funny = votes["funny"]
		useful = votes["useful"]
		cool = votes["cool"]
		year = int(date.split("-")[0])
		normalize_factor = float(2015-year)/time_normalize_factor
		funny_norm = float(funny/normalize_factor)
		useful_norm = float(useful/normalize_factor)
		cool_norm = float(cool/normalize_factor)

		sentiment = getSentiment(text) #TODO: JADLER FILL IN HERE

		csv_writer.writerow([sentiment, funny, useful, cool, funny_norm, useful_norm, cool_norm])

	f_in.close()
	f_out.close()



if __name__ == '__main__':
	# =====================
	# ARGUMENT HANDLING
	# =====================
	parser = argparse.ArgumentParser()
	parser.add_argument('-input', help='Path to review data (do not use default files)')
	parser.add_argument('-test', action='store_true', help='use default test data set')
	opts = parser.parse_args()

	isTest = False
	if(opts.test):
		isTest = True
	review_filepath = opts.input

	if (opts.input == None):
		dataset_filepath = "../../data/extracted/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review" 

		if(isTest):
			dataset_filepath = dataset_filepath+"_test"

		review_filepath = dataset_filepath+".json"


	parseReviews(review_filepath)