# Manga-Scraper

## Introduction
This script downloads manga from kissmanga.com

Inspired From [Astrames](https://github.com/Astrames/kissmanga-downloader)

## Contents
<!-- * [Demo](ttps://github.com/Crucizer/Manga-Scrapper/#Demo) -->
* [Installation](https://github.com/Crucizer/Manga-Scrapper/#Installation)
* [Usuage](https://github.com/Crucizer/Manga-Scrapper/#Usuage)
* [Features](https://github.com/Crucizer/Manga-Scrapper/#Features)

## Installation
* Install 3.8 from [here](https://www.python.org/downloads/release/python-382/)
* Install git from [here](https://git-scm.com/downloads)
* Run `git clone https://github.com/Crucizer/Manga-Scrapper.git`
* Run `pip install -r requirements.txt`
* Download ChromeDriver From [here](https://chromedriver.chromium.org/downloads)
* Add the location of ChromeDriver into environmental variables and save it as "chromedriver"

## Usage
* Change the "save_path" variable in the starting of the `main.py` file if you wanna change manga directory to somewhere else.(By Default it's the same directory as the script)
* Execute `manga.py`.
* Enter The URL of the manga from kissmanga.com
* Enter the chapter range
* Enjoy!

## Features

* Downloads all images of a chapter and puts them in a seperate folder.
* Creates A CBR of each chapter outside the directory and deletes the chapter directory as it is no longer needed.
