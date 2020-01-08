#!python -3


import re
import os
import sys
from datetime import datetime
from urllib.parse import unquote



"""
					Author: @n0crush
					https://github.com/n0crush

					Script
					Download video from facebook use commandline interface.

												----01/09/2020 00:00----
				"""


try:
	import requests
except:
	os.system('pip install requests')
	print('[WARNING] Error occured when try import Package.')
	sys.exit('[ RUN AGAIN ]')

def getLink(url):
	
	url = "https://m"+url[11:]				# redirect to mobile interface

	res = requests.get(url, timeout=10, allow_redirects=True)

	if res.status_code!=200:
		sys.exit("[!] Invalid URL. Check again!")

	if (re.findall("/video_redirect/", res.text))==[]:
		sys.exit("[!] Video not found.")

	text_data = res.text
	url_decoded = unquote(text_data.split("?src=")[1].split("\"")[0])			# decode url

	return url_decoded



def downloadVideo(url, folder, video_name):

	if not (os.path.exists(folder)):
		folder = os.path.join(os.path.expanduser('~'), "Downloads")
		print("[!] Using default folder: ", folder)

	for i in "\\/:*?\"<>|":
		if i in video_name:
			video_name = 'temp.mp4'
			print("[!] Video name invalid. Used 'temp' as name.")
			break

	if ".mp4" not in video_name:		# prevent error when naming file
		video_name += ".mp4"
	path = folder+"\\"+video_name

	res = requests.get(url, timeout=10, allow_redirects=False)

	with open(path, 'wb') as data:
		data.write(res.content)

	print("[OK] Download completed!")


def usage():
	print("-"*25)
	print("Use: python fbdwn.py \"url\" \"folder\" \"name\"")
	print("\t--url	  :		url taken in video by right click.")
	print("\t--folder :		absolute path, if omited use default path.")
	print("\t--name   :		name.mp4 or just name.")
	print("-"*25)
	sys.exit("Error")


def main():

	if len(sys.argv)!=4:
		usage()

	url = sys.argv[1]
	folder = sys.argv[2]
	name = sys.argv[3]

	s = datetime.now()

	origin_link = getLink(url)
	downloadVideo(origin_link, folder, name)

	e = datetime.now()
	time_delta = (e-s)

	print("Finished %d.%ds" %(time_delta.seconds, time_delta.microseconds))


#
if __name__ == '__main__':
	main()
#



