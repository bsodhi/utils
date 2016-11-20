#!/usr/bin/python
'''
This short function reports duplicate links if found in a supplied HTML file.
'''
from bs4 import BeautifulSoup as BS
import sys

def find_duplicate_links(in_file):
	'''
	
	'''
	links = []
	soup = BS(open(in_file), "html.parser")
	found = False
	for link in soup.find_all('a'):
		if link in links:
			print "Found duplicate: "+str(link)
			found = True
		else:
			links.append(link)
	if not found:
		print "No duplicate links found."

# Main
if len(sys.argv) != 2:
	print "Please supply the input html file."
else:
	print "Checking duplicate links in: "+str(sys.argv[1])
	find_duplicate_links(sys.argv[1])

