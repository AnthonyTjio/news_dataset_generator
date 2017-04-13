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
	def rotate_file(cls, main_dir, temp_dir):
		"""
			Rotate temp file with main file

			Args:
				main_dir(str): Location of main file
				temp_dir(str): Location of temporary file
		"""
		os.remove(main_dir)
		copyfile(temp_dir, main_dir)
		os.remove(temp_dir)

	@classmethod
	def remove_extra_spaces(cls, txt):
		return re.sub("\s+", " ", txt).strip()


