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

# sendmail.email_send("***REMOVED***", methods.createhtmlbody())

## New main loop

methods.pennanalyze()