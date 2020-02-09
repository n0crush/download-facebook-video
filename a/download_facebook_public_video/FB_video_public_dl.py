#! python -3


try:
	import requests
except:
	os.system('pip install requests')
	print('[WARNING] An Error occured when try to import "requests".')
	sys.exit('[ RUN AGAIN ]')

import re, os
from datetime import datetime

class Facebook:

	"""
		attributes:
					----------------------------------------------
					getLink_status 	- status for getLink() method
					download_status	- status for download() method
					video_size		- size of downloadable video
					origin_link		- original video source
					----------------------------------------------

		methods:
					----------------------------------------------
					getLink(url)	- get original video source
					----------------------------------------------
					download(
					optionargument=folder, video_name
					)				- download video
					----------------------------------------------

	"""

	def __init__(self):
		self.getLink_status = 'Error'
		self.download_status = 'Failed'
		self.video_size = "0 byte"
		self.origin_link = None

	def __repr__(self):
		return "Download Public Videos on Facebook - @n0crush"

	def getLink(self, url):

		res = requests.get(url, timeout=6)
		

		if res.status_code != 200:
			return "[!] Invalid URL. Check again!"
		if not "Set-Cookie" in res.headers.keys():
			return "You must sigin to get origin link to this video!"	#future
		else:
			self.getLink_status = "Success"

		if re.search('hd_src:"(.+?)"', res.text)==None:
			return "HD link not found"
		
		self.origin_link = re.search('hd_src:"(.+?)"', res.text).group(1)

		return "<Response: %s>" %(self.getLink_status)

	def download(self, folder="", video_name=""):
		def getSize(s):
			x = len(s)
			if x>=10:
					result = str(round(int(s)/(1024**3), 1))+" MB"
			elif x>=7:
					result = str(round(int(s)/(1024**2), 1))+" MB"
			elif x>=4:
					result = str(round(int(s)/(1024)))+" Kb"
			elif x<=3:
					result = str(int(s)/(1024**3))+" bytes"
			return result

		if not (os.path.exists(folder)):
			folder = os.path.join(os.path.expanduser('~'), "Downloads")
			print("[!] Using default folder: ", folder)

		incorrect_video_name = False
		for i in "\\/:*?\"<>|":
			if i in video_name:
				incorrect_video_name = True
				print("[!] Video name invalid. Used 'facebook_video_' as name.")
				break

		if video_name=="" or incorrect_video_name==True:
			duma = str(datetime.now())[:19].replace(':', "_")
			duma = duma.replace(" ", "_")
			duma = duma.replace('-', "_")

			video_name = 'facebook_video_'+duma+'.mp4'
		elif ".mp4" not in video_name:		
			video_name += ".mp4"

		path = folder+"\\"+video_name

		if self.origin_link==None:
			return "[<Download status: %s>]" %(self.download_status)
		else:
			self.download_status="Success"

		res = requests.get(self.origin_link, allow_redirects=False)

		self.video_size = getSize(res.headers['Content-Length'])

		with open(path, 'wb') as data:
			data.write(res.content)

		return "[<Download status: %s>, <Path: %s>]" %(self.download_status, path)

#cs--------------

# url = "https://www.facebook.com/le.nguen.794/videos/206149947224826/"
# f = Facebook()
# xx = f.getLink(url)
# xy = f.download("C:\\users\\your_pc_name\\desktop", "let_delete_me.mp4")

# print('xx-', xx)
# print('xy-', xy)
# print('-'*50)
# print(f.getLink_status)
# print(f.download_status)
# print(f.origin_link)
# print(f.video_size)
# print('-'*50)

#ce--------------


