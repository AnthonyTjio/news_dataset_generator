import nltk
import numpy as np
import csv
from nltk.corpus import stopwords

from .WordSanitizer import WordSanitizer
from .CSVTranslator import CSVTranslator
from .TFIDFCalculator import TFIDFCalculator

class SimilarityChecker:

	@classmethod
	def analyze(
			cls, csv_src, src_column_index, title_column_index, article_column_index, label_column_index,
		 	dest_similar, dest_unique, similarity_threshold):
		"""
			Retrieve news information in csv file and compare similar articles from different sources

			Args:
				csv_src(str): Source CSV directory
				src_column_index(int): Column index of source
				title_column_index(int): Column index of title
				article_column_index(int): Column index of content
				label_column_index(int): Column index of label
				dest_similar(str): Destination CSV file which contains similar articles
				dest_unique(str): Destination CSV file which only contain unqiue articles
				similarity_threshold(float[0 < x < 1]) similarity limit to be considered as similar (1 is exactly similar)
		"""
		with open(dest_similar, 'a') as sim_output, open(dest_unique, 'a') as uni_output:
			sim_writer = csv.writer(sim_output, delimiter=",")
			uni_writer = csv.writer(uni_output, delimiter=",")

			TfIdfCalculator = TFIDFCalculator()

			similarity_threshold = 1-similarity_threshold
			news = CSVTranslator.csv_to_list(csv_src)

			np_news = np.array(news) 
			text_list = np_news[:,article_column_index].tolist() # Retrieve articles to list

			TfIdfCalculator.load_possible_terms_from_list(text_list)
			tf_idf = TfIdfCalculator.calculate_tf_idf_from_list(text_list)

			classified_index = []
			similar_index = 0

			for main_index, main_news in enumerate(np_news):
				if (main_index in classified_index):
					print("MISS")
					continue

				print("Comparing "+main_news[title_column_index]+" from "+main_news[src_column_index])
				classified_index.append(main_index)
				similar_indexes = []

				for secondary_index in range(main_index, len(news)):
					if (secondary_index in classified_index):
						continue

					secondary_news = np_news[secondary_index]

					term1 = tf_idf[main_index].copy()
					term2 = tf_idf[secondary_index].copy()

					for term in term1:
						if term not in term2:
							term2[term] = 0

					for term in term2:
						if term not in term1:
							term1[term] = 0

					v1 = [score for (term, score) in sorted(term1.items())]
					v2 = [score for (term, score) in sorted(term2.items())]

					distance = nltk.cluster.util.cosine_distance(v1,v2) # closer to 0 is more similar

					print(main_news[title_column_index]+" COMPARED WITH "+secondary_news[title_column_index]+str(distance))
					if(distance < similarity_threshold):
						similar_indexes.append(secondary_index)

				if similar_indexes:
					similar_index += 1
					data = []
					data.append(similar_index)
					data.append(main_news[src_column_index])
					data.append(main_news[title_column_index])
					data.append(main_news[article_column_index])
					data.append(main_news[label_column_index])
					sim_writer.writerow(data)

					print(similar_indexes)
					for index in similar_indexes:
						data = []
						secondary_news = np_news[index]
						classified_index.append(index)

						data.append(similar_index)
						data.append(secondary_news[src_column_index])
						data.append(secondary_news[title_column_index])
						data.append(secondary_news[article_column_index])
						data.append(secondary_news[label_column_index])
						sim_writer.writerow(data)
				else:
					data = []
					data.append(main_news[src_column_index])
					data.append(main_news[title_column_index])
					data.append(main_news[article_column_index])
					data.append(main_news[label_column_index])
					uni_writer.writerow(data)

	@classmethod
	def safe_analyze(
			cls, csv_src, src_column_index, title_column_index, article_column_index, label_column_index,
		 	dest_similar, dest_unique, similarity_threshold):
		"""
			Retrieve news information in csv file and compare similar articles from different sources safely
			which will not trigger memory error

			Args:
				csv_src(str): Source CSV directory
				src_column_index(int): Column index of source
				title_column_index(int): Column index of title
				article_column_index(int): Column index of content
				label_column_index(int): Column index of label
				dest_similar(str): Destination CSV file which contains similar articles
				dest_unique(str): Destination CSV file which only contain unqiue articles
				similarity_threshold(float[0 < x < 1]) similarity limit to be considered as similar (1 is exactly similar)
		"""
		with open(dest_similar, 'a') as sim_output, open(dest_unique, 'a') as uni_output:
			sim_writer = csv.writer(sim_output, delimiter=",")
			uni_writer = csv.writer(uni_output, delimiter=",")

			TfIdfCalculator = TFIDFCalculator()

			similarity_threshold = 1-similarity_threshold
			news_count = CSVTranslator.get_csv_number_of_row(csv_src)

			# Retrieve possible text in article to tf-idf-calculator
			with open(csv_src, 'r') as input:
				reader = csv.reader(input, delimiter=",")
				for row_index, row in enumerate(reader):
					for column_index, column in enumerate(row):
						if(column_index == int(article_column_index)):
							TfIdfCalculator.load_possible_terms_from_text(column)
							print("Retrieving article #"+str(row_index))

			tf_idf = {}

			# Retrieve tf-idf value of each row
			with open(csv_src, 'r') as input:
				reader = csv.reader(input, delimiter=",")
				for row_index, row in enumerate(reader):
					for column_index, column in enumerate(row):
						if(column_index == int(article_column_index)):
							tf_idf[row_index] = TfIdfCalculator.calculate_tf_idf_from_text(column)
							print(tf_idf[row_index])

			classified_index = []
			similar_index = 0

			for main_index in range(news_count):
				if (main_index in classified_index):
					continue

				print("Comparing News from rowv"+str(main_index))

				classified_index.append(main_index)
				similar_indexes = []

				for secondary_index in range(main_index, news_count):
					if (secondary_index in classified_index):
						continue
					print(secondary_index)
					term1 = tf_idf[main_index]
					term2 = tf_idf[secondary_index]

					for term in term1:
						if term not in term2:
							term2[term] = 0

					for term in term2:
						if term not in term1:
							term1[term] = 0

					v1 = [score for (term, score) in sorted(term1.items())]
					v2 = [score for (term, score) in sorted(term2.items())]

					distance = nltk.cluster.util.cosine_distance(v1,v2) # closer to 0 is more similar

					if(distance < similarity_threshold):
						similar_indexes.append(secondary_index)

				if similar_indexes:
					similar_index += 1
					data = []
					main_news = CSVTranslator.get_csv_row(csv_src, main_index)

					data.append(similar_index)
					data.append(main_news[src_column_index])
					data.append(main_news[title_column_index])
					data.append(main_news[article_column_index])
					data.append(main_news[label_column_index])
					sim_writer.writerow(data)

					print(similar_indexes)
					for index in similar_indexes:
						data = []
						secondary_news = CSVTranslator.get_csv_row(csv_src, secondary_index)
						classified_index.append(index)

						data.append(similar_index)
						data.append(secondary_news[src_column_index])
						data.append(secondary_news[title_column_index])
						data.append(secondary_news[article_column_index])
						data.append(secondary_news[label_column_index])
						sim_writer.writerow(data)
				else:
					data = []
					main_news = CSVTranslator.get_csv_row(csv_src, main_index)

					data.append(main_news[src_column_index])
					data.append(main_news[title_column_index])
					data.append(main_news[article_column_index])
					data.append(main_news[label_column_index])
					uni_writer.writerow(data)
