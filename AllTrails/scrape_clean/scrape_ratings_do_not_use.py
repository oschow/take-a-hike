from bs4 import BeautifulSoup
from pymongo import MongoClient
from requests import get, post
import pandas as pd

def get_soup(url):
    response = get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def parse_ratings(user, name_of_hike, hike_id):
    row_data = {}
    if user.find('span', itemprop='author') != None:
        user_name = user.find('span', itemprop='author').text
        rating = user.find('span', itemprop="reviewRating").findChildren('meta')[0]['content']
        row_data['hike_name'] = name_of_hike
        row_data['hike_id'] = hike_id
        row_data['user_name'] = user_name
        row_data['rating'] = rating
    return row_data


def get_ratings(soup):
    load_more = soup.select('div#load_more.feed-item.load-more.trail-load').find('h3')
    hikes = soup.select('div.trail-result-card')
    hike_id_count = 0
    for hike in hikes:
        name_of_hike = hike.select('div.name.short')[0].text
        hike_id = hike_id_count
        hike_id_count += 1
        h = hike.findChild('a')
        hike_url = 'http://www.alltrails.com' + h['href']
        review_soup = get_soup(hike_url)
        users = review_soup.select('div.feed-user-content.rounded')
        for user in users:
            mongo_doc = parse_ratings(user, name_of_hike, hike_id)
            table.insert_one(mongo_doc)

if __name__ == '__main__':
    client = MongoClient()
    db = client['ratings_db']
    table = db['ratings']

    start_url = 'http://www.alltrails.com/us/colorado?ref=search'
    soup = get_soup(start_url)
    ratings = get_ratings(soup)
