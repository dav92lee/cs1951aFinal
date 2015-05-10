from create_index import tokenizer
from math import log
import ast
import operator
import json


index_filepath = "inverted_index.csv"
index_f = open(index_filepath, "r")
business_filepath = "../../data/extracted/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business.json"
business_f = open(business_filepath, "r")
N = 1500000 #approx number of documents in the dataset
timenow = 2015
timestart = 2004
# One word query (OWQ): a single word (i.e. pizza). It will return a set 
# of businesses whose review contains the search term.
def q1(query_str):
	print "q1"
	results = []

	tokenized_query_str = tokenizer(query_str).keys()
	if len(tokenized_query_str) > 0:
		query_str = tokenized_query_str[0]
	
	index_f.seek(0)
	for line in index_f:
		line_arr = line.split(",", 1)
		word = line_arr[0]
		if word == query_str:
			content_arr = ast.literal_eval(line_arr[1].strip()[1:-1])
			df = len(content_arr)
			for review in content_arr:
				b_id = review[0]
				b_line = review[1]
				b_indices = review[2]
				b_date = review[3]
				tf = len(b_indices)
				score = getScore(tf, df, b_date)
				updated_review = (b_id, b_line, b_indices, b_date, score)
				results.append(updated_review)
			break



	return results

# Free text query (FTQ): a sequence of at least two words, separated by 
# a space (i.e. taco burrito). It will return a set of businesses whose
# reviews contains all search terms in any order. For this query, you can
# treat all the reviews for a particular business as one single review.
# For example, if there is a business with two reviews, one containing
# the word "taco" and the other containing the word "burrito", this 
# business should be considered in the returned results.
def q2(query_str):
	print "q2"
	results = []

	query_str = tokenizer(query_str).keys()
	num_words = len(query_str)
	found = 0
	index_f.seek(0)
	approved_lines = []
	full_results = []
	#TODO: Calculate rating, approved docs
	for line in index_f:
		line_arr = line.split(",", 1)
		word = line_arr[0]
		if word in query_str:
			content_arr = ast.literal_eval(line_arr[1].strip()[1:-1])
			df = len(content_arr)
			word_docs = []
			temp_result = []
			for review in content_arr:
				b_id = review[0]
				b_line = review[1]
				b_indices = review[2]
				b_date = review[3]
				tf = len(b_indices)
				score = getScore(tf, df, b_date)
				word_docs.append(b_line)
				updated_review = (b_id, b_line, b_indices, b_date, score)
				temp_result.append(updated_review)
			full_results = temp_result + full_results
			found += 1
			if found == 1:
				approved_lines = word_docs
			else:
				approved_lines = list(set(approved_lines).intersection(word_docs))
			if found == num_words:
				break


	#TODO: filter via approved docs
	for review in full_results:
		b_line = review[1]
		if b_line in approved_lines:
			results.append(review)


	return results

# Phrase query (PQ): a sequence of at least two words, separated by a
# space and in double quotes (i.e. "fish taco"). It will return a set 
# of businesses whose review contains all search terms in the given order.
def q3(query_str):
	print "q3"
	results = []
	#only used to determine number of unique words to be found (no repeats)
	temp_query_str = tokenizer(query_str).keys() 
	num_unique_words = len(temp_query_str)
	found = 0

	query_str_split = query_str.split()
	query_str_arr = []
	tokenized_query_str = tokenizer(query_str).keys()
	if len(tokenized_query_str) > 0:
		query_str = tokenized_query_str[0]
	for query_word in query_str_split:
		
		tokenized_query_word = tokenizer(query_word).keys()
		if len(tokenized_query_word) > 0:
			tokenized_query_word = tokenized_query_word[0]
			query_str_arr.append(tokenized_query_word)
	
	query_str = query_str_arr
	num_words = len(query_str)

	# query_str is an array of all the words that we will consider
	
	#START (USE QUERY STR TO PROCESS)
	full_results = []
	possible_reviews = []
	for j in range(0, num_words):
		full_results.append(0)

	index_f.seek(0)

	for line in index_f:
		line_arr = line.split(",",1)
		word = line_arr[0]
		if word in query_str:
			content_arr = ast.literal_eval(line_arr[1].strip()[1:-1])
			#store all possible reviews
			indices = [i for i, x in enumerate(query_str) if x == word]

			#edit possible docs
			cur_possible_reviews = []
			df = len(content_arr)
			temp_result = []
			for review in content_arr:
				b_id = review[0]
				b_line = review[1]
				b_indices = review[2]
				b_date = review[3]	
				tf = len(b_indices)
				score = getScore(tf, df, b_date)
				updated_review = (b_id, b_line, b_indices, b_date, score)
				temp_result.append(updated_review)
				if b_line not in cur_possible_reviews:
					cur_possible_reviews.append(int(b_line))

			for index in indices:
				full_results[index] = temp_result

			if (found != 0):
				possible_reviews = list(set(possible_reviews).intersection(cur_possible_reviews))
			else:
				possible_reviews = list(set(cur_possible_reviews))

			found += 1
			# for review in content_arr:


	if found != num_unique_words:
		return []

	# We now have 
	#	- full_results: list of lists of response entries where entry i is word i in our query
	#	- possible_reviews: list of all possible reviews that still satisfy our conditions
	#						(for first level filtering)
	# We need for calculations:
	#	- review_indices_map: map of line_num -> index_num for the first word in the query string
	review_indices_map = {}
	for i in range(0, len(full_results)):
		word_entry = full_results[i]
		for j in range(0, len(word_entry)):
			review_entry = word_entry[j]
			review_line = review_entry[1]
			if review_line in possible_reviews:
				index_array = review_entry[2]
				if i == 0:
					review_indices_map[review_line] = index_array
				else:
					temp_index_array = [x-i for x in index_array]
					intersection = list(set(review_indices_map[review_line]).intersection(temp_index_array))
					review_indices_map[review_line] = intersection
					
	# loop through one last time
	for i in range(0, len(full_results)):
		content_arr = full_results[i]
		for review in content_arr:
			b_line = review[1]
			if b_line in possible_reviews:
				b_indices = review[2]
				b_id = review[0]
				b_date = review[3]	
				b_score = review[4]
				temp_review_index = (x+i for x in review_indices_map[review_line])
				intersection = list(set(temp_review_index).intersection(b_indices))
				if len(intersection):
					updated_review = (b_id, b_line, intersection, b_date, score)
					results.append(updated_review)

	# first_word_entry = full_results[0]
	# for review_entry in first_word_entry:
	# 	review_line = review_entry[1]
	# 	index_array = review_entry[2]
	# 	if review_line in review_indices_map:
	# 		intersection = list(set(review_indices_map[review_line]).intersection(index_array))
	# 		if len(intersection) > 0:
	# 			new_review_entry = (review_entry[0], review_line, intersection)
	# 			results.append(new_review_entry)
	return results

