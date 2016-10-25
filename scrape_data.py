'''Code to scrape ProTrails Colorado'''

from bs4 import BeautifulSoup
from pymongo import MongoClient
from requests import get
import pandas as pd
import numpy as np

def get_soup(url):
    response = get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

if __name__ == '__main__':
    co_url = 'http://www.protrails.com/state/colorado'
    soup = get_soup(url)

    client = MongoClient()
    db = client['hike_database']
    tab = db['hikes']

    co_areas = soup.select('a')
    for area in co_areas:
        href = area.findChild('a')['href']
        co_area_url = url + href
        area_soup = get_co_area_url(co_area_url)
        hike_mongo= hike_info(area_soup)
        tab.insert_one(hike_mongo)
