# -*- coding: utf-8 -*-
import sys
import getopt
from driver import Driver

if (len(sys.argv) > 1):
	command = sys.argv[1].lower()
else:
	readme_src= open("readme.md", 'r')
	readline_src = readme_src.readlines()
	for line in readline_src:
		print(line)

if(command == "crawl"):
	Driver.crawl()

elif(command == "scan"):
	Driver.scan()

elif(command == "compare"):
	opts, args = getopt.getopt(sys.argv[2:], "Ss:", ["safe=", "source="])
	if(len(sys.argv)>2):
		safe = False
		src = None
		for opt, arg in opts:
			if opt in ("-S", "--safe"):
				safe = arg
			elif opt in ("-s", "source"):
				src = arg

		if (src is None):
			src = "./data.csv"
		if (safe):
			Driver.compare(csv_src=src, safe=True)
		else:
			Driver.compare(csv_src=src)

elif(command == "compare"):
	if (len(sys.argv) == 3):
		src = sys.argv[2].lower()
		Driver.compare(csv_src=src)
	else:
		Driver.compare()

elif(command == "clean"):
	if (len(sys.argv) >=5):
		src = sys.argv[2].lower()
		# src = "data.csv"
		regex = sys.argv[3]
		columns = []

		for i in sys.argv[4:]:
			columns.append(i)	
		print
		Driver.clean_csv(src, regex, columns)
	else:
		"Require at least 3 parameters with format Source(Optional) - Regex - Column(s) "

elif(command == "count"):
	if (len(sys.argv) == 4):
		src = sys.argv[2].lower()
		column = sys.argv[3]
		Driver.count_label(src, column)

