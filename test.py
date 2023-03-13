from bs4 import BeautifulSoup
# import required module
import os

# assign directory
directory = 'htmls/'

# iterate over files in
# that directory
for filename in os.scandir(directory):
    if filename.is_file():
        print(filename.path)

with open("htmls/index.html") as h:
    body = h.read()
soup = BeautifulSoup(body, 'html.parser')

for link in soup.find_all('a'):
    if 'unsubscribe' in link.text:
        print(str(link.get('href')))
