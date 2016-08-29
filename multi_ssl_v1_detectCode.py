#!/usr/bin/env python
# -*- coding: utf-8 -*-
import commands,sys,os,shlex,subprocess,re,datetime,locale
from multiprocessing import Process,Pool

proc = 12

APK_DIR = "../test_apk2/"
CHECK_SMALI_DIR = "../check_smali/"
TEMP_DIR = "../temp/"
OUTPUT_DIR = "./output/"

def findAllFiles(directory):
    for root, dirs, files in os.walk(directory):
		yield root
		for file in files:
			yield os.path.join(root, file)


def deleteWhiteSpace(text):
	text = text.strip()
	return text

def checkDeleteTargets(text):
	dlist =[".local",".locals",".line"]
	for dtext in dlist:
		if dtext in text:
			text = ""
			break
	return text

def checkMultipleLines(smali,text):
	tx = open(text,'r')
	text_lines = tx.readlines()
	tx.close()
	text_index = 0
	sl = open(smali,'r')
	smali_lines = sl.readlines()
	sl.close()
	getData = []
	for smali_line in smali_lines:
		smali_line = deleteWhiteSpace(smali_line)
		smali_line = checkDeleteTargets(smali_line)
		#skip no text
		if not smali_line:
			continue
		if deleteWhiteSpace(text_lines[text_index])in smali_line:
			text_index +=1
			if ".param" in smali_line:
				#print smali_line
				text = smali_line.strip()
				text = text.replace(',','')
				getData.append(text)
			if text_index +1 >= len(text_lines):
				getData.append(smali_lines[0].strip())
				return True,getData
		else:
			text_index = 0
			getData = []
	return False,getData

def checkSmali_Multi(apk,targetSmalis,codeSnippets):
	countNum = 0
	for smali in targetSmalis:
		for codeSnippet in codeSnippets:
			getData =[]
			flag,getData = checkMultipleLines(smali,codeSnippet)
			if flag:
				countNum += 1
				appName = apk.lstrip(APK_DIR)
				writeOutput(apk,smali,getData,codeSnippet,str(countNum))
	
	

def doApktool(apkPath):
	print "apktool:" + apkPath
	cmd = 'apktool d -q -f %s'%(apkPath)
	subprocess.call(shlex.split(cmd))

def checkTrue(line):
	line = line.split(",")[-1]
	flag = line.find('0x1')
	return flag

def getCheckSmaliPath():
	lists = []
	for file in findAllFiles(CHECK_SMALI_DIR):
		root,ext = os.path.splitext(str(file))
		if ext == ".txt":
			lists.append(str(file))
	return lists

def getAppSmaliPath(path):
	lists = []
	for file in findAllFiles(path):
		root,ext = os.path.splitext(str(file))
		if ext == ".smali":
			lists.append(str(file))
	return lists

def getApkPath():
	lists = []
	for file in findAllFiles(APK_DIR):
		root,ext = os.path.splitext(str(file))
		if ext == ".apk":
			lists.append(str(file))
	return lists

def deleteTmpFolder(path):
	cmd = 'rm -r %s'%(path)
	subprocess.call(shlex.split(cmd))

def writeOutput(apk,smali,getData,codeSnippet,countNum):
	global outfName
	outPath = OUTPUT_DIR + outfName+ "-output.csv"
	if not os.path.isdir(OUTPUT_DIR):
		cmd = 'mkdir %s'%(OUTPUT_DIR)
		subprocess.call(shlex.split(cmd))

		
	outPutFile = open(outPath,'a')
	dataText = ""
	#print getData
	for data in getData:
		dataText += data + ","
	apk = apk.lstrip(APK_DIR)
	smali = smali.lstrip("./")
	codeSnippet = codeSnippet.lstrip(CHECK_SMALI_DIR)
	codeSnippet = codeSnippet.strip()
	text = apk +","+smali+","+dataText+codeSnippet+","+countNum+os.linesep
	#text = text.replace(";",os.linesep)
	print text
	outPutFile.write(text)
	outPutFile.close()
	
def checkSmali(apk,targetSmalis,codeSnippets):
	countNum = 0
	for smali in targetSmalis:
		for codeSnippet in codeSnippets:
			checkSnippetNum = 0
			totalSnippetNum = 0
			for cCode in open(codeSnippet,'r'):
				regflag = 0
				totalSnippetNum += 1
				reg = cCode.split(",")[0]
				cCode = cCode.rstrip("¥n")
				cCode = cCode.strip()
				if reg == "regexp":
					regflag = 1
					cCode = cCode.lstrip("regexp,")
					cCode = cCode.rstrip("¥n")
					cCode = cCode.strip()
					checkText = re.compile(cCode)
				else:
					cCode = cCode.rstrip("¥n")
					cCode = cCode.strip()
					checkText = cCode
				line_list = []
				for line in open(smali,'r'):
					line_list.append(str(line))
					
				#with open(smali,'r') as smali_file:
				for index,cSmali in enumerate(line_list):

				#for cSmali in open(smali,'r'):
					cSmali = cSmali.rstrip("¥n")
					cSmali = cSmali.strip()
					if regflag:
						#print str(checkText)
						flag = checkText.match(cSmali)
					else:
						if checkText in cSmali:
							flag = 1
						else:
							flag = 0
					if flag:
						#print "aaaa"
						trueFlag =checkTrue(str(line_list[index-2]))
						if trueFlag:
							checkSnippetNum += 1
							#print "bbbb"
						break
			if checkSnippetNum >= totalSnippetNum:
				countNum += 1
				appName = apk.lstrip(APK_DIR)
				writeOutput(apk,smali,codeSnippet,str(countNum))

def doDecompile(apk,checkLists,index):
	print 'process id:' + str(os.getpid())
	#フォルダ名取得
	root,ext = os.path.splitext(apk)
	fName = root.split("/")[-1]
	doApktool(apk)
	smaliFName = str("./" + fName + "/smali/")
	smaliPathLists = getAppSmaliPath(smaliFName)
	checkSmali_Multi(apk,smaliPathLists,checkLists)
	deleteTmpFolder(fName)
	print "%s/%s"%(index+1,totalNum)

	
def argwrapper(args):
	return args[0](*args[1:])

if __name__ == "__main__":
	global outfName
	d = datetime.datetime.today()
	outfName = d.strftime("%Y-%m-%d-%H:%M:%S")
	doneNum = 0
	apkLists = getApkPath()
	print "APK Num:"+ str(len(apkLists))
	global totalNum
	totalNum = len(apkLists)
	checkLists = getCheckSmaliPath()	
	print "Check Num:"+ str(len(checkLists))
	#デコンパイルループ
	p = Pool()
	func_args = []
	for index,apk in enumerate(apkLists):
		func_args.append((doDecompile,apk,checkLists,index))
	p.map(argwrapper,func_args)
	

		#argsList = []
		#argsList.append(apk)
		#argsList.append(checkLists)
		#p.map(doDecompile,argsList)
		#job = Process(target=doDecompile,args=(apk,checkLists))
		#jobs.append(job)
		#job.start()
		#doneNum += 1
		#print "%s/%s"%(doneNum,totalNum)


	#[job.join() for job in jobs]
	
	#print "Finish!"

	
