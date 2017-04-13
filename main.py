# -*- coding: utf-8 -*-
import sys
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

		Driver.clean_csv(src, regex, columns)
	else:
		"Require at least 3 parameters with format Source(Optional) - Regex - Column(s) "
