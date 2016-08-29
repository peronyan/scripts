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
	inputJavaCode = sys.argv[1]




if __name__ == '__main__':
	main()
