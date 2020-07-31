# Importing Stuff
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
# importing tqdm for progress bar
from tqdm import tqdm
# Importing build-in modules
import urllib.request 
import os
import sys
import shutil
from pathlib import Path
import requests

# Sample URL
# https://kissmanga.com/Manga/Great-Teacher-onizuka/
# https://kissmanga.com/Manga/Shingeki-no-kyojin/
# https://kissmanga.com/Manga/monster/
# https://kissmanga.com/Manga/the-promised-neverland/

try:
	# save path for the manga
	# Please change the path
	save_path = os.environ.get("manga_path")
except:
	save_path = str(Path(__file__).parent.resolve())
save_path = list(save_path)
if save_path[-1] != "/":
	save_path += ["/"]
save_path = "".join(save_path)
# Getting chromedriver details
driver_path = os.environ.get("chromedriver")
Options = Options()
Options.headless = True
print("Launcing Web browser Silently...")

class Download:
	def __init__(self):
		# Getting info about the manga
		# self.browser = webdriver.Chrome(driver_path, options=Options)
		self.browser = webdriver.Chrome(ChromeDriverManager().install())
		self.url = input("Enter the url of the manga: ")
		self.change_name()
		self.browser.get(self.url)
		self.get_chapters()

	# Getting all chapter urls and slicing them in range with user's request
	def get_chapters(self):
		print(f"Getting chapters from {self.manga_name}...\nPlease Wait...")
		try:
			# This waits for the web page to load properly
			title_tag = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME,"bigChar")))
			title_text = title_tag.text
		except TimeoutException:
		    print("Exception Occured: TimeoutException")
		    print("Couldn't get the web page! Please check the URL and the internet connection.")
		    choice = input("If the webpage is not loaded or if there is a captcha, please solve it\nPress \"y\" to continue and any other key to exit: ")
		    if choice != "y" or choice == "Y":
		    	self.finished()
		    	sys.exit()
		# finding links of all chapters by xpath
		lis_of_ch = self.browser.find_elements_by_xpath("//tbody/tr/td/a")
		# reversing them as they are in reversed order
		lis_of_ch = lis_of_ch[::-1]
		self.chapters = []
		self.ch_names = []
		for ch in lis_of_ch:
			self.chapters.append(ch.get_attribute("href"))
			self.ch_names.append(ch.text)
			# print(ch.text)

		# print(self.ch_names)
		# print(lis_of_ch)
		print(f"There are {len(self.chapters)} Indexes of {self.manga_name}\nPlease enter the range of chapters.")
		# Getting range from user
		self.low_ch = int(input("From Which Index: "))
		self.high_ch = int(input("To which Index: "))
		self.chapters = self.chapters[(self.low_ch-1):self.high_ch]

		self.vol = self.low_ch
		try:
			os.mkdir(save_path + self.manga_name)
			print(f"Making {self.manga_name} directory...")
		except:
			print(f"{self.manga_name} directory already exists...")
		# for ch in self.chapters:
		# 	self.download_chapter(ch)
		# 	self.vol += 1

		for i in range(len(self.chapters)):
			self.current = i
			self.download_chapter(self.chapters[self.current])
			self.vol+=1
		self.finished()

	# This downloads each chapter
	def download_chapter(self, url):
		os.chdir(save_path)
		# Checking if chapter already exists or not
		self.check_if_chapter_exist()
		# Making directory and putting this stuff in that directory
		try:
			os.mkdir(f"{save_path}{self.manga_name}/{self.vol}")
			print(f"Making chapter {self.vol} directory...")
		except:
			pass
		dir_name = f"{self.vol}"
		count = 1
		self.browser.get(url)
		# Waiting for the webpage to load properly
		try:
		    drop_down_list = WebDriverWait(self.browser, 15).until(EC.presence_of_element_located((By.ID,"selectReadType")))
		except TimeoutException:
		    print("Couldn't get the web page! Please check the URL and the internet connection.")
		    choice = input("If the webpage is not loaded or if there is a captcha, please solve it\nPress \"y\" to continue and any other key to exit: ")
		    if choice != "y" or choice == "Y":
		    	self.finished()
		    	sys.exit()
		# select = Select(drop_down_list)
		# # Selecting the 'All Pages' option
		# select.select_by_value('1')
		# got the list of images
		list_of_page_img = []
		names = []
		for i in self.browser.find_elements_by_xpath('//div[@id="divImage"]/p/img'):
			list_of_page_img.append(i)
			names.append(i.get_attribute('text'))
		# print(names)
		chapters_left = len(list_of_page_img) - count
		# This thing does the downloading work and showing the progess bar
		with tqdm(total=len(list_of_page_img), desc=f"Downloading Chapter {self.vol}", bar_format="{l_bar}{bar:25} [ Time left: {remaining} ]") as pbar:
			for image in list_of_page_img:
			    url = image.get_attribute("src")
			    r = requests.get(url)
			    self.format = url.split(".")[-1]
			    with open((save_path + self.manga_name + "/" + dir_name + "/"+ f"Page {count}.{self.format}"), 'wb') as outfile:
			        outfile.write(r.content)			    #####	
			    count += 1
			    chapters_left = len(list_of_page_img) - count
			    pbar.update(1)

		# Calling other function to do some stuff
		self.to_cbr()

		# Change this to call other functions
		call = False
		if call:
			self.call_other_functions()


	# Convert File to .cbr format
	def to_cbr(self):
		print("Compressing images to .cbr format ...")
		os.chdir(f"{save_path}/{self.manga_name}/")
		file_name = f"""{self.vol} - {self.ch_names[self.vol-1]}"""
		shutil.make_archive(file_name,"zip", str(self.vol))
		os.rename(f"{file_name}.zip",f"{file_name}.cbr")

		# Deleting the images folder
		self.del_folder()


	# Deletes the stuff
	def del_folder(self):
		print("Deleting Images Folder ...")
		shutil.rmtree(str(self.vol))

	# This function does a pretty uneccesary job by changing the name of the manga to a good looking one
	def change_name(self):
		self.manga_name = self.url.split("/")[-1]
		# Making lists of all uppercase and lowercase letters
		uppercase = [chr(i) for i in range(65,65+26)]
		lowercase = [chr(i) for i in range(97, 97+26)]
		# Getting the manga name from the url
		if self.manga_name == "":
			self.manga_name = self.url.split("/")[-2]
		# changing the manga letters to uppercase and lowercase accordindly
		self.manga = self.manga_name.split("-")
		for i in range(len(self.manga)):
			tmp = list(self.manga[i])
			if tmp[0] in lowercase:
				tmp[0] = uppercase[lowercase.index(self.manga[i][0])]
				self.manga[i] = "".join(tmp)
		self.manga_name = " ".join(self.manga)

	# This function checks if the chapter pdf already exist or not
	def check_if_chapter_exist(self):
		try:
			if f"{self.vol} - {self.ch_names[self.vol-1]}.cbr" in os.listdir(self.manga_name):
				choice = input('Chapter already exists. Do you wanna overwrite?("y" for yes and "n" for no)')
				if choice == "y" or choice == "Y":
					print("Overwriting...")
					os.remove(f"Chapter {self.vol}.pdf")
				elif choice == "n" or choice == "N":
					print("Skipping...")
					if self.vol + 1 <= self.high_ch:
						print("Going to next chapter...")
						self.vol = self.vol + 1
					else:
						self.finished()
						sys.exit()
						exit()
				else:
					print("Invalid Choice. Choose Again")
					self.check_if_pdf_exist()
		except:
			pass

	# Closes the web browser
	def finished(self):
		print("Exiting...")
		self.browser.quit()
		sys.exit()

Object = Download()
