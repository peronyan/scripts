#!/usr/bin/env python
# -*- coding: utf-8 -*-
from multiprocessing import Process,Pool
import sys,re,os
import urllib,urllib2

PROC = 12
SEARCH_NUM = 20
OUTPUT_PATH = "./output/"

def checkBracket(code):
	global list_index
	global javaCodes
	methodPattern = re.compile(r'[(].*?[)];')
	inBracketPattern = re.compile(r'[(].*?[)]')
	intenBracketPattern = re.compile(r'[(].*[(].*?[)].*?[)]')
	match1 = True
	#bracketFlag = False
	while(match1):
		match1= inBracketPattern.search(code)
		match2= intenBracketPattern.search(code)
		#match3 = methodPattern.search(code)
		if match2:
			replaceText = match2.group()

			#両端の括弧を外す
			text = replaceText[:-1]
			text = text[1:]
			argumentList = text.split(',')
			#print argumentList
			for argument in argumentList:
				period = argument.split('.')
				for p in period:
					p = p.strip()
					#print p
				#引数の中からメソッドでないものを消す
					if not p.endswith(")") and not p.endswith(");"):
						continue
					checkBracket(p)
			code = code.replace(replaceText,'')
			#match1 = False
		if match1:
			#bracketFlag = True
			replaceText = match1.group()
			#print replaceText
			#print replaceText
			code = code.replace(replaceText,'')
				#print code
		else:
			match1 = False
	#if bracketFlag:
	appendText = code
	javaCodes[list_index].append(appendText)




def main():
	inputJavaCode = sys.argv[1]
	global javaCodes
	global list_index
	javaCodes = [[],[],[],[],[],[],[],[]]
	list_index = 0
	methodPattern = re.compile(r'[(].*[)];')
	for code in open(inputJavaCode):
		code = code.strip()
		if not code:
			continue
		#elif len(code) <= 3:
		#	continue
		if code.find("}") > -1:
			#print code
			list_index -= 1
			#print list_index
		if code.find("{") > -1:
			#print code
			list_index += 1
			#print list_index
				
		matchedList = methodPattern.findall(code)
		if len(matchedList) <= 0:
			#if code.find("protected") <= -1 and code.find("public") <= -1:
			if code.find("class") > -1:
				if code.find("extends") > -1:
					code = code.split("extends")[-1]
					code = code.strip()
					code = code.split(" ")[0]
					if code.find("<") > -1:
						code = code.split("<")[0]
					className = "new " + code
				else:
					className = "new " + " Object"
				print list_index
				javaCodes[list_index].append(className)

			#print "no match"
			continue

		#=の一番後ろ側だけに絞る
		code = code.split("=")[-1]
		#super delete
		#code = code.replace('super.','')
		#code = code.replace('this.','')
		#method name
		print code
		checkBracket(code)

	writeList = []
	oFile = open('output.txt','w')
	for code_list in javaCodes:
		for code in code_list:
			code = code.strip()
			code = code.replace(';','')
			code = code.split('.')[-1]
			code = code.strip("(")
			code = code.strip(")")
			if not code:
				continue
			if len(code) <= 2:
				continue
			if code.find("{") > -1:
				code = code.split(" ")[-2]
			if code.startswith("new "):
				code = code.lstrip("new ")
				code = code + ";-><init>"
			#continue
			else:
				code = "->" + code
			oFile.write(code)
			oFile.write(os.linesep)
			#writeList.append(code)
	
	#for text in reversed(writeList):
	#	oFile.write(text)
	#	oFile.write(os.linesep)
			#writeListoFile.write(os.linesep)
	oFile.close()



if __name__ == '__main__':
	main()
