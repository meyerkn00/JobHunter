# import requests
import re
import requests
from datetime import date
from datetime import datetime as dtm
from time import sleep
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import pandas as pd
import numpy as np
# Custom module, see sendmail.py in main folder
import sendmail
import database

## Function Definitions

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

def keywordsearch(df):
    keywords = ["Data", "Analyst", "Research"]
    df_filtered = df[df["names"].str.contains("|".join(keywords))]
    return df_filtered

def penn_job_update():
    """Analysis function for Penn Workday."""
    URL = "https://wd1.myworkdaysite.com/recruiting/upenn/careers-at-penn/"
    soup = webquery(URL)
    
    results = str(soup.ul.find_all("a"))

    # Regex finds job names and links from soup
    rawlinks = re.findall(r'href="(/en-US.*?)"', results)
    links = [f'https://wd1.myworkdaysite.com{x}' for x in rawlinks]
    names = re.findall(r'>([A-Za-z].*?)<', results)
 
    # pandas dataframe
    table = pd.DataFrame({
        'names': names,
        'links': links
    })

    database.add_to_jobs(1, table)

    # filtered_table = keywordsearch(table)

    # html = createhtml(filtered_table)
    # return html

def comcast_job_update():
    """Analysis function for Comcast.
            
            Basically identical to Penn
    """
    URL = "https://comcast.wd5.myworkdayjobs.com/en-US/Comcast_Careers/jobs"
    soup = webquery(URL)
    results = str(soup.ul.find_all("a"))

    rawlinks = re.findall(r'href="(/en-US.*?)"', results)
    links = [f'https://comcast.wd5.myworkdayjobs.com{x}' for x in rawlinks]
    names = re.findall(r'>([A-Za-z].*?)<', results)
    table = pd.DataFrame({
        'names': names,
        'links': links
    })

    database.add_to_jobs(2, table)
    # filtered_table = keywordsearch(table)

    # html = createhtml(filtered_table)
    # return html

def brookings_job_update():
    """Analysis function for Brookings"""
    URL = "https://careers-brookings.icims.com/jobs/search?ss=1&hashed=-435682078"
    iframe = "https://careers-brookings.icims.com/jobs/search?ss=1&hashed=-435682078&in_iframe=1"

    page = requests.get(iframe)

    soup = BeautifulSoup(page.content, 'lxml')
    results = str(soup.find_all("div", {"class": "col-xs-12 title"}))

    links = re.findall(r'href="(.*?)"', results)
    names = re.findall(r'title="[0-9].*? - (.*?)"', results)

    table = pd.DataFrame({
            'names': names,
            'links': links
        })
    
    database.add_to_jobs(3, table)
    # filtered_table = keywordsearch(table)
    
    # html = createhtml(filtered_table)
    # return html

def savereport():
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
                f'{pennanalyze()}'\
                '<h2>Brookings Institution</h2>'\
                f'{brookanalyze()}'\
                '<h2>Comcast</h2>'\
                f'{comcastanalyze()}'
            '</body></html>'
        )
        f.close()
        
# def createhtmlbody():
#     todays_date = date.today()
#     html =  ('<html><body>'
#             f'<h1>Job Report {todays_date}</h1>'\
#                 '<p>Today\'s Job Report is as follows:</p>'\
#                 '<h2>University of Pennsylvania</h2>'\
#                 f'{pennanalyze()}'\
#                 '<h2>Brookings Institution</h2>'\
#                 f'{brookanalyze()}'\
#                 '<h2>Comcast</h2>'\
#                 f'{comcastanalyze()}'
#             '</body></html>')
#     return html
