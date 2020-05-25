# Importing Stuff
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import urllib.request 
import os
import sys
import img2pdf
import shutil
from pathlib import Path
from selenium.webdriver.chrome.options import Options

# save path for the manga
# Please put a "/" at the end to indicate the directory
save_path = "/mnt/2ADAC21CDAC1E463/Docs/Manga/"
# save_path = Path(__file__).parent.resolve()
# Sample Url = https://kissmanga.com/Manga/Great-Teacher-Onizuka/
driver_path = os.environ.get("chromedriver")
Options = Options()
Options.headless = True
print("Launcing Web browser Silently...")
# brave_path = "/usr/bin/brave-browser-stable"
# option = webdriver.ChromeOptions()
# option.binary_location = brave_path
# ----------------------------------------------------------

class Download:
	# Getting all chapter urls and slicing them in range with user's request
	def get_chapters(self):
		print(f"Getting chapters from {self.manga_name}...Please Wait")
		try:
			title_tag = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME,"bigChar")))
			title_text = title_tag.text
		except TimeoutException:
		    print("Exception Occured:    TimeoutException")
		    sys.exit("Couldn't get title! Please check the URL and the internet connection.")
		# finding links of all chapters by xpath
		lis_of_ch = self.browser.find_elements_by_xpath("//tbody/tr/td/a")
		# reversing them as they are in reversed orde
		lis_of_ch = lis_of_ch[::-1]
		self.chapters = []
		for ch in lis_of_ch:
			self.chapters.append(ch.get_attribute("href"))
		self.chapters = self.chapters[(self.low_ch-1):self.high_ch]

		self.vol = self.low_ch
		try:
			print(f"Making {self.manga_name} directory...")
			os.mkdir(save_path + self.manga_name)
		except:
			pass
		# os.chdir(self.manga_name)
		for ch in self.chapters:
			self.download_chapter(ch)
			self.vol += 1

	def download_chapter(self, url):
		os.chdir(save_path)
		# Making directory and putting this stuff in that directory
		print("Making chapter directory...")
		try:
			os.mkdir(f"{save_path}{self.manga_name}/Chapter {self.vol}")
		except:
			pass
		# os.mkdir((save_path + self.manga_name + "/" + f"Chapter {self.vol}"))
		dir_name = f"Chapter {self.vol}"
		count = 1
		try:
			self.browser.get(url)
		except:
			self.browser.find_element_by_link_text("Adblock").click()
			alert = world.browser.switch_to.alert
			alert.accept()
		try:
		        drop_down_list = WebDriverWait(self.browser, 15).until(EC.presence_of_element_located((By.ID,"selectReadType")))
		except TimeoutException:
		    print("Exception Occured:    TimeoutException")
		    sys.exit("Couldn't load chapter! Please check the internet connection.")
		select = Select(drop_down_list)
		# Selecting the 'All Pages' option
		select.select_by_value('1')

		list_of_page_img = self.browser.find_elements_by_xpath('//div[@id="divImage"]/p/img')


		for image in list_of_page_img:
		    url = image.get_attribute("src")
		    print("Downloading page " + str(count))
		    urllib.request.urlretrieve(url, (save_path + self.manga_name + "/" + dir_name + "/"+ f"Page {count}.jpg"))
		    count += 1

		self.jpg_to_pdf()
		self.delete_folder()


	def jpg_to_pdf(self):
		print("Making PDF...")
		os.chdir(f"{save_path}/{self.manga_name}/Chapter {self.vol}/")
		with open(f"Chapter {self.vol}.pdf", "wb") as f:
			f.write(img2pdf.convert([i for i in sorted(os.listdir(), key=len) if i.endswith(".jpg")]))
		os.chdir("../")


	def check_if_multiple_pdfs_exist(self):
		if len(os.listdir()) > 1:
			print("Multiple PDFs exist in that manga directory. Do you want to to combine them into one?")
			choice = input('Press "y" for yes and "n" for no')
		if choice == "y":
			pass
		elif choice == "n":
			pass
		else:
			print("Invalid Choice\n")
			self.check_if_multiple_pdfs_exist()

	def delete_folder(self):
		print("Deleting The Images Folder")
		shutil.rmtree(f"Chapter {self.vol}/")


	def basic(self):
		self.browser = webdriver.Chrome(driver_path, options=Options)
		
		self.url = input("Enter the url of the manga: ")
		self.manga_name = self.url.split("/")[-1]
		uppercase = [chr(i) for i in range(65,65+26)]
		lowercase = [chr(i) for i in range(97, 97+26)]
		if self.manga_name == "":
			self.manga_name = self.url.split("/")[-2]
		self.manga_name = list(self.manga_name)
		if self.manga_name[0] in lowercase:
			self.manga_name[0] = self.manga_name[lowercase.index(self.manga_name[0])]
		self.manga_name = "".join(self.manga_name)
		self.low_ch = int(input("From Which Chapter: "))
		self.high_ch = int(input("To which Chapters: "))
		try:
			self.browser.get(self.url)
		except:
			self.browser.find_element_by_link_text("Adblock").click()
			alert = world.browser.switch_to.alert
			alert.accept()
		self.get_chapters()


hey = Download()
hey.basic()
