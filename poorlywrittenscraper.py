import os
import sys
import re
import requests
import itertools
from requests import get
from bs4 import BeautifulSoup as bs

HOME_DIR = os.getcwd()
DEFAULT_DIR_NAME = 'poorly_created_folder'

def show_logo():
  print("""
a Python comic(al) scraper for poorlydwarnlines.com
                         __
.-----.-----.-----.----.|  |.--.--.
|  _  |  _  |  _  |   _||  ||  |  |
|   __|_____|_____|__|  |__||___  |
|__|                        |_____|
                __ __   __
.--.--.--.----.|__|  |_|  |_.-----.-----.
|  |  |  |   _||  |   _|   _|  -__|     |
|________|__|  |__|____|____|_____|__|__|

.-----.----.----.---.-.-----.-----.----.
|__ --|  __|   _|  _  |  _  |  -__|   _|
|_____|____|__| |___._|   __|_____|__|
                      |__|
version: 0.2 | author: baduker | https://github.com/baduker
  """)

def handle_menu():
  print("\nThe scraper has found {} comics.".format(len(found_comics)))
  print("How many comics do you want to download?")
  print("Type 0 to exit.")

  while True:
    try:
      global n_of_comics
      n_of_comics = int(input(">> ").strip())
    except ValueError:
      print("Error: incorrect value. Try again.")
      continue
    if n_of_comics > len(found_comics) or n_of_comics < 0:
      print("Error: incorrect number of comics to download. Try again.")
      continue
    elif n_of_comics == 0:
      sys.exit()
    else:
      break
  return n_of_comics

def move_to_dir(title):
  if os.getcwd() != HOME_DIR:
    os.chdir(HOME_DIR)
  try:
    os.mkdir(title)
    os.chdir(title)
  except FileExistsError:
    os.chdir(title)
  except:
    print("Couldn't create directory!")

def generate_comic_link(array, num):
  for link in itertools.islice(array, 0, num):
    yield link

def grab_image_src_url(link):
  req = requests.get(link)
  comic = req.text
  soup = bs(comic, 'html.parser')
  for i in soup.find_all('p'):
    for img in i.find_all('img', src=True):
      return img['src']

def download_image(link):
  file_name = url.split('/')[-1]
  with open(file_name, "wb") as file:
    response = get(url)
    file.write(response.content)

def fetch_comic_archive():
  url = 'http://www.poorlydrawnlines.com/archive/'
  req = requests.get(url)
  page = req.text
  soup = bs(page, 'html.parser')
  all_links = []
  for link in soup.find_all('a'):
    all_links.append(link.get('href'))
  return all_links

def filter_comic_archive(archive):
  pattern = re.compile(r'http://www.poorlydrawnlines.com/comic/.+')
  filtered_links = [i for i in archive if pattern.match(i)]
  return filtered_links

show_logo()

all_comics = fetch_comic_archive()
found_comics = filter_comic_archive(all_comics)

handle_menu()

for link in generate_comic_link(found_comics, n_of_comics):
  print("Downloading: {}".format(link))
  move_to_dir(DEFAULT_DIR_NAME)
  url = grab_image_src_url(link)
  download_image(url)

print("Successfully downloaded {} comics.".format(n_of_comics))

