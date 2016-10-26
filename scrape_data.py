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
    title = hike_soup.find('div', id='trail-title')
    name = title[0].findChild('h1').text
    hike_data_table = hike_soup.find('table', id='trail-details-table')
    hike_area = area
    round_trip_length = hike_data_table.findChildren('td')[1].text
    start_end_elevation = hike_data_table.findChildren('td')[3].text
    elevation_change = hike_data_table.findChildren('td')[5].text
    skill_level = hike_data_table.findChildren('td')[7].text
    dogs_allowed = hike_data_table.findChildren('td')[9].text
    gps = hike_soup.find('div', id='trail-description-gps-coordinates')
    gps_coordinates = gps.findChildren('li')[0].text
    desc = hike_soup.find('div', id='trail-description-description')
    description = desc.findChildren('p')[1].text + desc.findChildren('p')[3:]
    return {name: {'part_of_co': area,
                     'round_trip_length': round_trip_length,
                     'start_end_elevation': start_end_elevation,
                     'elevation_change': elevation_change,
                     'skill_level': skill_level,
                     'dogs_allowed': dogs_allowed,
                     'gps_coordinates': gps_coordinates,
                     'trail_description': description}}

def get_hike_data(soup, area):
    hikes = soup.findAll('div', id='quicktabs-tabpage-pro_area_tabs-0')[0].findChildren('a')
    for hike in hikes:
        hike_url = 'http://www.protrails.com/' + hike['href']
        hike_soup = get_soup(hike_url)
        mongo_doc = parse_hikes(hike_soup, area)
        table.insert_one(mongo_doc)

if __name__ == '__main__':
    client = MongoClient()
    db = client['hike_database']
    table = db['hike_data']

    aspen_url = 'http://www.protrails.com/area/82/Aspen-Snowmass'
    denver_url = 'http://www.protrails.com/area/4/boulder-denver-golden-fort-collins-lyons'
    national_monument_url = 'http://www.protrails.com/area/26/colorado-national-monument'
    gsdnp_url = 'http://www.protrails.com/area/64/great-sand-dunes-national-park'
    indian_peaks_url = 'http://www.protrails.com/area/5/indian-peaks-wilderness-area-james-peak-wilderness-area'
    rmnp_url = 'http://www.protrails.com/area/8/rocky-mountain-national-park'
    summit_eagle_clearcreek_url = 'http://www.protrails.com/area/41/summit-county-eagle-county-clear-creek-county'

    # urls = [aspen_url, denver_url, national_monument_url, gsdnp_url, indian_peaks_url, rmnp_url, summit_eagle_clearcreek_url]
    # for area in urls:
    #     soup = get_soup(area)
    #     get_hike_data(soup, area)


    aspen_soup = get_soup(aspen_url)
    # denver_soup = get_soup(denver_url)
    # national_monument_soup = get_soup(national_monument_url)
    # gsdnp_soup = get_soup(gsdnp_url)
    # indian_peaks_soup = get_soup(indian_peaks_url)
    # rmnp_soup = get_soup(rmnp_url)
    # summit_eagle_clearcreek_soup = get_soup(summit_eagle_clearcreek_url)

    # c = table.find()
    # for i in range(5):
    #     print next(c)
    #     raw_input('')
