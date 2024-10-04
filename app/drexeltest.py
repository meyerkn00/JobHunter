import re
import requests
from time import sleep
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, expect
import pandas as pd
# Custom module, see database.py in main folder
import methods.database as database

def drexel_job_update():
    """Job update function for Drexel"""
    url = 'https://careers.drexel.edu/en-us/listing/'
    #page = requests.get(url)
    pass


url = 'https://careers.drexel.edu/en-us/listing/'
print(requests.get(url))