import csv
import random
import numpy as np

class CSVTranslator:

	@classmethod
	def csv_to_list(self, src):
		"""
			Grabs csv file and return 2 dimension list

			Args:
				src(str): csv file location
		"""
		with open(src, 'r') as input:
			reader = csv.reader(input, delimiter=",")
			data_holder = []

			for index, row in enumerate(reader):
				data = []
				for column in row:
					data.append(column)

				data_holder.append(data)
				
			return data_holder

	@classmethod
	def get_csv_row(self, src, row_index):
		"""
			Grab csv row as list, use as alternative when csv_to_list exceed server memory
			
			Args:
				src(str): csv file location
				row_index(int): row to retrieve the data

			Return:
				data(list): List of data in a row
		"""
		with open(src, 'r') as input:
			reader = csv.reader(input, delimiter=",")

			for index, row in enumerate(reader):
				if (index==int(row_index)):
					data = []
					for column in row:
						data.append(column)

					return data

			return None

	@classmethod
	def get_csv_number_of_row(self, src):
		"""
			Retrieve number of row in csv file

			Args:
				src(str): csv file location

			Return:
				num_of_rows(int): Number of rows
		"""
		with open(src, 'r') as input:
			reader = csv.reader(input, delimiter=",")

			num_of_rows = 0
			for row in reader:
				num_of_rows += 1

			return num_of_rows

	@classmethod
	def analyze_tag_distribution(self, csv_src, label_column_index):
		"""
			Grabs csv file and analyze tag distribution

			Args:
				src(str): csv file location
				label_column_index(int): label column position in csv file
		"""
		rows = self.csv_to_list(csv_src)
		labels = {}
		for row in rows:
			label = row[int(label_column_index)]
			if(label not in labels):
				labels[label] = 0
			labels[label] +=1

		for label in labels.keys():
			print(str(label)+" is "+str(labels[label]))

	@classmethod
	def split_data(self, src_list, ratio):
		"""
			Split a list into 2 list randomly based on percentage

			Args:
				src_list(list): source list to be splitted randomly
				ratio(int, 0 <= ratio <= 1): ratio of first product list

			Returns:
				list1(list): Splitted list which is (percentage) of source list
				list2(list): Splitted list which is (1-percentage) of source list
		"""
		if(ratio < 0 or ratio > 1):
			raise ValueError("Ratio should be between 0 and 1")

		random.shuffle(src_list)
		seperator = int(len(np_data)*ratio)

		list1 = np.array(src_list[:seperator]) 
		list2 = np.array(src_list[seperator:])

		return list1, list2