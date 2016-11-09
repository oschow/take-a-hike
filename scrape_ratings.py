from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from pymongo import MongoClient
import time

def login(browser):
    browser.get('http://www.alltrails.com')
    go_login = browser.find_element_by_xpath("//li[@id='login'][//a]")
    go_login.click()
    time.sleep(10)
    username = browser.find_element_by_id("user_email")
    password = browser.find_element_by_id("user_password")
    username.send_keys("olivialschow@gmail.com")
    password.send_keys("galvanize")
    browser.find_element_by_name("commit").click()
    search = browser.find_element_by_id("search")
    search.send_keys("Colorado")
    soup, browser = get_all_hikes(browser)
    return soup, browser

def get_all_hikes(browser):
    browser.get('https://www.alltrails.com/us/colorado?ref=search')
    while True:
        try:
            load_more_hikes = WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.XPATH,"//div[@id='load_more'] [@class='feed-item load-more trail-load'][//a]")))
            load_more_hikes.click()
            time.sleep(6)
        except:
            break
    soup = BeautifulSoup(browser.page_source)
    return soup

def get_all_ratings(browser, hike_url):
    browser.get(hike_url)
    while True:
        try:
            load_more_ratings = WebDriverWait(browser, 15).until(EC.visibility_of_element_located((By.XPATH,"//div[@id='load_more'] [@class='feed-item load-more'][//a]")))
            load_more_ratings.click()
            time.sleep(5)
        except:
            break
    soup = BeautifulSoup(browser.page_source)
    return soup

def parse_meta_data(hike_soup):
    header = hike_soup.find('div', id='title-and-menu-box')
    hike_name = header.findChild('h1').text
    difficulty = header.findChild('span').text
    stars = header.findChild('meta')['content']
    num_reviews = header.find('span', itemprop='reviewCount').text
    area = hike_soup.select('div.trail-rank')
    try:
        hike_region = area[0].findChild('span', itemprop='name').text
    except:
        hike_region = area[0].findChild('a').text
    # directions = header.select('li.bar-icon.trail-directions')
    distance = hike_soup.select('span.distance-icon')[0].text
    try:
        elevation_gain = hike_soup.select('span.elevation-icon')[0].text
    except:
        elevation_gain = None
    route_type = hike_soup.select('span.route-icon')[0].text
    tags = hike_soup.select('section.tag-cloud')[0].findChildren('h3')
    hike_attributes = []
    for tag in tags:
        hike_attributes.append(tag.text)
    user_ratings = []
    users = hike_soup.select('div.feed-user-content.rounded')
    for user in users:
        if user.find('span', itemprop='author') != None:
            user_name = user.find('span', itemprop='author').text
            user_name = user_name.replace('.', '')
            rating = user.find('span', itemprop="reviewRating").findChildren('meta')[0]['content']
            user_ratings.append({user_name: rating})
    row_data = {}
    row_data['hike_name'] = hike_name
    row_data['hike_difficulty'] = difficulty
    row_data['stars'] = stars
    row_data['num_reviews'] = num_reviews
    row_data['hike_region'] = hike_region
    row_data['total_distance'] = distance
    row_data['elevation_gain'] = elevation_gain
    row_data['route_type'] = route_type
    row_data['hike_attributes'] = hike_attributes
    row_data['ratings'] = user_ratings
    return row_data

def create_db(soup, browser):
    hikes = soup.select('div.trail-result-card')
    for hike in hikes:
        h = hike.findChild('a')
        if h == None:
            continue
        hike_url = 'http://www.alltrails.com' + h['href']
        hike_soup = get_all_ratings(browser, hike_url)
        mongo_doc = parse_meta_data(hike_soup)
        table.insert_one(mongo_doc)


if __name__ == '__main__':
    client = MongoClient()
    db = client['rating_db']
    table = db['hikes']

    browser = webdriver.Chrome()
    soup = get_all_hikes(browser)
    create_db(soup, browser)
