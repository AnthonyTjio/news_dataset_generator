import re
import string

class WordSanitizer:

	@classmethod
	def remove_non_utf(cls, text):
		"""
			Removes non utf-8 characters from string

			Args:
				text(str): source string

			Returns:
				f_text(str): Filtered string
		"""	
		f_text = ''.join(c for c in text if c in string.printable)
		return f_text

	@classmethod
	def remove_hidden_characters(cls, text):
		"""
			Removes special characters from string (Ideal for purging URLs)

			Args:
				text(str): source string

			Returns:
				f_text(str): filtered string
		"""
		f_text =  re.sub("[\s]+","", text, flags=re.IGNORECASE)
		return f_text

	@classmethod
	def remove_extra_spaces(cls, text):
		"""
			Removes extra hidden characters from string

			Args:
				text(str): source string

			Returns:
				f_text(str): filtered string
		"""
		f_text =  re.sub("\s+"," ", text, flags=re.IGNORECASE).strip()
		return f_text

	@classmethod
	def remove_infrequent_symbols_in_article(cls, text):
		"""
			Removes extra hidden characters from string

			Args:
				text(str): source string

			Returns:
				f_text(str): filtered string
		"""
		f_text =  re.sub("[^\w!?$))(-:=,.) ]+","", text)
		return f_text

	@classmethod
	def clean_using_regex(cls, text, regex):
		"""
			Clean string using regex

			Args:
				text(str): source string

			Returns:
				f_text(str): filtered string
		"""
		f_text =  re.sub(regex,"", text, flags=re.IGNORECASE).strip()
		return f_text

	@classmethod
	def custom_stopwords(cls, text, stopwords):
		"""
			Removes words in stopwords

			Args:
				text(str): source string
				stopwords(list(str)): list of stopwords

			Returns:
				f_text(str): filtered string
		"""
		text_list = text.split()
		filtered_list = [word for word in text_list if word not in stopwords]
		f_text = ' '.join(filtered_list)

	@classmethod
	def sanitize_text_data(cls, text, stopwords=None):
		"""
			Perform all sanitization to the string

			Args:
				text(str): source string

			Returns:
				f_text(str): filtered string
		"""
		text = cls.remove_non_utf(text)
		text = cls.remove_extra_spaces(text)
		text = cls.remove_infrequent_symbols_in_article(text)
		if(stopwords is not None):
			text = cls.custom_stopwords(text, stopwords)

		f_text = text
		return f_text