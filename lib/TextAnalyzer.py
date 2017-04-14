import nltk
from nltk.corpus import stopwords
import re
import os
import numpy as np
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class TextAnalyzer:

	word_list = []
	sent_list = []

	def __init__(self, word_list_dir=None, pos_sent_list_dir=None, neg_sent_list_dir=None):
		"""
			Initializing Text Analyzer Object, User may insert the word list dictionary and sentiment 
			dictionary for further usage

			Args:
				word_list_dir(str, optional): Directory of the word dictionary list (file in txt format)
				pos_sent_dir(str, optional): Directory of positive sentiment dictionary list (file in txt format)
				neg_sent_dir(str, optional): Directory of negative sentiment dictionary list (file in txt format)
		"""
		self.word_list_dir = word_list_dir
		self.pos_sent_list_dir = pos_sent_list_dir
		self.neg_sent_list_dir = neg_sent_list_dir

		self.factory = StemmerFactory()
		self.stemmer = self.factory.create_stemmer()
		self.stop = stopwords.words('bahasa') 	

		# Loading Word List Dictionary if given
		if (word_list_dir is not None):
			if os.path.isfile(word_list_dir):
				read_word = open(word_list_dir, 'r')
				readline_word = read_word.readlines()
				if readline_word is not None:
					for word in readline_src:
						self.word_list.append(word)
				else:
					raise StandardError("Word List Dictionary is empty")
			else:
				raise StandardError("Word List Dictionary is not found")

		# Loading Positive Sentiment List Dictionary if given
		if (pos_sent_list_dir is not None):
			if os.path.isfile(pos_sent_list_dir):
				read_sen = open(pos_sent_list_dir, 'r')
				readline_sen = read_sen.readlines()
				if readline_sen is not None:
					for sen in readline_src:
						self.pos_sent_list.append(sen)
				else:
					raise StandardError("Positive Sentiment List Dictionary is empty")
			else:
				raise StandardError("Positive Sentiment List Dictionary is not found")

		# Loading Negative Sentiment List Dictionary if given
		if (neg_sent_list_dir is not None):
			if os.path.isfile(neg_sent_list_dir):
				read_sen = open(neg_sent_list_dir, 'r')
				readline_sen = read_sen.readlines()
				if readline_sen is not None:
					for sen in readline_src:
						self.neg_sent_list.append(sen)
				else:
					raise StandardError("Negative Sentiment List Dictionary is empty")
			else:
				raise StandardError("Negative Sentiment List Dictionary is not found")

	def retrieve_non_dictionary_words(self, text, word_list_dir=None):
		if (word_list_dir is not None):
			self.word_list_dir = word_list_dir

			# Loading Word List Dictionary if given
			if (word_list_dir is not None):
				if os.path.isfile(word_list_dir):
					read_word = open(word_list_dir, 'r')
					readline_word = read_word.readlines()
					if readline_word is not None:
						for word in readline_src:
							self.word_list.append(word)
					else:
						raise StandardError("Word List Dictionary is empty")
				else:
					raise StandardError("Word List Dictionary is not found")

		if (not self.word_list):
			return "No dictionary found"

		filtered_text = [word for word in text if word not in word_list]
		return filtered_text

	def retrieve_unique_words(self, text):
		"""
			Returns list of unique words

			Args:
				text(str): Text string to be refactored

			Return:
				word_list(list(string)): List of unique words
		"""
		splitted_text = re.findall("([a-zA-Z]+|[0-9]+|[^\w\s]+)", text)
		word_list = np.unique(splitted_text).tolist()
		return word_list

	def retrieve_word_count(self, text):
		"""
			Returns list of words with its word count

			Args:
				text(str): Text string to be refactored

			Return:
				word_list(dict{string: qty}): List of unique words and its count
		"""
		word_list = nltk.FreqDist(text.lower().split())
		return word_list

	def normalize_text(self, text):
		"""
			Returns normalized version of the text
			Normalization means removal of non-alphanumeric characters and stemming of word.
			Also remove stopwords

			Args:
				text(str): Text to be normalized

			Return: 
				normalized_text(str): Normalized text
		"""
		normalized_list = self.stemmer.stem(text)
		normalized_list = [word for word in normalized_list.split(" ") if word not in self.stop]
		normalized_text = " ".join(normalized_list)
		# print(normalized_text)

		return normalized_text