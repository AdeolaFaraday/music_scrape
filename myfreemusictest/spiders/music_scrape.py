import time
import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from shutil import which
import os


class MusicScrapeSpider(scrapy.Spider):
    name = 'music_scrape'
    allowed_domains = ['myfreemp3juices.cc']
    start_urls = ['https://myfreemp3juices.cc/']

    def parse(self, response):
        chrome_options = Options()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_PATH")
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-sh-usage')
        chrome_path = which("chromedriver")
        driver = webdriver.Chrome(
            executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
        driver.set_window_size(1920, 1080)
        driver.get("https://myfreemp3juices.cc/")

        search_input = driver.find_element_by_xpath("//input[@id='query']")

        search_input.send_keys("burna boy dangote")

        search_input.send_keys(Keys.ENTER)

        time.sleep(3.5)

        music_tiles = driver.find_elements_by_xpath(
            "//li[@class='list-group-item']")

        for music_tile in music_tiles:
            yield {
                'download_link': music_tile.find_element_by_xpath("./a[@title='Download']").get_attribute('href'),
                'music_title': [music.text for music in music_tile.find_elements_by_xpath("./a[@id='navi']")],
                'music_duration': music_tile.find_element_by_xpath("./div/a[@class='btn btn-primary btn-xs']").text
            }
