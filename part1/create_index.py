import sys
import ast
import argparse
import json
import re
import string
import csv
import os
from nltk.corpus import stopwords
import shutil
from porter_stemmer import PorterStemmer
from itertools import groupby

# GLOBAL VARIABLES
stopwords_list = stopwords.words("english")
punc = string.punctuation
punc_table = {ord(c): None for c in punc}
stemmer = PorterStemmer()
responses_per_batch = 5000
punc_regex = re.compile('[%s]' % re.escape(string.punctuation))
# FILEPAHTS
temp_map_dir = "temp_map"
temp_reduce_dir = "temp_reduce_dir"

def mapwords():
	#variables used
	isTest = False
	map_out_dict = {}

	# =====================
	# ARGUMENT HANDLING
	# =====================
	parser = argparse.ArgumentParser()
	parser.add_argument('-input', help='Path to review data (do not use default files)')
	parser.add_argument('-test', action='store_true', help='use default test data set')
	opts = parser.parse_args()
	############################################################

	if (opts.test):
		isTest = True
	review_filepath = opts.input


	# =====================
	# OPEN FILES
	# =====================
	if (opts.input == None):
		dataset_filepath = "../../data/extracted/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review" 

		if(isTest):
			dataset_filepath = dataset_filepath+"_test"

		review_filepath = dataset_filepath+".json"

	f_in = open(review_filepath, 'r')


	if not os.path.exists(temp_map_dir):
	    os.makedirs(temp_map_dir)
	else:
	    shutil.rmtree(temp_map_dir)           #removes all the subdirectories!
	    os.makedirs(temp_map_dir)

	# =====================
	# LOOP THROUGH FILE
	# =====================
	line_num = 0
	output_num = 0
	for review in f_in:
		review_obj = json.loads(review)
		text = review_obj["text"]
		review_id = line_num
		line_num += 1
		business_id = review_obj["business_id"].encode('utf-8')

		#tokenizer outputs a list of (word, index) tuples from the inputted text string
		word_tup_arr = tokenizer(text)
		
		for word in word_tup_arr:
			index_arr = word_tup_arr[word]
			cur_review = (business_id, review_id, index_arr)
			if word not in map_out_dict:
				map_out_dict[word] = []
			map_out_dict[word].append(cur_review)


		# =====================
		# OUTPUT TEMP MAP FILE
		# =====================
		if (line_num%responses_per_batch == 0):
			#write to temp output
			output_num = line_num/responses_per_batch
			print output_num
			map_out_filename = temp_map_dir + "/" + "mapoutput_" + str(output_num) + ".csv"
			f_map_out = open(map_out_filename, 'w')
			csv_writer = csv.writer(f_map_out)
			#sort dict
			temp_vocab = map_out_dict.keys()
			temp_vocab.sort()
			for word in temp_vocab:
				word_tuple = map_out_dict[word]
				word = word.encode('utf-8')
				csv_writer.writerow([word, word_tuple])
			#write dict to temp output
			map_out_dict = {}
			f_map_out.close()


	#write out last batch of files
	output_num += 1
	map_out_filename = temp_map_dir + "/" + "mapoutput_" + str(output_num) + ".csv"
	f_map_out = open(map_out_filename, 'w')
	csv_writer = csv.writer(f_map_out)
	#sort dict
	temp_vocab = map_out_dict.keys()
	temp_vocab.sort()
	for word in temp_vocab:
		word_tuple = map_out_dict[word]
		word = word.encode('utf-8')
		csv_writer.writerow([word, word_tuple])
	#write dict to temp output
	f_map_out.close()


	f_in.close()




