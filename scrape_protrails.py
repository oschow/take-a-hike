'''Code to scrape ProTrails Colorado'''

from bs4 import BeautifulSoup
from pymongo import MongoClient
from requests import get
import json

def get_soup(url):
    response = get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def parse_hikes(hike_soup, area):
    page_body = hike_soup.find('body')
    title = page_body.select('div.trail-title')
    name = title[0].findChild('h1').text.split('-')[0]
    name = name.replace('.', '')
    hike_data_table = hike_soup.find('table', id='trail-details-table')
    hike_area = area.split('/')[-1]
    round_trip_length = float(hike_data_table.findChildren('td')[1].text.split()[0])
    start_elevation = hike_data_table.findChildren('td')[3].text.split()[0]
    end_elevation = hike_data_table.findChildren('td')[3].text.split()[2]
    net_elevation_gain = hike_data_table.findChildren('td')[5].text.split()[0]
    skill_level = hike_data_table.findChildren('td')[7].text
    dogs_allowed = bool(hike_data_table.findChildren('td')[9].text)
    gps = hike_soup.select('div.trail-description-gps-coordinates')
    if len(gps) != 0:
        gps_coordinates = gps[0].findChildren('li')[0].text
    else:
        gps_coordinates = 'Null'
    desc = hike_soup.select('div.trail-description-description')[0]
    description = desc.findChildren('p')[0].text
    if len(desc) > 1:
        for text_chunk in desc.findChildren('p')[1:]:
            text = ''.join(text_chunk.text)
            description += text
    return {name: {'part_of_co': hike_area,
                     'round_trip_length': round_trip_length,
                     'start_elevation': start_elevation,
                     'end_elevation': end_elevation,
                     'net_elevation_gain': net_elevation_gain,
                     'skill_level': skill_level,
                     'dogs_allowed': dogs_allowed,
                     'gps_coordinates': gps_coordinates,
                     'trail_description': description}}

def get_hike_data(soup, area):
    hikes = soup.findAll('div', id='quicktabs-tabpage-pro_area_tabs-0')[0].findChildren('a')
    for hike in hikes:
        hike_url = 'http://www.protrails.com' + hike['href']
        hike_soup = get_soup(hike_url)
        mongo_doc = parse_hikes(hike_soup, area)
        table.insert_one(mongo_doc)

if __name__ == '__main__':
    client = MongoClient()
    db = client['hike_db']
    table = db['hikes']

    aspen_url = 'http://www.protrails.com/area/82/Aspen-Snowmass'
    denver_url = 'http://www.protrails.com/area/4/boulder-denver-golden-fort-collins-lyons'
    national_monument_url = 'http://www.protrails.com/area/26/colorado-national-monument'
    gsdnp_url = 'http://www.protrails.com/area/64/great-sand-dunes-national-park'
    indian_peaks_url = 'http://www.protrails.com/area/5/indian-peaks-wilderness-area-james-peak-wilderness-area'
    rmnp_url = 'http://www.protrails.com/area/8/rocky-mountain-national-park'
    summit_eagle_clearcreek_url = 'http://www.protrails.com/area/41/summit-county-eagle-county-clear-creek-county'

    urls = [aspen_url, denver_url, national_monument_url, gsdnp_url, indian_peaks_url, rmnp_url, summit_eagle_clearcreek_url]
    for area in urls:
        soup = get_soup(area)
        get_hike_data(soup, area)

    # Code below will print out the first 5 entries in the database
    # c = table.find()
    # for i in range(5):
    #     print next(c)
    #     raw_input('')
