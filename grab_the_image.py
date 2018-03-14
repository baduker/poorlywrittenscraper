import re
import requests
from bs4 import BeautifulSoup as bs

url = 'http://www.poorlydrawnlines.com/comic/phone/'
req = requests.get(url)
comic = req.text

soup = bs(comic, 'html.parser')

for i in soup.find_all('p'):
	for img in i.find_all('img', src=True):
		print(img['src'])
