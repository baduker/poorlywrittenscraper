import re
import requests
from bs4 import BeautifulSoup as bs

url = 'http://www.poorlydrawnlines.com/archive/'
req = requests.get(url)
page = req.text

soup = bs(page, 'html.parser')

all_links = []

for link in soup.find_all('a'):
	all_links.append(link.get('href'))

print('Finished downloading links!')
print(len(all_links))

pattern = re.compile(r'http://www.poorlydrawnlines.com/comic/.+')

filtered = [i for i in all_links if pattern.match(i)]

print(len(filtered))
for i in filtered:
	print(i)
