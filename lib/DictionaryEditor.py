import re
import nltk
import numpy as np
import os
import time
from shutil import copyfile

from .WordSanitizer import WordSanitizer
from .ListManipulator import ListManipulator

class DictionaryEditor:
	
	@classmethod
	def tokenize_txt_file(cls, txt_src, txt_target=None, regex=None):
		"""
			Converts txt file into tokens 

			Args:
				txt_src(str): Source txt file location
				txt_target(str, optional): Target txt file location, if left blank will replace the src file
				regex(str, optional): Regex on how to split the tokens, if left blank will use space 
		"""
		text_list = []
		if not regex:
			regex = "\s+"

		if not txt_target:
			txt_target = txt_src[:-4]+"_tokenized.txt"

		temp_target = txt_target[:-4]+"_temp.txt"
		txt_writer = open(temp_target, 'w')
		word_count = 0

		try:
			read_src = open(txt_src, 'r')
			readline_src = read_src.readlines()
			if readline_src is not None:
				for text in readline_src:
					text = text.lower()
					text = re.compile(regex).split(text)
					for word in text:
						word_count += 1 
						text_list.append(word.strip())

			else:
				raise Exception('Source not found error')
			
			word_list = np.unique(text_list).tolist()

			for index, word in enumerate(word_list):
				if(word):
					txt_writer.write(word+"\n")

			txt_writer.close()
			cls.rotate_file(txt_target, temp_target)

		except Exception as error:
			print(str(error)+" has ocurred...")


	@classmethod
	def remove_similar_tokens(cls, src_1_dir, src_2_dir):
		"""
			Removes similar tokens from 2 txt sources

			Args:
				src1(str): First txt source
				src2(str): Second txt source
		"""
		temp_src_1_dir = src_1_dir[:-4]+"_temp.txt"
		src_1_reader = open(src_1_dir, 'r')
		src_1_writer = open(temp_src_1_dir, 'w')

		temp_src_2_dir = src_2_dir[:-4]+"_temp.txt"
		src_2_reader = open(src_2_dir, 'r')
		src_2_writer = open(temp_src_2_dir, 'w')

		try:
			src_1_list = []
			readline_src = src_1_reader.readlines()
			if readline_src is not None:
				for text in readline_src:
					src_1_list.append(text.strip())
			else:
				raise Exception("First Source is empty")

			src_2_list = []
			readline_src = src_2_reader.readlines()
			if readline_src is not None:
				for text in readline_src:
					src_2_list.append(text.strip())
			else:
				raise Exception("First Source is empty")

			src_1_list, src_2_list = ListManipulator.xor_list(src_1_list, src_2_list)

			for word in src_1_list:
				src_1_writer.write(word+"\n")

			for word in src_2_list:
				src_2_writer.write(word+"\n")

			src_1_writer.close()
			src_2_writer.close()
			cls.rotate_file(src_1_dir, temp_src_1_dir)
			cls.rotate_file(src_2_dir, temp_src_2_dir)

		except Exception as error:
			print(str(error)+" has ocurred...")

	@classmethod
	def check_writing_status(cls, src, check_period=2):
		"""
			Checks if file is still updating and return True when finishes updating and vice versa
			
			Args:
				src(str): Source file Location

			Return:
				finish_signal(bool): File finishes updating or not
		"""
		file = os.stat(src)
		file_size = file.st_size
		time.sleep(check_period)

		curr_file = os.stat(src)
		curr_size = file.st_size
		comp = file_size - curr_size
		if comp == 0:
			return True
		else:
			return False


	@classmethod
	def rotate_file(cls, main_dir, temp_dir):
		"""
			Rotate temp file with main file

			Args:
				main_dir(str): Location of main file
				temp_dir(str): Location of temporary file
		"""
		if(os.path.isfile(main_dir)):
			os.remove(main_dir)
		copyfile(temp_dir, main_dir)
		os.remove(temp_dir)
