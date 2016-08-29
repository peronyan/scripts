#!/usr/bin/env python
# -*- coding: utf-8 -*-
from multiprocessing import Process,Pool
import sys,re,os
import urllib,urllib2

PROC = 12
SEARCH_NUM = 20
OUTPUT_PATH = "./output/"

def checkBracket(code):
	global javaCodes
	inBracketPattern = re.compile(r'[(].*?[)]')
	intenBracketPattern = re.compile(r'[(].*[(].*[)].*[)]')
	match1 = True
	while(match1):
		match1= inBracketPattern.search(code)
		match2= intenBracketPattern.search(code)
		if match2:
			replaceText = match2.group()

			#両端の括弧を外す
			text = replaceText[:-1]
			text = text[1:]
			argumentList = text.split(',')
			for argument in argumentList:
				argu = argument.split('.')
				for arg in argu:
					arg = arg.strip()
				#引数の中からメソッドでないものを消す
					if arg.find("(") == -1 and arg.find(")") == -1:
						continue
					checkBracket(arg)
			code = code.replace(replaceText,'')
			#match1 = False
		if match1:
			replaceText = match1.group()
			code = code.replace(replaceText,'')
				#print code
		else:
			match1 = False

	javaCodes.append(code)




def main():
	inputJavaCode = sys.argv[1]
	global javaCodes
	javaCodes = []
	methodPattern = re.compile(r'[(].*[)];')
	for code in open(inputJavaCode):
		code = code.strip()
		if not code:
			continue
		elif len(code) <= 3:
			continue
		matchedList = methodPattern.findall(code)
		if len(matchedList) <= 0:
			#print "no match"
			continue

		#=の一番後ろ側だけに絞る
		code = code.split("=")[-1]
		#super delete
		#code = code.replace('super.','')
		#code = code.replace('this.','')
		#method name
		checkBracket(code)



	oFile = open('output.txt','w')
	for code in javaCodes:
		code = code.strip()

		code = code.replace(';','')
		code = code.split('.')[-1]
		code = code.strip("(")
		code = code.strip(")")
		if code.startswith("new"):
			continue
		if not code:
			continue
		oFile.write("->")
		oFile.write(code)
		oFile.write(os.linesep)
	oFile.close()



if __name__ == '__main__':
	main()
