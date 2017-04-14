import json
import os

from lib.grabber import Grabber
from lib.scanner import Scanner
from lib.similarity_checker import SimilarityChecker
from lib.CSVEditor import CSVEditor
from lib.CSVTranslator import CSVTranslator

class Driver:

	def ensure_dependencies():
		default_link_dir = "./links"
		if not os.path.exists(default_link_dir):
			os.makedirs(default_link_dir)

		default_moderation_dir = "./moderation"
		if not os.path.exists(default_moderation_dir):
			os.makedirs(default_moderation_dir)

		default_config_dir = "./conf.json"
		if not os.path.isfile(default_config_dir):
			open(default_config_dir, 'w')

		default_csv_dir = './data.csv'
		if not os.path.isfile(default_csv_dir):
			open(default_csv_dir, 'w')

	ensure_dependencies()

	@classmethod
	def crawl(cls, src='./links/', target='./links/', config='conf.json'):
		"""
			Initialize web crawler based on config

			Args:
				src(str, optional): folder directory containing initial starting points 
				target(str, optional): target folder directory to insert crawl product
				config(str, optional): config directory containing crawl details
		"""
		with open(config) as conf:
			sites = json.load(conf)
			for site in sites:
				source_directory = src+site["src"]+'.txt'
				regex = site["regex"]
				max_depth = site["iteration"]
				base_url = site["base_url"]

				if (max_depth>0):
					Grabber._crawl(source_directory, regex, max_depth, base_url=base_url)

	@classmethod
	def scan(cls, conf_dir='conf.json'):
		"""
			Retrieve title and article of URLs from text files based on config. The retrieved information will be
			inserted into data.csv by default along with the pre-determined label
		"""
		default_scanner_error_log_dir = "./scanner_error_log.csv"
		open(default_scanner_error_log_dir, 'w') # Will always overwrite existing file
		
		Scanner._extract_data()

	@classmethod
	def compare(cls, csv_src="data.csv", safe=False,
				src_column_index=0, title_column_index=1, article_column_index=2,
				label_column_index=3, dest_similar="./moderation/similar.csv",
				dest_unique="./moderation/unique.csv", similarity_threshold=0.75):

		if(safe):
			SimilarityChecker.safe_analyze(
				csv_src, src_column_index, title_column_index,
				article_column_index, label_column_index,
				dest_similar, dest_unique, similarity_threshold)
		else:			
			SimilarityChecker.analyze(
				csv_src, src_column_index, title_column_index,
				article_column_index, label_column_index,
				dest_similar, dest_unique, similarity_threshold)

	@classmethod
	def clean_csv(cls, csv_src, regex, columns_to_clean):
		CSVEditor.clean_column_with_regex(csv_src, regex, columns_to_clean)

	@classmethod
	def count_label(cls, csv_src, label_column_index):
		csvTranslator = CSVTranslator()
		csvTranslator.analyze_tag_distribution(csv_src, label_column_index)