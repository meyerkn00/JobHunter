from datetime import date
from datetime import datetime as dtm
from time import sleep
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import pandas as pd
import numpy as np
# Custom modules
import sendmail
import methods
import database

## Main Loop

# sendmail.email_send("karl+jh@themeyers.org", methods.createhtmlbody())

## New main loop

# Update DB with jobs
methods.penn_job_update() # ID 1
methods.comcast_job_update() # ID 2
methods.brookings_job_update() # ID 3

# Pull 