import numpy as np

class ListManipulator:

	@classmethod
	def xor_list(cls, list_1, list_2):
		"""
			Perform xor operation on 2 list

			Args:
				list_1(list): First List
				list_2(list): Second List

			Return:
				refined_list_1(list): XORed list1
				refined_list_2(list): XORed list2
		"""
		combined_list = list(set(list_1) & set(list_2))
		refined_list_1 = [x for x in list_1 if x not in combined_list]
		refined_list_2 = [x for x in list_2 if x not in combined_list]

		return refined_list_1, refined_list_2