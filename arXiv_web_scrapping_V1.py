'''
About: This script scrapes the ArXiv for recent and old papers. We are only considering Physics papers in the last 5 year.
Author: Ramit Dey and Sayantan Auddy
Created : 4 June 2019

Input: The category 
	   The year range for which the data is needed

Modified: 

'''

## Impprting the required packages for web scrapping
from bs4 import BeautifulSoup
import requests 
import csv


category = 'gr-qc' ## specify the category that for the paper. For example gr-qc

start_year = 18
end_year = 19 

for year_number in range(start_year,end_year): ## the last year in not included
	year = str(year_number)
	print("Gathering data for the year: ",year)

	## creating the output .csv file in the same working directory

	output_filename = 'Arviv_GRQC_Title_' + year +'.csv'
	csv_file = open(output_filename,'w')
	csv_writer = csv.writer(csv_file)
	csv_writer.writerow(['Title'])


	skip_list = ['0','2000','4000']

	## for shorter list just use '0'
	# skip_list = ['0']
	for skip in skip_list: ## this loops over next page specified by the skip valuerange in ArXiv .
		

		'''Requesting the required webpage'''
		source=requests.get('https://arxiv.org/list/'+ category +'/'+ year +'?skip='+ skip +'&show=2000').text

		'''souping the html'''
		soup=BeautifulSoup(source,'lxml')

		body=soup.find('div',id='dlpage')



		'''poinitng at the dl tag which contains the list of all the papers'''
		content=body.find('dl')
		# print(content.prettify)

		title = content.find('div',class_='list-title mathjax')
		# print(title.text)
		# article_title =title.text.split(':')
		


		##extracting the titles from each row within the dl tag where the title is 
		## given the class, list-title mathjax 	

		for title in content.find_all('div',class_='list-title mathjax'):
			article_title =title.text.split(':') ######### TO split the title line from ':'	
			
			csv_writer.writerow([":".join(article_title[1:])]) ### To get the title text only 

	csv_file.close()
	print("The CSV file is ready ")
