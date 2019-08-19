import sys
import cv2 as cv
import requests
import os
import json
import urllib


# Post image get response
def upload_image(path, url):
	files = {'image': open(path,'rb')}
	response = requests.post(url, files=files)
	output = response.json()
	return output


# save image
def download_img(img_url,image_name, pth):
		print(img_url)
		try:
			urllib.request.urlretrieve(img_url,pth+image_name)
		except Exception as e:
			print(e)


output = upload_image(sys.argv[1], sys.argv[2])
download_img(output["image_link"], output["image_name"], "analyzed_images/")



