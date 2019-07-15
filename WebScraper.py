import os
import re
import bs4
import requests
from sys import *
from urllib.parse import urlparse
from urllib.request import urlopen
def is_downloadable(url):
	h=requests.head(url,allow_redirects=True)
	header=h.headers
	content_type=header.get('content-type')
	
	if 'text' in content_type.lower():
		return False
	if 'html' in content_type.lower():
		return False
	return True

def get_filename_from_cd(cd):
	a=urlparse(cd)
	return os.path.basename(a.path)

def MarvellousDownload(url):
	url="http:"+url
	allowed=is_downloadable(url)
	if allowed:
		try:
			res=requests.get(url,allow_redirects=True)
			res.raise_for_status()
			filename=get_filename_from_cd(url)
			fd=open(filename,"wb")

			for buffer in res.iter_content(1024):
				fd.write(buffer)

			fd.close()
			return True
		except Exception as e:
			print(e)
			return False

def MarvellousWebScrapper(url):
	try:
		connection=urlopen(url)
		raw_html=connection.read()
		connection.close()
		page_soup=bs4.BeautifulSoup(raw_html,"html.parser")


		container=page_soup.findAll("div",{"class":"item-container"})

		for elements in container:
			ret=MarvellousDownload(elements.a.img['data-src'])
			if ret==False:
				break
		return ret

	except Exception as e:
		print(e)
		return False
def main():
	print("application name",argv[0])
	if len(argv)==2:
		if(argv[1]=="-h") or (argv[1]=="-H"):
			print("script used to download any file")
			exit()
		if(argv[1]=="-u") or (argv[1]=="-U"):
			print("usage: applnname path_of_directory extension")
			exit()
	url=  "https://www.newegg.com/Video-Cards-Video-Devices/Category/ID-38?Tpk=video%20card"
	try:
		bret=MarvellousWebScrapper(url)
		if bret==True:
			print("files downloaded successfully")
		else:
			print("files not downloaded successfully")
	except Exception as e:
		print (e)
		print("failed to download")

if __name__=="__main__":
	main()
