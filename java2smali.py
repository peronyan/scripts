#!/usr/bin/env python
# -*- coding: utf-8 -*-
from multiprocessing import Process,Pool
import sys
import urllib,urllib2

PROC = 12
SEARCH_NUM = 20
OUTPUT_PATH = "./output/"

def main():
	inputJavaCode = sys.argv[1]
	javaCodes = []
	for code in open(inputJavaCode):
		code = code.strip()
		if not code:
			continue
		javaCodes.append(code)

	for code in javaCodes:
		print code



if __name__ == '__main__':
	main()
