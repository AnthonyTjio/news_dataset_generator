import csv
import random

class CSVTranslator:

	@classmethod
	def csv_to_list(self, src):
		"""
			Grabs csv file and return 2 dimension list

			Args:
				src(str): csv file location
		"""
		with open(src, 'r') as input:
			reader = csv.reader(input)
			data_holder = []

			for row in reader:
				data = []
				for column in row:
					data.append(column)

				data_holder.append(data)

			return data_holder

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