import requests
from bs4 import BeautifulSoup

# Brookings seems to have all of the job search data hidden within javascript. Skipping for now
# URL = "https://careers-brookings.icims.com/jobs/search?ss=1&hashed=-435682078"
# page = requests.get(URL)

# Penn Demo
URL = "https://wd1.myworkdaysite.com/recruiting/upenn/careers-at-penn/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'lxml')

results = soup.find("ul")

soup.ul
