import re
import requests
import itertools
from bs4 import BeautifulSoup as bs

def grab_link(array):
	for link in itertools.islice(array, 0, 3):
		yield link

def grab_image(link):
	req = requests.get(link)
	comic = req.text
	soup = bs(comic, 'html.parser')
	for i in soup.find_all('p'):
		for img in i.find_all('img', src=True):
			print(img['src'])

url = 'http://www.poorlydrawnlines.com/archive/'
req = requests.get(url)
page = req.text

soup = bs(page, 'html.parser')

all_links = []

for link in soup.find_all('a'):
	all_links.append(link.get('href'))

pattern = re.compile(r'http://www.poorlydrawnlines.com/comic/.+')

filtered_links = [i for i in all_links if pattern.match(i)]

for link in grab_link(filtered_links):
	grab_image(link)

# print('{} comics found.'.format(len(filtered_links)))
