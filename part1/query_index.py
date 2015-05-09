from create_index import tokenizer
import ast

index_filepath = "inverted_index.csv"
index_f = open(index_filepath, "r")
# One word query (OWQ): a single word (i.e. pizza). It will return a set 
# of businesses whose review contains the search term.
def q1(query_str):
	print "q1"

	tokenized_query_str = tokenizer(query_str).keys()
	if len(tokenized_query_str) > 0:
		query_str = tokenized_query_str[0]
	
	index_f.seek(0)
	for line in index_f:
		line_arr = line.split(",", 1)
		word = line_arr[0]
		if word == query_str:
			content_arr = ast.literal_eval(line_arr[1])
			break
	return content_arr

# Free text query (FTQ): a sequence of at least two words, separated by 
# a space (i.e. taco burrito). It will return a set of businesses whose
# reviews contains all search terms in any order. For this query, you can
# treat all the reviews for a particular business as one single review.
# For example, if there is a business with two reviews, one containing
# the word "taco" and the other containing the word "burrito", this 
# business should be considered in the returned results.
def q2(query_str):
	print "q2"
	query_str = tokenizer(query_str).keys()
	num_words = len(query_str)
	found = 0
	results = []
	index_f.seek(0)
	for line in index_f:
		line_arr = line.split(",", 1)
		word = line_arr[0]
		if word in query_str:
			content_arr = ast.literal_eval(line_arr[1].strip()[1:-1])
			results = results+content_arr
			found += 1
			if found == num_words:
				break

	return results

# Phrase query (PQ): a sequence of at least two words, separated by a
# space and in double quotes (i.e. "fish taco"). It will return a set 
# of businesses whose review contains all search terms in the given order.
def q3(query_str):
	print "q3"
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
			docs_arr = ast.literal_eval(line_arr[1].strip()[1:-1])
			#store all possible reviews
			indices = [i for i, x in enumerate(query_str) if x == word]
			for index in indices:
				full_results[index] = docs_arr

			#edit possible docs
			cur_possible_reviews = []
			for docs in docs_arr:
				line_num = docs[1]
				index_arr = docs[2]			
				if line_num not in cur_possible_reviews:
					cur_possible_reviews.append(int(line_num))

			if (found != 0):
				possible_reviews = list(set(possible_reviews).intersection(cur_possible_reviews))
			else:
				possible_reviews = list(set(cur_possible_reviews))

			found += 1
			# for review in docs_arr:


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
	results = []
	first_word_entry = full_results[0]
	for review_entry in first_word_entry:
		review_line = review_entry[1]
		index_array = review_entry[2]
		if review_line in review_indices_map:
			intersection = list(set(review_indices_map[review_line]).intersection(index_array))
			if len(intersection) > 0:
				new_review_entry = (review_entry[0], review_line, intersection)
				results.append(new_review_entry)
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
	#TODO
	print "q4"

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


if __name__ == '__main__':
	while True:
		cur_query = raw_input('-->').strip()
		qType = determineQType(cur_query)
		output_businesses = ""
		if qType == 1:
			output_businesses = q1(cur_query)
		elif qType == 2:
			output_businesses = q2(cur_query)
		elif qType == 3:
			output_businesses = q3(cur_query)
		elif qType == 4:
			output_businesses = q4(cur_query)
		print "======================"
		print output_businesses