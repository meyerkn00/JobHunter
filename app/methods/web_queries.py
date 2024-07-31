import re
import requests
from time import sleep
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, expect
import pandas as pd
# Custom module, see database.py in main folder
import methods.database as database

## Function Definitions

def webquery(url):
    """Generic function for pulling website html.
    
        Takes url arg
        returns html in soup form
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        # TO DO: Fix the sleep to be dynamically triggered by a body element loading
        # page.wait_for_timeout(2000)
        # expect(page.locator('id=root')).not_to_be_empty()
        expect(page.get_by_role("listitem").first).not_to_be_empty()
        soup = BeautifulSoup(page.content(), 'lxml')
        browser.close()
    return soup

def workday_update(url, urlsnippet):
    soup = webquery(url)

    results = str(soup.ul.find_all("a"))

    # Regex finds job names and links from soup
    rawlinks = re.findall(r'href="(/en-US.*?)"', results)
    links = [f'{urlsnippet}{x}' for x in rawlinks]
    names = re.findall(r'>(.*?)</a>', results)
    
    table = pd.DataFrame({
        'names': names,
        'links': links
    })

    return table

def penn_job_update():
    # """Job update function for Penn Workday."""
    url = "https://wd1.myworkdaysite.com/recruiting/upenn/careers-at-penn/"
    urlsnippet = 'https://wd1.myworkdaysite.com'
    database.add_to_jobs(1, workday_update(url, urlsnippet))

def comcast_job_update():
    """Job update function for Comcast.
            
            Basically identical to Penn
    """
    url = "https://comcast.wd5.myworkdayjobs.com/en-US/Comcast_Careers/jobs"
    urlsnippet = 'https://comcast.wd5.myworkdayjobs.com'
    database.add_to_jobs(2, workday_update(url, urlsnippet))

def brookings_job_update():
    """Job update function for Brookings"""
    url = "https://careers-brookings.icims.com/jobs/search?ss=1&hashed=-435682078"
    iframe = "https://careers-brookings.icims.com/jobs/search?ss=1&hashed=-435682078&in_iframe=1"

    page = requests.get(iframe, timeout=10)

    soup = BeautifulSoup(page.content, 'lxml')
    results = str(soup.find_all("div", {"class": "col-xs-12 title"}))

    links = re.findall(r'href="(.*?)"', results)
    names = re.findall(r'title="[0-9].*? - (.*?)"', results)

    table = pd.DataFrame({
            'names': names,
            'links': links
        })
    
    database.add_to_jobs(3, table)

def reliance_job_update():
    """Job update function for Reliance Standard"""
    url = "https://rsli.wd5.myworkdayjobs.com/en-US/RSLIJobs"
    urlsnippet = 'https://rsli.wd5.myworkdayjobs.com'
    database.add_to_jobs(4, workday_update(url, urlsnippet))

def update_job_db():
    penn_job_update() # ID 1
    brookings_job_update() # ID 2
    comcast_job_update() # ID 3
    reliance_job_update() # ID 4