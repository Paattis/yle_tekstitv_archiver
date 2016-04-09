import requests
import urllib
import json
import os
import datetime
import time
import random

firstPage = 100
lastPage = 899
maxSubPages = 9
subPageNums = ["0"+str(i) for i in range(1,maxSubPages+1)]
print(subPageNums)
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
		return False

	#page or subpage doesn't exist
	if r.status_code != 200:
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
	except:
		return False

for pageNum in range(firstPage,lastPage+1):
	for subPageNum in subPageNums:
		print(subPageNum)
		if getPicture(pageNum,basePath,subPageNum):
			print("Page %i subpage %s successfully saved" % (pageNum,subPageNum))
		time.sleep(random.randint(1,5))





