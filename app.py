# import requests
import re
from datetime import date
from time import sleep
from dataclasses import dataclass
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from simplegmail import Gmail

# Brookings seems to have all of the job search data hidden within javascript. Skipping for now
# URL = "https://careers-brookings.icims.com/jobs/search?ss=1&hashed=-435682078"
# page = requests.get(URL)

## Outside of central loop definitions

# Output class
"""The following class takes a name input and creates
        1. Joblist to store job results
        2. function to add to joblist
        3. bundle function to take all job lists and assemble into string for email
"""

class Company:
    def __init__(self, name):
        self.name = name
        self.joblist = []
        self.jobhtml = ''
    
    def add_job(self, joblist):
        self.joblist.append(joblist)
    
    def bundle(self):
        self.jobhtml = ''.join(self.joblist)
        return(self.jobhtml)

@dataclass
class Job:
    title: str
    link: str
    # location: str

## All of this will go within a loop
# Penn Demo using playwright

"""Generic function for pulling website html
        Takes URL arg
        returns html in soup form
"""

def webquery(URL):
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

"""Analysis function for Penn Workday
        returns Penn class containing jobs within
        to do: turn output into table
"""

def pennanalyze():
    URL = "https://wd1.myworkdaysite.com/recruiting/upenn/careers-at-penn/"
    soup = webquery(URL)
    
    results = str(soup.ul.find_all("a"))
    result_elements = soup.ul       .find_all("a")

    # Regex finds job names and links from soup

    links = re.findall(r'href="(/en-US.*?)"', results)
    names = re.findall(r'>([A-Za-z].*?)<', results)

    # Add first 6 jobs to the joblist of Penn
    Penn = Company("Penn")

    for i in range(5):
    # This is just to catch if there are less than 6 jobs on a page
        if names[i] == [] or links[i] == []:
            jobhtml = '<p>None</p><br />'
            # x = Job(title = "null", link = "null")
        else:
            fulllink = f'https://wd1.myworkdaysite.com{links[i]}'
            jobhtml = f'<a href={fulllink}>{names[i]}</a><br />'
            # x = Job(title = names[i], link = fulllink)
        Penn.add_job(jobhtml)

    return Penn

# print(Penn.joblist)

# Send results in email

# first time this is run it prompts a login, not sure how to do this on a server
# If your browser is on a different machine then exit and re-run this
# application with the command-line parameter
#  --noauth_local_webserver

def sendreport():
    gmail = Gmail()

    todays_date = date.today()

    params = {
        "to": "karl+jh@themeyers.org",
        "sender": "karl0mey@gmail.com",
        "subject": f'Job Hunter Report {todays_date}',
        "msg_html": f'<h1>Job Report {todays_date}</h1><br />'\
                    '<p>Today\'s Job Report is as follows:</p><br />'\
                    f'<h2>{Penn.name}</h2><br />'\
                    f'{Penn.bundle()}'
    }

    message = gmail.send_message(**params)