def mergeDocs(dir1, dir2):
	#reduce single directory
	#merging temp output files
	old_reduce_dir = dir1
	new_reduce_dir = dir2
	old_reduce_dir_files = listdir_nohidden(old_reduce_dir)
	len_old_reduce_dir = len(old_reduce_dir_files)

	#mkdir temp_reduce_dir
	if not os.path.exists(new_reduce_dir):
	    os.makedirs(new_reduce_dir)
	else:
	    shutil.rmtree(new_reduce_dir)           #removes all the subdirectories!
	    os.makedirs(new_reduce_dir)

	# MERGING FILES
	# -------------
	for i in range(0, len_old_reduce_dir, 2):
		#merge files
		if i+1 == len_old_reduce_dir:
			#just copy file
			cur_in_filepath1 = old_reduce_dir+"/"+old_reduce_dir_files[i]
			cur_out_filepath = new_reduce_dir+"/"+"mapfile" + str((i+2)/2) + ".csv"
			cur_in_file1 = open(cur_in_filepath1 ,"r")
			cur_out_file = open(cur_out_filepath ,"w")
			csv_writer = csv.writer(cur_out_file)
			for line in cur_in_file1:

				line_arr = line.split(",",1)
				if (len(line_arr[0]) == 0) or (len(line_arr[1]) == 0): continue
				word = line_arr[0]
				occurance_arr = eval(line_arr[1])
				csv_writer.writerow([word, occurance_arr])

		else:
			#merge two files
			cur_in_filepath1 = old_reduce_dir+"/"+old_reduce_dir_files[i]
			cur_in_filepath2 = old_reduce_dir+"/"+old_reduce_dir_files[i+1]
			cur_out_filepath = new_reduce_dir+"/"+"mapfile" + str((i+2)/2) + ".csv"
			cur_in_file1 = open(cur_in_filepath1 ,"r")
			cur_in_file2 = open(cur_in_filepath2 ,"r")
			cur_out_file = open(cur_out_filepath ,"w")
			csv_writer = csv.writer(cur_out_file)
			
			#merge (both files still have line)
			used_line1 = True
			used_line2 = True
			file1_complete = False
			file2_complete = False
			while True:
				if used_line1:
					line1=cur_in_file1.readline()
					used_line1 = False
				if used_line2:
					line2=cur_in_file2.readline()
					used_line2 = False
				if not line1:
					file1_complete = True
				if not line2:
					file2_complete = True
				if file1_complete or file2_complete: 
					break
				line1_arr = line1.split(",",1)
				line2_arr = line2.split(",",1)


				try:
				    gotdata = line1_arr[1]
				except IndexError:
				    print "=== CANNOT READ LINE ==="
				    print line1
				if (len(line1_arr) != 2) or (len(line1_arr[0]) == 0) or (len(line1_arr[1]) == 0):
					used_line1 = True
					continue


				try:
				    gotdata = line2_arr[1]
				except IndexError:
				    print "=== CANNOT READ LINE ==="
				    print line2
				if (len(line2_arr) != 2) or (len(line2_arr[0]) == 0) or (len(line2_arr[1]) == 0):
					used_line2 = True
					continue
				word1 = line1_arr[0]
				word2 = line2_arr[0]

				# Slowndown but uses arrays instead of strings
				# ==================================
				# occurance_arr1 = line1_arr[1].strip()[1:-1]
				# occurance_arr1 = ast.literal_eval(occurance_arr1)
				# occurance_arr2 = line2_arr[1].strip()[1:-1]
				# occurance_arr2 = ast.literal_eval(occurance_arr2)
				# combined_occurance_arr = occurance_arr1+occurance_arr2

				# Faster but uses strings (needs to be tested)
				# =======================
				occurance_arr1 = ast.literal_eval(line1_arr[1].strip())
				occurance_arr2 = ast.literal_eval(line2_arr[1].strip())
				combined_occurance_arr = occurance_arr1[:-1] +", "+ occurance_arr2[1:]
				#if words are equal, combine entry; else, place one ahead of the other
				if word1 == word2:
					csv_writer.writerow([word1, combined_occurance_arr])
					# print type(occurance_arr1)
					used_line1 = True
					used_line2 = True
				elif word1 > word2:
					#word2 is earlier in alphabet
					csv_writer.writerow([word2, occurance_arr2])
					used_line2 = True
				else:
					#word1 is earlier in alphabet
					csv_writer.writerow([word1, occurance_arr1])
					used_line1 = True



			if not file1_complete:
				#write out file1
				while True:
					line = cur_in_file1.readline()
					if not line: break
					line_arr = line.split(",", 1)
					if (len(line_arr[0]) == 0) or (len(line_arr[1]) == 0): continue
					word = line_arr[0]
					occurance_arr = eval(line_arr[1])
					csv_writer.writerow([word, occurance_arr])

			if not file2_complete:
				#write out file2
				while True:
					line = cur_in_file2.readline()
					if not line: break
					line_arr = line.split(",", 1)
					if (len(line_arr[0]) == 0) or (len(line_arr[1]) == 0): continue
					word = line_arr[0]
					occurance_arr = eval(line_arr[1])
					csv_writer.writerow([word, occurance_arr])




			cur_in_file1.close()
			cur_in_file2.close()
			cur_out_file.close()


# =====================
# TOKENIZER
# =====================

def tokenizer(text):
	word_tup_arr = {}
	word_arr = []

	# PARSING/PROCESSING ENTIRE TEXT
		# ---
	# [] replace newline characters
	text = text.replace('\r', ' ')
	text = text.replace('\n', ' ')
	# [] Lowercase
	text = text.lower()
	# [] Remove Punctuation
	text = punc_regex.sub('', text)

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
		# [] Remove duplicate letters (up to 3)
		''.join(''.join(letter)[:3] for _, letter in groupby(word))
		# [] Remove short/long words
		if len(word) < 3 or len(word) > 20:
			continue
		# ADD TO WORD TUP LIST
		if word not in word_arr:
			word_arr.append(word)
			word_tup_arr[word] = []
		word_tup_arr[word].append(index)

	return word_tup_arr


def listdir_nohidden(path):
	dir_arr = []
	dirfiles = os.listdir(path)
	for f in dirfiles:
		if not f.startswith('.'):
			dir_arr.append(f)
	return dir_arr

#===========================================
# Run Code
#===========================================


if __name__ == '__main__':
	# mapwords()
	# print "map complete"
	dir1 = temp_map_dir
	dir2 = temp_map_dir + "1"
	reduce_count = 1
	dir1_length = len(listdir_nohidden(dir1))
	while (dir1_length > 1):
		mergeDocs(dir1, dir2)
		reduce_count += 1
		dir1 = dir2
		dir2 = temp_reduce_dir + str(reduce_count)
		dir1_length = len(listdir_nohidden(dir1))
	print "reduce complete"

