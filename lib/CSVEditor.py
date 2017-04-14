import csv
import re
import os
from shutil import copyfile

from .CSVTranslator import CSVTranslator

class CSVEditor:
	@classmethod
	def clean_column_with_regex(cls, csv_dir, regex, columns_to_clean=None, clean_extra_spaces=True):
		"""
			Remove matching regex from csv file column

			Args:
				csv_dir(str): Location of csv file
				regex(str): Regex to be removed from the column
				column_to_clean(list(int), optional): CSV column to be cleaned, if left blank will clean whole column
				clean_extra_spaces(bool, Optional): Should it clean extra spaces as well?
		"""
		temp_dir = csv_dir[:-4]+"_temp.csv"

		rows = CSVTranslator.csv_to_list(csv_dir)
		if (columns_to_clean is None):
			columns_to_clean = range(len(rows[0]))

		with open(temp_dir, "w") as output:
			csv_writer = csv.writer(output, delimiter=",")
			for row in rows:
				for i in columns_to_clean:
					i = int(i)
					row[i] = re.sub(regex, "", row[i])
					row[i] = cls.remove_extra_spaces(row[i])

				data = []
				for info in row:
					data.append(info)

				csv_writer.writerow(data)

		cls.rotate_file(csv_dir, temp_dir)

	@classmethod
	def safe_clean_column_with_regex(cls, csv_src, regex, columns_to_clean=None, clean_extra_spaces=True):
		"""
			Remove matching regex from csv file column safely, use as alternative when csv_to_list throw memory error

			Args:
				csv_src(str): Location of csv file
				regex(str): Regex to be removed from the column
				column_to_clean(list(int), optional): CSV column to be cleaned, if left blank will clean whole column
				clean_extra_spaces(bool, Optional): Should it clean extra spaces as well?
		"""
		temp_dir = csv_src[:-4]+"_temp.csv"

		row_count = CSVTranslator.get_csv_number_of_row(csv_src)

		with open(csv_src, 'r') as input_data, open(temp_dir, "w") as output_data:
			csv_reader = csv.reader(input_data, delimiter=',')
			csv_writer = csv.writer(output_data, delimiter=",")

			for row_index, row in enumerate(csv_reader):
				data = []
				print("Cleaning index #"+str(row_index))

				for column_index, column in enumerate(row):
					if column_index in columns_to_clean or not columns_to_clean:
						column_data = re.sub(regex, "", column)
						data.append(column_data)
					else:
						data.append(column)

				csv_writer.writerow(data)

		cls.rotate_file(csv_src, temp_dir)

	@classmethod
	def remove_under_threshold_columns(cls, csv_src, columns_to_clean, min_length):
		"""
			Remove rows which column length is lower than minimum length

			Args:
				csv_src(str): Location of csv file
				columns_to_clean(list(int)): List of columns to be clean, if left blank will check whole column
				min_length(int): Length threshold of allowable column length
		"""
		temp_dir = csv_src[:-4]+"_temp.csv"
		min_length = int(min_length)

		row_count = CSVTranslator.get_csv_number_of_row(csv_src)

		with open(csv_src, 'r') as input_data, open(temp_dir, "w") as output_data:
			csv_reader = csv.reader(input_data, delimiter=',')
			csv_writer = csv.writer(output_data, delimiter=",")

			for row_index, row in enumerate(csv_reader):
				data = []
				ok = True
				print("Checking threshold on index #"+str(row_index))
				for column_index, column in enumerate(row):
					try:
						if column_index in columns_to_clean or not columns_to_clean:
							if (len(column) < min_length):
								ok = False
								break
							else:
								data.append(column)
						else:
							data.append(column)
					except Exception as error:
						print(str(error)+" has occured...")

				if (ok):
					csv_writer.writerow(data)

		cls.rotate_file(csv_src, temp_dir)

	@classmethod
	def remove_duplicate_columns(cls, csv_src, columns_to_clean):
		"""
			Remove row which column is duplicated with other row

			Args:
				csv_src(str): Location of csv file
				columns_to_clean(list(int)): List of columns to be clean, if left blank will check whole column
		"""
		temp_dir = csv_src[:-4]+"_temp.csv"

		row_count = CSVTranslator.get_csv_number_of_row(csv_src)

		with open(csv_src, 'r') as input_data, open(csv_src, 'r') as temp_data, \
			 open(temp_dir, "w") as output_data:

			csv_reader = csv.reader(input_data, delimiter=',')
			temp_csv_reader = csv.reader(temp_data, delimiter=',')
			csv_writer = csv.writer(output_data, delimiter=",")

			previous_index = -1
			blacklisted_indexes = []
			for main_row_index, main_row in enumerate(csv_reader):
				if (main_row_index == previous_index or main_row_index in blacklisted_indexes):
					continue

				data = []
				print("Cleaning duplicates of index #"+str(main_row_index))

				for main_column_index, main_column in enumerate(main_row):
					data.append(main_column)

				csv_writer.writerow(data)

				temp_data.seek(0)
				for secondary_row_index, secondary_row in enumerate(temp_csv_reader):
					if(secondary_row_index <= main_row_index or secondary_row_index in blacklisted_indexes):
						continue

					for secondary_column_index, secondary_column in enumerate(secondary_row):
						if (secondary_column_index in columns_to_clean or not columns_to_clean):
							try:
								text1 = data[secondary_column_index]
								text2 = secondary_column
								if(text1==text2):
									print("Similar Index: "+str(secondary_row_index))
									blacklisted_indexes.append(secondary_row_index)
									break
							except Exception as error:
								print(str(error)+" has occured")			
				
		cls.rotate_file(csv_src, temp_dir)

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

	@classmethod
	def remove_extra_spaces(cls, txt):
		return re.sub("\s+", " ", txt).strip()