#Location specific query (LSQ): an OWQ, FTQ or PQ restricted to a
# user-specified city. Just like Yelp.com your search engine should
# be able to make queries, restricting results to a single city or
# multiple cities. Below are a few examples of what these queries 
# should look like. Please use IN to specify that you are doing an 
# LSQ followed by a city or cities separated by commas.
	# One word query (OWQ): pizza IN charlotte
	# Free text query (FTQ): taco burrito IN las vegas, edinburgh
	# Phrase query (PQ): "fish taco" IN madison, waterloo, phoenix
def q4(query_str):
	print "q4"
	query_arr = query_str.split("IN")
	query = query_arr[0].strip()
	city = query_arr[1].strip()
	city_unclean_arr = city.split(",")
	city_arr = []
	for city in city_unclean_arr:
		cur_city = city.strip().lower()
		city_arr.append(cur_city)
	
	qType = determineQType(query)
	output_reviews = []
	if qType == 1:
		output_reviews = q1(query)
	elif qType == 2:
		output_reviews = q2(query)
	elif qType == 3:
		output_reviews = q3(query)
	
	business_list = []
	for review in output_reviews:
		business = review[0]
		business_list.append(business)

	#loop through business document
	approved_business_list = []
	business_f.seek(0)
	for business_entry in business_f:
		business_obj = json.loads(business_entry)
		business_name = business_obj["business_id"]
		business_city = business_obj["city"].lower()
		if business_name in business_list:
			if business_city in city_arr:
				approved_business_list.append(business_name)


	#filter results based off of approved businesses	
	result = []
	for review in output_reviews:
		business = review[0]
		if business in approved_business_list:
			result.append(review)


	return result

def determineQType(query_str):
	query_arr = query_str.split(" ")
	len_q = len(query_arr)

	
	if query_str[0] == '"' and query_str[-1] == '"' and len_q > 1:
		return 3
	if "IN" in query_arr:
		return 4
	if len_q == 1:
		return 1
	return 2

def getScore(tf, df, date):
	year_posted = int(date.split("-",1)[0])
	score = (1+log(tf))*log(float(N)/df) + (float(year_posted-timestart)/(timenow-timestart))
	return score

def rankOutput(output_reviews):
	business_id_list = {}
	for review in output_reviews:
		b_id = review[0]
		b_score = review[4]
		if b_id not in business_id_list:
			business_id_list[b_id] = float(b_score)
		else:
			business_id_list[b_id] += float(b_score)

	sorted_business_id = sorted(business_id_list.items(), key=operator.itemgetter(1), reverse=True)

	results = []
	for business in sorted_business_id:
		business_id = business[0]
		results.append(business_id)

	return results


def getBusinessNames(business_id_list):
	business_f.seek(0)
	business_name_list = business_id_list
	for line in business_f:
		business_obj = json.loads(line)
		business_id = business_obj["business_id"]
		if business_id in business_id_list:
			for i in range(0, len(business_name_list)):
				temp_business_id = business_name_list[i]
				if temp_business_id == business_id:
					business_name = business_obj["name"]
					business_name_list[i] = business_name
			
	return business_name_list

if __name__ == '__main__':
	while True:
		cur_query = raw_input('-->').strip()
		qType = determineQType(cur_query)
		output_reviews = ""
		if qType == 1:
			output_reviews = q1(cur_query)
		elif qType == 2:
			output_reviews = q2(cur_query)
		elif qType == 3:
			output_reviews = q3(cur_query)
		elif qType == 4:
			output_reviews = q4(cur_query)
		if output_reviews == []:
			print "[]"
		else:
			business_id_list =  rankOutput(output_reviews)
			business_name_list = getBusinessNames(business_id_list)
			for i in range(0, len(business_name_list)):
				business_name = business_name_list[i]
				print str(i+1) + ": " + business_name
		# loop through output, to sort businesses (don't forget to combine same businesses, but diff rating)
		# transform last data structure into business names
	index_f.close()
	business_f.close()