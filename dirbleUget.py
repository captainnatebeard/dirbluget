#!/usr/bin/python3

import os
import sys
import urllib.request

dirListList = []
blorp = 0
newLines = []
dirbOut = []

def main():
	global blorp
	global newLines
	if len(sys.argv) < 2 or len(sys.argv) > 4:
		print ("Usage: " + sys.argv[0] + " <url address> <wordlist> <outfile>")
	else:
		dirList = []
		if len(sys.argv) > 2:
			wordlist = sys.argv[2]
		else:
			wordlist = "/usr/share/wordlists/dirb/small.txt"
		if len(sys.argv) > 3:
			outfile = sys.argv[3]
		else:
			outfile = "/tmp/outfile"

		with open(wordlist, "r") as wl:
			lines = wl.readlines()
		if blorp == 0:
			for line in lines:
				line = line.replace('\n', '')
				if line != "":
					dirList.append(line)
					newLines.append(line)
			dirListList.append(dirList)
			os.system("mkdir " + outfile)
			blorp += 1
	while len(dirListList) > 0:
		dirscan(dirListList.pop(0), sys.argv[1], newLines, outfile)

def request(url, outfile, saveFile, isDir):
	try:
		call = urllib.request.Request(url)
		response = urllib.request.urlopen(call)
		html = str(response.read())
		responseCode = response.getcode()
		if responseCode < 400:
			print (url + " : status " + str(responseCode))
			newSaveFile = outfile + "/" + saveFile
			print (newSaveFile)
			if isDir:
				os.system("mkdir " + newSaveFile)
			else:
				with open(newSaveFile, 'a') as file:
					file.write(html)
					print (html)
			return True
	except Exception as f:
		#print (f)
		return False

def dirscan(dirList, url, wordlist, outfile):
	newDirList = []
	extList = [".html", ".php", ".asp", ".txt", ".aspx", ".js", ".htm", ".css"]
	for dir in dirList:
		for ext in extList:
			fileUrl = url + "/" + dir + ext
			statusFileOk = request(fileUrl, outfile, dir + ext, False)
		dirUrl = url + "/" + dir
		statusDirOk = request(dirUrl, outfile, dir, True)
		if statusDirOk and dir != "server-status":
			for i in wordlist:
				newDir = dir + "/" + i
				newDirList.append(newDir)
			dirListList.append(newDirList)
	main()



main()
