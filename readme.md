# How to use News Dataset Generator:
### Basic Usage: **python3 main.py [arg] **

Possible Arguments:
- **crawl** : Crawl websites based on config file
- **scan** : Scan website links and retrieve title and article of the website based on the config file, later on these information
			 will be written into data.csv along with the predetermined tag
- **compare** : Create 2 csv files based on data.csv which will compare possible similar articles with different tag
- **bagging** : Perform bagging / bootstrap aggregation on the source csv file to multiply datasets