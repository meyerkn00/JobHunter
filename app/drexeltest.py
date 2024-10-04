import re
import requests
from time import sleep
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, expect
import pandas as pd
# Custom module, see database.py in main folder
import methods.database as database
import methods.web_queries as query

def drexel_job_update():
    """Job update function for Drexel"""
    url = 'https://careers.drexel.edu/en-us/listing/'
    urlsnippet = 'https://careers.drexel.edu'
    soup = query.webquery(url)
    results = str(soup.tbody.find_all("a"))
    rawlinks = re.findall(r'href="(/en-us.*?)"', results)
    links = [f'{urlsnippet}{x}' for x in rawlinks]
    names = re.findall(r'>(.*?)</a>', results)    
    table = pd.DataFrame({'names': names, 'links': links})
    return table
print(drexel_job_update())

# url = 'https://careers.drexel.edu/en-us/listing/'
# urlsnippet = 'https://careers.drexel.edu'
# soup = query.webquery(url)
# results = str(soup.tbody.find_all("a"))
# rawlinks = re.findall(r'href="(/en-us.*?)"', results)
# links = [f'{urlsnippet}{x}' for x in rawlinks]
# names = re.findall(r'>(.*?)</a>', results)    
# table = pd.DataFrame({'names': names, 'links': links})
#print(table)