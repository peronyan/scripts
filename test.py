#!/usr/bin/env python
# -*- coding: utf-8 -*-
from google import search
from multiprocessing import Process,Pool
import sys
import urllib,urllib2
from bs4 import BeautifulSoup


PROC = 12
SEARCH_NUM = 20
OUTPUT_PATH = "./output/"

def googleSearch(word):
	#outFileName = word.replace("/","-")+ ".csv"
	#outFile = open(OUTPUT_PATH+outFileName,'w')
	for url in search(word, stop = SEARCH_NUM,lang = "en"):
		print url
		#outFile.write(str(url))
	#outFile.close()

def main():
	num = 0
	#p = Pool(PROC)
	for word in open(sys.argv[1]):
		num += 1
		word = word.strip()
		word = word.split(" ")[1]
		print str(num) +":"+ word
		googleSearch(word)
		#p.map(googleSearch,word)



if __name__ == '__main__':
	main()
