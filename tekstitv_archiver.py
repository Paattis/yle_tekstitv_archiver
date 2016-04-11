import requests
import urllib
import json
import os
import datetime
import time
import random

firstPage = 100
lastPage = 899
maxSubPages = 30

sleepTime = 5

subPageNums = list(map(lambda x: x if int(x) < 9 else x[1:],["0"+str(i) for i in range(1,maxSubPages+1)]))

date = datetime.datetime.today().strftime("%d_%m_%Y")
basePath ="./archived_pages/%s" % date

def getPicture(page,savePath,subPage="01",):
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
for pageNum in range(firstPage,lastPage+1):
	for subPageNum in subPageNums:
		print("Trying to save page %i subpage %s" % (pageNum,subPageNum))

		if getPicture(pageNum,basePath,subPageNum):
			print("Page %i subpage %s successfully saved" % (pageNum,subPageNum))
			savedPageCount += 1
			print("On page %i_%s out of %i possible pages, %i pages saved" % (pageNum,subPageNum,lastPage*maxSubPages,savedPageCount))

		time.sleep(sleepTime)





