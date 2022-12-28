#!/usr/bin/env python

# https://pencilprogrammer.com/download-instagram-image-using-python/
# python script to download instagram image
import re
import sys
from datetime import datetime
from functools import lru_cache

from bs4 import BeautifulSoup
import requests
from instascrape import Reel
from selenium import webdriver
import time
import os

from foxylib.tools.version.version_tool import VersionTool


class InstagramTool:
    @classmethod
    @VersionTool.not_working(reason="result doesn't have session id anymore")
    def auth2sessionid(cls, username, password):
        # https://stackoverflow.com/questions/62799145/how-to-get-instagram-sessionid-using-python-requests
        link = 'https://www.instagram.com/accounts/login/'
        login_url = 'https://www.instagram.com/accounts/login/ajax/'

        time = int(datetime.now().timestamp())

        payload = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{password}',
            'queryParams': {},
            'optIntoOneTap': 'false'
        }

        with requests.Session() as s:
            r = s.get(link)
            csrf = re.findall(r"csrf_token\":\"(.*?)\"", r.text)[0]
            r = s.post(login_url, data=payload, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "https://www.instagram.com/accounts/login/",
                "x-csrftoken": csrf
            })
            print(r.status_code)
            print(r.url)
            print(r.text)

            print(s.cookies)

    @classmethod
    def url2video(cls, url, filepath, sessionid,):
        # Header with session id
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 \
            Safari/537.36 Edg/79.0.309.43",
            "cookie": f'sessionid={sessionid};'
        }

        # Passing Instagram reel link as argument in Reel Module
        insta_reel = Reel(
            url
            # 'https://www.instagram.com/p/CYlZaX4Fdjh/'
            # 'https://www.instagram.com/reel/CKWDdesgv2l/?utm_source=ig_web_copy_link'
        )

        # Using  scrape function and passing the headers
        insta_reel.scrape(headers=headers)

        # Giving path where we want to download reel to the
        # download function
        insta_reel.download(fp=filepath)

        # printing success Message
        print(f'{url}: Downloaded Successfully.')

    @classmethod
    @VersionTool.not_working(reason="no need to use this. use above other function")
    @lru_cache(maxsize=1)
    def driver(cls):
        # export CHROMEDRIVER_PATH=/Users/moonyoungkang/Downloads/chromedriver
        chromedriver_path = os.environ.get("CHROMEDRIVER_PATH")

        ''' 
        create a webdriver chrome object by passing the path of "chromedriver.exe" file.(do not include .exe in the path).
        '''
        driver = webdriver.Chrome(chromedriver_path)
        return driver

    @classmethod
    @VersionTool.not_working(reason="no need to use this. use above other function")
    def url2url_image(cls, url):
        driver = cls.driver()

        ''' Open the instagram post on your chrome browser'''
        driver.get(url)

        ''' Fetch the source file of the html page using BeautifulSoup'''
        soup = BeautifulSoup(driver.page_source, 'lxml')

        ''' Extract the url of the image from the source code'''
        img = soup.find('img', class_='FFVAD')
        url_image = img['src']

        return url_image

    @classmethod
    def url_image2file(cls, url_image, ofilepath):

        '''Download the image via the url using the requests library'''
        r = requests.get(url_image)

        with open(ofilepath, 'wb') as f:
            f.write(r.content)
