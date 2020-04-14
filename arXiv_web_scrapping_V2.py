'''
About: This script scrapes the ArXiv for recent and old papers. We are only considering Physics papers in the last 5 years.
Author: Sayantan Auddy 
Created : 23 June 2019

Input: The category 
	   The year range for which the data is needed

Output : Year-wise csv with the data for the paper title and authors
		One global csv with the data for the published year, title and authors

Modified: 29 june to correct for the over counting is case the number of paper is 
		page was less than the skip number

'''

## Impprting the required packages for web scrapping
from bs4 import BeautifulSoup
import requests 
import csv
import numpy as np
import os.path

## Input from the user: 

category = 'gr-qc' ## specify the category of research paper. For example gr-qc
# category = 'astro-ph' ## specify the category of research paper. For example astro-ph

start_year = 2018
end_year = 2019



## Output Directory 

current_directory = os.getcwd() 
output_path = './output_'+ category
output_folder= current_directory + '/output_'+ category

try:  
    os.makedirs(output_folder)
except OSError:  
    pass
else:  
    print ("Successfully created the directory %s", output_folder)





## a csv file with data for all year
global_output_filename = os.path.join(output_path, 'Arviv_'+ category +'_Title_' + str(start_year) +'-'+ str(end_year) +'.csv')
csv_file_global = open(global_output_filename,'w')
csv_writer_global = csv.writer(csv_file_global)
csv_writer_global.writerow(['Year','Title','Authors'])
# csv_writer_global.writerow(['Year','Title'])



for year_number in range(start_year,end_year+1): ## To include the last year
	year_num = str(year_number)
	year = year_num[2:]
	print("Gathering data for the year: ",year_num)

	
	
	## creating the output .csv file in the same working directory
	output_filename = os.path.join(output_path,'Arviv_'+ category +'_Title_' + year +'.csv')
	csv_file = open(output_filename,'w')
	csv_writer = csv.writer(csv_file)
	csv_writer.writerow(['Title','Authors'])


	## The highest skip values 
	skip_list = ['0','2000','4000','6000','8000','10000','12000','14000','16000']


	## for shorter list just use '0'
	# skip_list = ['0']
	number_of_papers = 0
	for skip in skip_list: ## this loops over next page specified by the skip valuerange in ArXiv .
		# print(np.int(skip))
		if np.int(skip) == number_of_papers or number_of_papers == np.int(skip)-1:
			
			'''Requesting the required webpage'''
			source=requests.get('https://arxiv.org/list/'+ category +'/'+ year +'?skip='+ skip +'&show=2000').text
			
			'''souping the html'''
			soup=BeautifulSoup(source,'lxml')

			body=soup.find('div',id='dlpage')


			'''poinitng at the dl tag which contains the list of all the papers'''
			content=body.find('dl')
			# print(content.prettify)

			## Getting the Title, Author and the number of item from the arXiv as example

			# title = content.find('div',class_='list-title mathjax')
			# authors = content.find('div',class_='list-authors')
			# item=content.find('dt')
			# print(item.text.split(' ')[0])
			
			
		    ## extracting the titles from each row within the dl tag where the title is 
			## given the class, list-title mathjax 	
			## Also extracting the authors list corresponding to the given title
			
		
			for title, authors  in zip(content.find_all('div',class_='list-title mathjax'),content.find_all('div',class_='list-authors'),):
				number_of_papers = number_of_papers+1
				article_title =title.text.split(':') ######### TO split the title line from ':'	
				article_authors = authors.text.split(':')
				# print(article_authors[1].replace('\n',''))
				csv_writer.writerow([":".join(article_title[1:]),article_authors[1].replace('\n','')]) ### To get the title text only and not the word "Title" and only the authors
				csv_writer_global.writerow([str(year_num),":".join(article_title[1:]),article_authors[1].replace('\n','')]) ### To get data for all the years
				# csv_writer_global.writerow([str(year_num),":".join(article_title[1:])])
	
	print("Total number of paper in the year %s" %year_num, "are %s" %number_of_papers )	
	csv_file.close()
	print("The CSV file is ready ")
csv_file_global.close()
print("The global CSV file is  also ready ")
