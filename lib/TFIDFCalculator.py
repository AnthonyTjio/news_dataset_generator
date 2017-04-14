import nltk
import numpy as np

from .TextAnalyzer import TextAnalyzer

class TFIDFCalculator:

	def __init__(self):
		self.textAnalyzer = TextAnalyzer()
		self.word_list = []

	def load_possible_terms_from_list(self, text_list):
		"""
			Retrieve possible words/terms from list of text

			Args:
				text_list(list(string)): List containing text which term to be extracted
		"""
		temp_word_list = []

		for text in text_list:
			text = self.textAnalyzer.normalize_text(text)
			temp_word_list += self.textAnalyzer.retrieve_unique_words(text)

		self.word_list += np.unique(temp_word_list)
		self.word_list = np.unique(self.word_list).tolist()
		self.text_collection = nltk.TextCollection(self.word_list)

	def load_possible_terms_from_text(self, text):
		"""
			Retrieve possible words/terms from text

			Args:
				text(string): Text which term to be extracted
		"""
		text = self.textAnalyzer.normalize_text(text)
		temp_word_list = self.textAnalyzer.retrieve_unique_words(text)

		self.word_list += np.unique(temp_word_list).tolist()
		self.word_list = np.unique(self.word_list).tolist()
		self.text_collection = nltk.TextCollection(self.word_list)

	def calculate_tf_idf_from_list(self, text_list):
		"""
			Calculate tf-idf of list of text
			TF: Num of times word appears in a text list/ Total num of words in that text

			Args:
				text_list(list(str)): List of text to calculate tf-idf

			Return:
				tf_dict(dict(index: (dict(term: tf_idf)))): dictionary of text's index where it contains dictionary
															of terms containing freq dist
		"""
		tf_idf = {}

		#get tf_idf score
		for index, text in enumerate(text_list):
			text = self.textAnalyzer.normalize_text(text)
			text_dist = self.textAnalyzer.retrieve_word_count(text)
			tf_idf[index] = {}
			for term in text_dist.keys():
				tf_idf[index][term] = self.text_collection.tf_idf(term, text)

		return tf_idf

	def calculate_tf_idf_from_text(self, text):
		"""
			Calculate tf-idf of  text
			TF: Num of times word appears in a text list/ Total num of words in that text

			Args:
				text(string): Text to calculate tf-idf

			Return:
				text_tf_idf(dict(term: tf_idf))): dictionaryof terms containing freq dist
		"""
		text_tf_idf = {}

		#get tf_idf score
		text = self.textAnalyzer.normalize_text(text)
		text_dist = self.textAnalyzer.retrieve_word_count(text)
		for term in text_dist.keys():
			text_tf_idf[term] = self.text_collection.tf_idf(term, text)

		return text_tf_idf

