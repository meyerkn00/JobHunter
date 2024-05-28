# import requests
import re
import requests
from datetime import date
from datetime import datetime as dtm
from time import sleep
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from simplegmail import Gmail
import pandas as pd
import numpy as np

# Brookings seems to have all of the job search data hidden within javascript. Skipping for now
# URL = "https://careers-brookings.icims.com/jobs/search?ss=1&hashed=-435682078"
# page = requests.get(URL)

## Outside of central loop definitions

def webquery(URL):
    """Generic function for pulling website html.
    
        Takes URL arg
        returns html in soup form
    """
    # URL = "https://wd1.myworkdaysite.com/recruiting/upenn/careers-at-penn/"
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(URL)
        # TO DO: Fix the sleep to be dynamically triggered by a body element loading
        sleep(2)
        soup = BeautifulSoup(page.content(), 'lxml')
        browser.close()
    return soup


def createhtml(company):
    """"Roll-up" Function for company data frames.
        
        Takes each job and turns it into html for output
    """
    subset = company.iloc[0:7, :]
    htmllist = [f'<a href={x}>{y}</a><br />' for x, y in zip(subset['links'], subset['names'])]
    html = ''.join(htmllist)
    return html


def pennanalyze():
    """Analysis function for Penn Workday.
        
        returns Penn class containing jobs within
        to do: turn output into table
    """
    URL = "https://wd1.myworkdaysite.com/recruiting/upenn/careers-at-penn/"
    soup = webquery(URL)
    
    results = str(soup.ul.find_all("a"))

    # Regex finds job names and links from soup
    rawlinks = re.findall(r'href="(/en-US.*?)"', results)
    links = [f'https://wd1.myworkdaysite.com{x}' for x in rawlinks]
    names = re.findall(r'>([A-Za-z].*?)<', results)
 
    # pandas dataframe
    penntable = pd.DataFrame({
        'names': names,
        'links': links
    })

    pennhtml = createhtml(penntable)
    return pennhtml

def brookanalyze():
    URL = "https://careers-brookings.icims.com/jobs/search?ss=1&hashed=-435682078"
    iframe = "https://careers-brookings.icims.com/jobs/search?ss=1&hashed=-435682078&in_iframe=1"

    page = requests.get(iframe)

    soup = BeautifulSoup(page.content, 'lxml')
    results = str(soup.find_all("div", {"class": "col-xs-12 title"}))

    links = re.findall(r'href="(.*?)"', results)
    names = re.findall(r'title="[0-9].*? - (.*?)"', results)

    brooktable = pd.DataFrame({
            'names': names,
            'links': links
        })
    
    brookhtml = createhtml(brooktable)
    return brookhtml

# Send results in email

def sendreport(job1):
    """Sends job results via gmail.
        
        currently BROKEN due to api key issue. Google cloud tokens auto-expire after 7 days,
        which cannot be changed for non-reviewed projects.

        The first time this runs it will prompt a login.
        If you are running this remotely use the following command-line param
            --noauth_local_webserver
    """
    gmail = Gmail()

    todays_date = date.today()

    params = {
        "to": "karl+jh@themeyers.org",
        "sender": "karl0mey@gmail.com",
        "subject": f'Job Hunter Report {todays_date}',
        "msg_html": f'<h1>Job Report {todays_date}</h1><br />'\
                    '<p>Today\'s Job Report is as follows:</p><br />'\
                    f'<h2>{job1.name}</h2><br />'\
                    f'{job1.bundle()}'
    }

    message = gmail.send_message(**params)

def savereport(penn, brook):
    """Temp function for saving job results as html.
        
        will be superseded by an email sending function
    """
    todays_date = date.today()
    with open(f'TestOutput/{dtm.strftime(dtm.now(),'%m%d%y.%H%M')}.html', 'w', encoding="utf-8") as f:
        f.write(
            '<html><body>'
            f'<h1>Job Report {todays_date}</h1>'\
                '<p>Today\'s Job Report is as follows:</p>'\
                '<h2>University of Pennsylvania</h2>'\
                f'{penn}'
                '<h2>Brookings Institution</h2>'\
                f'{brook}'
            '</body></html>'
        )
        f.close()
        
# What will become the main loop

# penndata = pennanalyze()

savereport(pennanalyze(), brookanalyze())

# sendreport(penndata)