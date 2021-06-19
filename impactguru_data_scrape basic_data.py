#!/usr/bin/env python
__author__ = "Ashutosh Mishra"
__copyright__ = "Copyright 2021, ImpactGuru_Sample_Project"
__credits__ = ["Ashutosh Mishra"]
__code_name__ = "impact_guru_fundraiser_basic_data_scraper"
__version__ = "1.0"
__maintainer__ = "Ashutosh Mishra"
__status__ = "Production"

#loading packages#
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
import os
from datetime import datetime
import urllib3
from selenium.webdriver.support.ui import Select
import requests
from lxml import html
import itertools
import random
from selenium.webdriver.common.action_chains import ActionChains

urllib3.disable_warnings()
dir_path = os.path.dirname(os.path.realpath(__file__))
chrome_driver = dir_path + r'\webdriver\chromedriver'

url = 'https://www.impactguru.com/fundraisers'

class Fundraiser:

    def __init__(self):
        self.output_dict = {'Section_Name':[],'Campaign_Title':[],'Campaign_By':[],
                            'Funds_Raised':[],'Campaign_URL':[]}

    def data_scraper(self,temp_sections_type):
        driver = webdriver.Chrome(chrome_driver)
        driver.get(url)
        driver.maximize_window()
        sections_type = temp_sections_type
        for sections in sections_type:
            print(f'\nProcessing :- {sections}\n')
            try:
                driver.find_element_by_link_text(sections).click()
                time.sleep(5)
                try:
                    while True:
                        driver.find_element_by_id('loadMoreBtn').click()
                        time.sleep(4)
                except:
                    pass
                response = driver.page_source
                main_page = bs(response, 'html.parser')
                body_sections = main_page.find_all('div', {'class': 'card-body'})
                for body in body_sections:
                    campaign_title = body.find('h5', {'class': 'card-h-text'}).text
                    campaign_by_temp = body.find('p', {'class': 'card-text'}).text
                    campaign_by = str(campaign_by_temp).replace('by ','')
                    campaign_url = body.find('a')['href']
                    campaign_money_raised = body.find('span', {'class': 'price-b'}).text

                    self.output_dict['Section_Name'].append(sections)
                    self.output_dict['Campaign_Title'].append(campaign_title)
                    self.output_dict['Campaign_By'].append(campaign_by)
                    self.output_dict['Campaign_URL'].append(campaign_url)
                    self.output_dict['Funds_Raised'].append(campaign_money_raised)

            except Exception as ex:
                print(ex)

        driver.quit()
        print('\nScraping successful\n')

    #function for writing output data#
    def write_output(self):
        df = pd.DataFrame(self.output_dict)
        now = datetime.now().strftime("_%d_%b_%y_%I_%M_%p")
        writer = pd.ExcelWriter(dir_path + '\Output\Impact_Guru_basic_data' + str(now) + '.xlsx')
        df.to_excel(writer, 'Output', index=False)
        writer.save()

if __name__ == '__main__':
    start_time = time.time()
    fund_obj = Fundraiser()
    sections_type = ['Medical','NGO','Personal Cause','Creative Ideas','Acid Attacks']
    fund_obj.data_scraper(sections_type)
    fund_obj.write_output()
    print(f'\nExecution time: {(time.time() - start_time) / 60} minutes')