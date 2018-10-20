import requests
import re
import json
import math
import pandas as pd
import datetime
import requests
import urllib.request
import urllib.error
import urllib.parse
import requests
import itertools
from bs4 import BeautifulSoup
from selenium import webdriver
# from geo import *
import time
# from get_mapdata import *

# Chrome의 경우 | 아까 받은 chromedriver의 위치를 지정해준다.
driver = webdriver.Chrome('driver/chromedriver')

# PhantomJS의 경우 | 아까 받은 PhantomJS의 위치를 지정해준다.
# driver = webdriver.PhantomJS('driver/phantomjs')
# 암묵적으로 웹 자원 로드를 위해 3초까지 기다려 준다.
driver.implicitly_wait(3)




headers = {
    'user-agent': 'mozilla/5.0 (macintosh; intel mac os x 10_13_5) applewebkit/537.36 (khtml, like gecko) chrome/69.0.3497.100 safari/537.36'
}

# create lists for wanted data
keys = ['title', 'longitude', 'latitude']

blog_url_list = []
title = []
longitude = []
latitude = []

# create list for search start numbers
search_start_count = list(range(1, 1000, 10))

def get_search_url(start_date, end_date, page_num):
    search_url = "https://search.naver.com/search.naver?date_from=" + str(start_date) + "&date_option=8&date_to=" + str(end_date) + "&dup_remove=1&nso=p%3Afrom" + str(start_date) + "to" + str(end_date) + "&post_blogurl=&post_blogurl_without=&query=홍대%20카페&sm=tab_pge&srchby=all&st=sim&where=post&start=" + str(page_num)
    return search_url


def get_blog_post_url(search_url):
    driver.get(search_url)
    get_blog_post_content_text = driver.page_source
    # get_blog_post_content_text = get_blog_post_content_code.text
    get_blog_post_content_soup = BeautifulSoup(get_blog_post_content_text, 'lxml')
    # print(get_blog_post_content_soup)

    blog_url_list_draft = []
    blog_url_list = []

    for li in get_blog_post_content_soup.find_all(class_="thumb thumb-rollover"):
        blog_url_list_draft.append(li.a.get('href'))

    for url_ad_temp in blog_url_list_draft:
        url_ad = url_ad_temp.replace("?Redirect=Log&logNo=", "/")
        blog_url_list.append(url_ad)

    return blog_url_list


def get_map_data_up_ver(blog_url):
    driver.get(blog_url)
    get_blog_post_content_text = driver.page_source
    get_blog_post_content_soup = BeautifulSoup(get_blog_post_content_text, 'lxml')

    # get_blog_post_content_code = requests.get(blog_url)
    # get_blog_post_content_text = get_blog_post_content_code.text
    # get_blog_post_content_soup = BeautifulSoup(get_blog_post_content_text, 'lxml')

    for link in get_blog_post_content_soup.select('frame#mainFrame'):
        real_blog_post_url = "http://blog.naver.com" + link.get('src')
        driver.get(real_blog_post_url)
        get_real_blog_post_content_text = driver.page_source
        # get_blog_post_content_text = get_blog_post_content_code.text
        get_real_blog_post_content_soup = BeautifulSoup(get_real_blog_post_content_text, 'lxml')


        # Get map data
        blog_post_content = get_real_blog_post_content_soup.select('.se_caption_group.is-contact > a')

        # exception handling
        if not blog_post_content:
            pass
        else:
            for contents in blog_post_content:
                mappoition = contents.get('data-linkdata', None)

            # map data to json
            mapposition = json.loads(mappoition)

            # Add to lists by key
            key_num = 1
            for key in keys:
                if key_num == 1:
                    title.append(mapposition[key])
                elif key_num == 2:
                    longitude.append(mapposition[key])
                else:
                    latitude.append(mapposition[key])
                key_num = key_num+1


def get_map_data_down_ver(blog_url):
    driver.get(blog_url)
    get_blog_post_content_text = driver.page_source
    get_blog_post_content_soup = BeautifulSoup(get_blog_post_content_text, 'lxml')

    for link in get_blog_post_content_soup.select('frame#mainFrame'):
        step2_blog_post_url = "http://blog.naver.com" + link.get('src')
        # print("step2_blog_post_url : " + step2_blog_post_url)
        driver.get(step2_blog_post_url)

        get_step2_blog_post_content_text = driver.page_source
        get_step2_blog_post_content_soup = BeautifulSoup(get_step2_blog_post_content_text, 'lxml')

        for link in get_step2_blog_post_content_soup.select('#postViewArea iframe'):
            real_blog_post_url = link.get('src')

            driver.get(real_blog_post_url)

            get_real_blog_post_content_text = driver.page_source
            get_real_blog_post_content_soup = BeautifulSoup(get_real_blog_post_content_text, 'lxml')


            # Get map data
            blog_script_list = get_real_blog_post_content_soup.select('script')
            blog_script = str(blog_script_list[-2])
            blog_script = blog_script.replace("\\", "")
            pattern = re.compile("\\\"(\w+)\\\":\"(.*?)\"")
            map_dict = dict(re.findall(pattern, blog_script))
            # print(type(map_dict))
            # print(map_dict['centerX'])

            if not map_dict:
                pass
            else:
                longitude_data = map_dict['centerX']
                latitude_data = map_dict['centerY']

                title.append(map_dict['title'])
                longitude.append(longitude_data)
                latitude.append(latitude_data)


if __name__ == '__main__':
    for post_num in search_start_count:
        search_url = get_search_url(20151101, 20151130, post_num)
        blog_url_list.append(get_blog_post_url(search_url))


    blog_url_list = list(itertools.chain.from_iterable(blog_url_list))

    for blog_url in blog_url_list:
        try:
            time.sleep(1)
            get_map_data_down_ver(blog_url)
            get_map_data_up_ver(blog_url)
        except:
            pass


    # create dataframe for final data storage
    data = {'title':title, 'longitude':longitude, 'latitude':latitude}
    post_geo_data = pd.DataFrame(data)

    # Check data frames
    print(post_geo_data.head(20))

    # Export csv file
    post_geo_data.to_csv("data/hongdae/hongdae_2015_11.csv", mode='w')
