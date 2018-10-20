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
from bs4 import BeautifulSoup

# 네이버 애플리케이션 client id와 secret을 입력
naver_client_id = "QrFzh6XCf07LBOLFJ2sm"
naver_client_secret = "A9TgKq9anF"



#mapdata = []

keys = ['title', 'longitude', 'latitude']

#datetime = []
title = []
longitude = []
latitude = []

def naver_blog_crawling(search_blog_keyword, display_count, sort_type):
    search_result_blog_page_count = get_blog_search_result_pagination_count(search_blog_keyword, display_count)
    get_blog_post(search_blog_keyword, display_count, search_result_blog_page_count, sort_type)


def get_blog_search_result_pagination_count(search_blog_keyword, display_count):
    encode_search_keyword = urllib.parse.quote(search_blog_keyword)
    url = "https://openapi.naver.com/v1/search/blog?query=" + encode_search_keyword
    request = urllib.request.Request(url)

    request.add_header("X-Naver-Client-Id", naver_client_id)
    request.add_header("X-Naver-Client-Secret", naver_client_secret)

    response = urllib.request.urlopen(request)
    response_code = response.getcode()

    if response_code is 200:
        response_body = response.read()
        response_body_dict = json.loads(response_body.decode('utf-8'))

        if response_body_dict['total'] == 0:
            blog_pagination_count = 0
        else:
            blog_pagination_total_count = math.ceil(response_body_dict['total'] / int(display_count))

            if blog_pagination_total_count >= 1000:
                blog_pagination_count = 1000
            else:
                blog_pagination_count = blog_pagination_total_count

            # 키워드에 대한 기본 정보 반환
            print("키워드 " + search_blog_keyword + "에 해당하는 포스팅 수 : " + str(response_body_dict['total']))

        return blog_pagination_count

def get_blog_post(search_blog_keyword, display_count, search_result_blog_page_count, sort_type):
    encode_search_blog_keyword = urllib.parse.quote(search_blog_keyword)



    for i in range(1, search_result_blog_page_count + 1):
        url = "https://openapi.naver.com/v1/search/blog?query=" + encode_search_blog_keyword + "&display=" + str(
            display_count) + "&start=" + str(i) + "&sort=" + sort_type

        request = urllib.request.Request(url)

        request.add_header("X-Naver-Client-Id", naver_client_id)
        request.add_header("X-Naver-Client-Secret", naver_client_secret)

        response = urllib.request.urlopen(request)
        response_code = response.getcode()

        if response_code is 200:
            response_body = response.read()
            response_body_dict = json.loads(response_body.decode('utf-8'))

            for j in range(0, len(response_body_dict['items'])):
                try:
                    blog_post_url = response_body_dict['items'][j]['link'].replace("amp;", "")

                    get_blog_post_content_code = requests.get(blog_post_url)
                    get_blog_post_content_text = get_blog_post_content_code.text

                    get_blog_post_content_soup = BeautifulSoup(get_blog_post_content_text, 'lxml')

                    for link in get_blog_post_content_soup.select('frame#mainFrame'):
                        real_blog_post_url = "http://blog.naver.com" + link.get('src')

                        get_real_blog_post_content_code = requests.get(real_blog_post_url)
                        get_real_blog_post_content_text = get_real_blog_post_content_code.text

                        get_real_blog_post_content_soup = BeautifulSoup(get_real_blog_post_content_text, 'lxml')

                        # 지리 정보
                        # 게시글 마다 반복
                        for blog_post_content in get_real_blog_post_content_soup.select('.se_caption_group.is-contact > a'):
                            mapposition = blog_post_content.get('data-linkdata', None)
                            mapposition = json.loads(mapposition)

                            # key별로 리스트에 담기
                            i = 1
                            for key in keys:
                                # # Print map data with key
                                # print(key.upper(), ':', mapposition[key])

                                if i == 1:
                                    title.append(mapposition[key])
                                elif i == 2:
                                    longitude.append(mapposition[key])
                                else:
                                    latitude.append(mapposition[key])

                                i = i+1

                except:
                    j += 1


if __name__ == '__main__':
    # 검색하고 싶은 키워드, 한 페이지당 표출할 개수, 정렬순서(sim;유사도순, date;날짜순)
    naver_blog_crawling("파이썬 컨벤션", 100, "date")
    data = {'title':title, 'longitude':longitude, 'latitude':latitude}
    df = pd.DataFrame(data)
    print(df.head(5))

    # df.to_csv("mapdata.csv", mode='w')
