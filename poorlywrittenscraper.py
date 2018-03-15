import os
import re
import requests
import itertools
from requests import get
from bs4 import BeautifulSoup as bs

HOME_DIR = os.getcwd()
DEFAULT_DIR_NAME = 'poorly_created_folder'

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

def grab_link(array):
  for link in itertools.islice(array, 0, 3):
    yield link

def grab_image_source(link):
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

def fetch_archive():
  url = 'http://www.poorlydrawnlines.com/archive/'
  req = requests.get(url)
  page = req.text
  soup = bs(page, 'html.parser')
  all_links = []
  for link in soup.find_all('a'):
    all_links.append(link.get('href'))
  return all_links

def filter_archive(archive):
  pattern = re.compile(r'http://www.poorlydrawnlines.com/comic/.+')
  filtered_links = [i for i in archive if pattern.match(i)]
  return filtered_links

all_comics = fetch_archive()
found_comics = filter_archive(all_comics)

print("{} comics found.".format(len(found_comics)))

for link in grab_link(found_comics):
  print("Downloading {}".format(link))
  move_to_dir(DEFAULT_DIR_NAME)
  url = grab_image_source(link)
  download_image(url)
  print("Done.")

