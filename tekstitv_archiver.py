import requests
import urllib
import json
import os
import datetime
import time
import random
import sys

firstPage = 100
lastPage = 899
maxSubPages = 30

sleepTime = 5

if len(sys.argv) > 1:
	useKnown = True if "useknown" in sys.argv else False
	saveNew = True if "savenew" in sys.argv else False
else:
	useKnown = False
	saveNew = False
print(useKnown,saveNew)

knownPages = {}
page = 0
subPage = ""

#read file that contains list of known pages to save time
try:
	with open("knownpages.txt","r") as f:
		content = f.read()
		if len(content) != 0:
			content = content.split(",")
			for line in content:
				line = line.split("_")
				pageNum = int(line[0])
				subPage = line[1].strip("\n")
				if pageNum in knownPages.keys():
					knownPages[pageNum].append(subPage)
				else:
					knownPages[pageNum] = []
					knownPages[pageNum].append(subPage)
		else:
			print("knownpages.txt is empty")

	totalPagesToSave = sum([len(v) for v in knownPages.values()])
except IOError:
	#no file found
	useKnown = False
	#create new file 
	f = open("knownpages.txt","w")
	f.close()

subPageNums = list(map(lambda x: x if int(x) < 10 else x[1:],["0"+str(i) for i in range(1,maxSubPages+1)]))

date = datetime.datetime.today().strftime("%d_%m_%Y")
basePath ="./archived_pages/%s" % date

def getPicture(page,savePath,subPage="01"):
	userAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0"
	headers = {"User-Agent":userAgent}

	try:
		pictureUrl = "http://www.yle.fi/tekstitv/images/P%i_%s.gif" % (page,subPage)
		print(pictureUrl)
		r = requests.get(pictureUrl,headers=headers);
	except:
		print("save failed")
		return False

	#page or subpage doesn't exist
	if r.status_code != 200:
		print("save failed")
		return False

	
	#create the path	
	basePath = savePath+"/pictures"
	dirName = basePath
	
	#check if the folder already exists and create it if it doesn't
	if not os.path.exists(dirName):
   		os.makedirs(dirName)

   	#get the picture from the url
	try:
		pictureSavePath = basePath+"/"+pictureUrl.split("/")[-1]
		pictureSavePath = os.path.realpath(pictureSavePath)
		urllib.request.urlretrieve(pictureUrl,pictureSavePath)
		return True
	except AttributeError:
		#python 2.7
		try:
			pictureSavePath = basePath+"/"+pictureUrl.split("/")[-1]
			pictureSavePath = os.path.realpath(pictureSavePath)
			urllib.urlretrieve(pictureUrl,pictureSavePath)
			return True
		except:
			return False
		

savedPageCount = 0
pageCount = 0
newPages = []
firstItem = True
if not useKnown:
	for pageNum in range(firstPage,lastPage+1):
		for subPageNum in subPageNums:
			print("Trying to save page %i subpage %s" % (pageNum,subPageNum))

			if getPicture(pageNum,basePath,subPageNum):
				print("Page %i subpage %s successfully saved" % (pageNum,subPageNum))
				savedPageCount += 1
				print("On page %i_%s out of %i possible pages, %i pages saved" % (pageNum,subPageNum,lastPage*maxSubPages,savedPageCount))

				if saveNew:
					
					try:
						if len(knownPages) == 0:
							firstItem = True
						else:
							firstItem = False;
						if pageNum not in knownPages.keys():
							print("adding new item to dict")
							knownPages[pageNum] = []
						if subPageNum not in knownPages[pageNum]:
							print("New page discovered, saving")
							pageString = "%i_%s" % (pageNum,subPageNum)
							newPages.append(pageString)

							#save found page
							with open("knownpages.txt", "ab") as knownPagesFile:
								if firstItem:
									knownPagesFile.write(pageString)
								else:
									knownPagesFile.write(","+pageString)
					except KeyError:
						print("Knownpages related keyerror")
						pass
					

			time.sleep(sleepTime)



else:
	print("Using known pages")
	for page,subPages in knownPages.iteritems():
		print(page)
		for subPageNum in subPages:
			print("Trying to save page %i subpage %s" % (page,subPageNum))
			if getPicture(page,basePath,subPageNum):
				print("Page %i subpage %s successfully saved" % (page,subPageNum))
				savedPageCount += 1

			pageCount += 1
			print("%i/%i pages (%i successful)" % (pageCount,totalPagesToSave,savedPageCount))
			
			time.sleep(sleepTime)





