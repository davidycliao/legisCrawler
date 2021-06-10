#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------------------ #
# @author: davidycliao                                                                       #
# @email: davidycliao@gmail.com                                                              #
# @date: 9-May-2021                                                                          #
# @info: An Automation Webcrawling Toolkit for Taiwan Parliamentary Questions                #
# ------------------------------------------------------------------------------------------ #


import re
import time
import os
import random
import pandas as pd
import numpy as np
import itertools

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--start-maximized") #open Browser in maximized mode
options.add_argument("--no-sandbox") # bypass OS security model
options.add_argument("--disable-dev-shm-usage") #overcome limited resource problems
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

def main():
    term = input('Term :')
    # create a folder for restoring parliarmentary questions by individual legislator
    legislators = []
    with open("legislators/" + term + ".txt", "r") as f:
        for line in f:
            legislators.append(line.strip())

    dirName = term +'_term'
    try:
        os.makedirs(dirName)
        print("Directory " , dirName ,  " Created")
    except FileExistsError:
        print("Directory " , dirName ,  " already exists")

    for leg in legislators:

        # initiate a pandas dataframe
        df=pd.DataFrame(columns=['date', 'legislator', 'title', 'category','topic','keywords', 'ques_type', 'link_href'])

        # activate Chrome webdriver
        # driver = webdriver.Chrome('./chromedriver', options=options)
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

        driver.implicitly_wait(60)

        # click to the term 『立法菁英』
        driver.get('https://lis.ly.gov.tw/lylegismc/lylegismemkmout?@@0.6259989951044278')
        driver.find_element_by_xpath("""//*[@id="Map"]/area[1]""").click()

        # click to the term (屆)
        driver.find_element_by_link_text(term).click()

        # click to the legislator (立法委員)，and then activate new tab
        #driver.find_element_by_link_text(leg).click()
        driver.find_element_by_partial_link_text(leg).click()
        driver.switch_to.window(driver.window_handles[1])

        # click to『問政成果』
        driver.find_element_by_xpath("""//*[@id="menu02"]""").click()

        # click to『委員質詢』
        try:
            driver.find_element_by_xpath("""//*[@id="pop02"]/a""").click()
            # try 『專案質詢』 exist or not, and then click to『專案質詢』
            start_time = time.time()
            try:
                driver.find_element_by_link_text("專案質詢").click()
                for i in range(0,len(driver.find_elements_by_class_name("p_tab"))):
                    num_p_tab = driver.find_elements_by_class_name("p_tab")[i].text
                    m = re.match("專案質詢", driver.find_elements_by_class_name("p_tab")[i].text)
                    if m :
                        num_rows = int("".join([str(int) for int in [s for s in re.sub("專案質詢\\n\[",'', num_p_tab).split(']') if s.isdigit()]]))
                # click to row 『１』 to start
                driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr[3]/td[2]/table/tbody/tr[5]/td/table/tbody/tr/td/table/tbody/tr[2]/td[3]/a""").click()

                print(leg, 'has', num_rows, 'Q&As and is starting to be scraped at ',  time.strftime("%I %M %p",time.localtime(start_time)))
                print('------------------------------------------------------------------------------------------------------------')
                print('------------------------------------------------------------------------------------------------------------')
                # Here start to loop the each legislator in the list
                for i in range(1, num_rows + 1):
                    count = 0
                    # Type (1): The format of the table is 14 rows, the most common
                    # Example: 朱鳳芝, 7th, page 1
                    if len(driver.find_elements_by_class_name("rectr")) == 14:
                        if i == 1:
                            # scrape and save the legislator's 專案質詢 if number of 專案質詢 is equal to 1
                            try:
                                legislator = leg
                                title = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[4]/td[2]""").text
                                date = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[8]/td[2]""").text
                                ques_type = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]""").text
                                link_href = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/a""").get_attribute('href')
                                category = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[12]/td[2]""").text
                                topic=driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[13]/td[2]""").text
                                keywords=driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[14]/td[2]""").text
                                df.loc[i] = [date, legislator, title, category, topic, keywords, ques_type, link_href]
                                # next page
                                try:
                                    driver.implicitly_wait(60)
                                    driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr/td[2]/input[2]""").click()
                                    # print  Type (1)  elif i == 1 and continue loop
                                    print("Format Type (1)", leg, 'at page', i, 'as titled', title[:15], 'is webscraped!!')
                                except NoSuchElementException:
                                    # print  Type (1)  elif i == 1 as legislator only has one 「專案質詢」 and break loop due to last iteration
                                    print(leg, "only has", i, "『專案質詢』")
                                    break
                            except NoSuchElementException as e:
                                # save current scraped data from TRY at line 46
                                count += 1
                                df.loc[i] = [date, legislator, title, category, topic, keywords, ques_type, link_href]
                                print(e, "Something wrong with the page", i, "Potential Error UP!! at line 77")
                                break
                        elif i > 1:
                            try:
                                legislator = leg
                                title = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[4]/td[2]""").text
                                date = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[8]/td[2]""").text
                                ques_type = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]""").text
                                link_href = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/a""").get_attribute('href')
                                category = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[12]/td[2]""").text
                                topic=driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[13]/td[2]""").text
                                keywords=driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[14]/td[2]""").text
                                df.loc[i] = [date, legislator, title, category, topic, keywords, ques_type, link_href]
                                # next page
                                try:
                                    driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr/td[2]/input[3]""").click()
                                    driver.implicitly_wait(60)
                                    # print fianl Type (1)  elif i > 1 and continue
                                    print("Format Type (1)", leg, 'at page', i, 'as titled', title[:15], 'is webscraped!!')
                                except NoSuchElementException:
                                    # print final Type (1)  elif i > 1 and break loop due to last iteration
                                    print("Format Type (1)", leg, 'at page', i, 'as titled', title[:15], 'is webscraped!!')
                                    break
                            except NoSuchElementException as e:
                                count += 1
                                print(e,  "Something wrong with the page", i, "Potential Error UP!! at line 102")
                                df.loc[i] = [date, legislator, title, category, topic, keywords, ques_type, link_href]
                                break

                    # Type (2): the format of the table is 13 rows
                    # Example: 丁守中, Term 3, Page 1
                    elif len(driver.find_elements_by_class_name("rectr")) == 13:
                    # elif driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[11]/td[1]/nobr""").text == '類別':
                        if i == 1:
                            # scrape and save the legislator's 專案質詢 if number of 專案質詢 is equal to 1
                            try:
                                legislator = leg
                                title = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[4]/td[2]""").text
                                date = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[8]/td[2]""").text
                                ques_type = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]""").text
                                link_href = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/a""").get_attribute('href')
                                category = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[11]/td[2]""").text
                                topic=driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[12]/td[2]""").text
                                keywords=driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[13]/td[2]""").text
                                df.loc[i] = [date, legislator, title, category, topic, keywords, ques_type, link_href]
                                # next page
                                try:
                                    driver.implicitly_wait(60)
                                    driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr/td[2]/input[2]""").click()
                                    # print  Type (2)  elif i == 1 and continue loop
                                    print("Format Type (2)", leg, 'at page', i, 'as titled', title[:15], 'is webscraped!!')
                                except NoSuchElementException:
                                    # print  Type (2)  elif i == 1 as legislator only has one 「專案質詢」 and break loop due to last iteration
                                    print(leg, "only has", i, "『專案質詢』")
                                    break
                            except NoSuchElementException as e:
                                # save current scraped data from TRY at line 46
                                df.loc[i] = [date, legislator, title, category, topic, keywords, ques_type, link_href]
                                print(e,"Something wrong with the page", i, "Potential Error UP!! at line 135")
                                break
                        elif i > 1:
                            try:
                                legislator = leg
                                title = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[4]/td[2]""").text
                                date = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[8]/td[2]""").text
                                ques_type = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]""").text
                                link_href = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/a""").get_attribute('href')
                                category = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[11]/td[2]""").text
                                topic=driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[12]/td[2]""").text
                                keywords=driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[13]/td[2]""").text
                                df.loc[i] = [date, legislator, title, category, topic, keywords, ques_type, link_href]
                                # next page
                                try:
                                    driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr/td[2]/input[3]""").click()
                                    driver.implicitly_wait(60)
                                    # print final Type (2)  elif i > 1 and continue
                                    print("Format Type (2)", leg, 'at page', i, 'as titled', title[:15], 'is webscraped!!')
                                except NoSuchElementException:
                                    # print fianl Type (2)  elif i > 1 and break loop due to last iteration
                                    print("Format Type (2)", leg, 'at page', i, 'as titled', title[:15], 'is webscraped!!')
                                    break
                            except NoSuchElementException as e:
                                count += 1
                                print(e,  "Something wrong with the page", i,  "Potential Error UP!! at line 160")
                                df.loc[i] = [date, legislator, title, category, topic, keywords, ques_type, link_href]
                                break

                    # Type (3): the format of the table is 12 rows
                    elif len(driver.find_elements_by_class_name("rectr")) == 12:
                        try:
                            if i == 1:
                                # scrape and save the legislator's 專案質詢 if number of 專案質詢 is equal to 1
                                try:
                                    legislator = leg
                                    title = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[4]/td[2]""").text
                                    date = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[8]/td[2]""").text
                                    ques_type = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]""").text
                                    link_href = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/a""").get_attribute('href')
                                    category = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[10]/td[2]""").text
                                    topic=driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[11]/td[2]""").text
                                    keywords=driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[12]/td[2]""").text
                                    df.loc[i] = [date, legislator, title, category, topic, keywords, ques_type, link_href]
                                    # next page
                                    try:
                                        driver.implicitly_wait(60)
                                        driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr/td[2]/input[2]""").click()
                                        # print  Type (3)  elif i == 1 and continue loop
                                        print("Format Type (1)", leg, 'at page', i, 'as titled', title[:15], 'is webscraped!!')

                                    except NoSuchElementException:
                                        # print  Type (3)  elif i > 1  as legislator only has one 「專案質詢」 and break the loop due to last iteration.
                                        print(leg, "only has", i, "『專案質詢』")
                                        break
                                except NoSuchElementException as e:
                                    count += 1
                                    df.loc[i] = [date, legislator, title, category, topic, keywords, ques_type, link_href]
                                    print(e, "Something wrong with the page", i, "Potential Error UP at line 220")
                                    break

                            else :
                                try:
                                    legislator = leg
                                    title = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[4]/td[2]""").text
                                    date = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[8]/td[2]""").text
                                    ques_type = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]""").text
                                    link_href = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/a""").get_attribute('href')
                                    category = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[10]/td[2]""").text
                                    topic=driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[11]/td[2]""").text
                                    keywords=driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[12]/td[2]""").text
                                    df.loc[i] = [date, legislator, title, category, topic, keywords, ques_type, link_href]
                                    # next page
                                    try:
                                        driver.implicitly_wait(60)
                                        driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr/td[2]/input[3]""").click()
                                        # print final Type (3)  elif i > 1 ann continue the loop
                                        print("Format Type (3): 「答覆：未答」。 「答復日期」 and 「答復」 are excluded.", leg,
                                              'at page', i, 'as titled', title[:15], 'is webs scraped!!')
                                    except NoSuchElementException:
                                        # print final Type (3)  elif i > 1 and break the loop due to last iteration.
                                        print("Format Type (3): 「答覆：未答」。 「答復日期」 and 「答復」 are excluded.", leg, 'at page', i, 'as titled', title[:15], 'is webscraped!!')
                                        break

                                except NoSuchElementException as e:
                                    count += 1
                                    df.loc[i] = [date, legislator, title, category, topic, keywords, ques_type, link_href]
                                    print(e, "Something wrong with the page", i,  "Potential Error UP at line 247")
                                    break

                        except NoSuchElementException as e:
                            count += 1
                            print(e, "Something wrong with the page", i, " loading", "Potential Error UP  at line 254")
                            df.loc[i] = [date, legislator, title, category, topic, keywords, ques_type, link_href]
                            break

                    # Type (6): the format change: the number of the table is 11 rows
                    # Example: 徐中雄, 4 term, page 1
                    #elif len(driver.find_elements_by_class_name("rectr")) == 11:
                    elif driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[9]/td[1]""").text == '類別':
                        try:
                            if i == 1:
                                # scrape and save the legislator's 專案質詢 if number of 專案質詢 is equal to 1
                                try:
                                    driver.implicitly_wait(60)
                                    legislator = leg
                                    title = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[4]/td[2]""").text
                                    date = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[6]/td[2]""").text
                                    ques_type = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]""").text
                                    link_href = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/a""").get_attribute('href')
                                    category = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[9]/td[2]""").text
                                    topic=driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[10]/td[2]""").text
                                    keywords=driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[11]/td[2]""").text
                                    df.loc[i] = [date, legislator, title, category, topic, keywords, ques_type, link_href]
                                    # next page
                                    try:
                                        driver.implicitly_wait(60)
                                        driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr/td[2]/input[2]""").click()
                                        print("Format Type (6): number of rows, 11", leg, 'at page', i, 'as titled', title[:15], 'is webscraped!!')
                                    except NoSuchElementException:
                                        # print final Type (6)  elif i > 1  as legislator only has one 專案質詢
                                        print(leg, "only has", i , "『專案質詢』")
                                        break

                                except NoSuchElementException as e:
                                    count += 1
                                    df.loc[i] = [date, legislator, title, category, topic, keywords, ques_type, link_href]
                                    print(e, "Something wrong with the page", i,  "Potential Error UP!! at line 289")
                                    break

                            elif i >1:
                                try:
                                    legislator = leg
                                    title = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[4]/td[2]""").text
                                    date = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[6]/td[2]""").text
                                    ques_type = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]""").text
                                    link_href = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/a""").get_attribute('href')
                                    category = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[9]/td[2]""").text
                                    topic=driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[10]/td[2]""").text
                                    keywords=driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[11]/td[2]""").text
                                    df.loc[i] = [date, legislator, title, category, topic, keywords, ques_type, link_href]
                                    # next page
                                    try:
                                        driver.implicitly_wait(60)
                                        driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr/td[2]/input[3]""").click()
                                        # print final Type (6)  elif i > 1
                                        print("Format Type (6): number of rows, 11", leg, 'at page', i, 'as titled', title[:15], 'is webscraped!!')
                                    except NoSuchElementException:
                                        # print final Type (6)  elif i > 1
                                        print("Format Type (6):number of rows, 11", leg, 'at page', i, 'as titled', title[:15], 'is webscraped!!')
                                        break
                                except NoSuchElementException as e:
                                    count += 1
                                    df.loc[i] = [date, legislator, title, category, topic, keywords, ques_type, link_href]
                                    print(e, "Something wrong with the page", i, "Potential Error UP!! at line 316")
                                    break
                        except NoSuchElementException as e:
                            count += 1
                            print(e, "Something wrong with the page", i," loading", "Potential Error UP!! at line 447")
                            df.loc[i] = [date, legislator, title, category, topic, keywords, ques_type, link_href]
                            break
                    # Type (4): the format change: the number of the table is 15 rows
                    # 多「機關名稱」 at row 14  before「關鍵字」
                    elif driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[14]/td[1]/nobr""").text == '機關名稱':
                        try:
                            if i == 1:
                                # scrape and save the legislator's 專案質詢 if number of 專案質詢 is equal to 1
                                try:
                                    legislator = leg
                                    title = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[4]/td[2]""").text
                                    date = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[8]/td[2]""").text
                                    ques_type = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]""").text
                                    link_href = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/a""").get_attribute('href')
                                    category = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[12]/td[2]""").text
                                    topic=driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[13]/td[2]""").text
                                    keywords=driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[15]/td[2]""").text
                                    df.loc[i] = [date, legislator, title, category, topic, keywords, ques_type, link_href]
                                    # next page
                                    try:
                                        driver.implicitly_wait(60)
                                        driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr/td[2]/input[2]""").click()
                                        print("Format Type (4): number of rows, 15, 多「機關名稱」", leg, 'at page', i, 'as titled', title[:15], 'is webscraped!!')
                                    except NoSuchElementException:
                                        # print final Type (4)  elif i > 1  as legislator only has one 專案質詢
                                        print(leg, "only has", i, "『專案質詢』")
                                        break

                                except NoSuchElementException as e:
                                    count += 1
                                    df.loc[i] = [date, legislator, title, category, topic, keywords, ques_type, link_href]
                                    print(e, "Something wrong with the page", i, "Potential Error UP!! at line 353")
                                    break

                            elif i >1 :
                                try:
                                    legislator = leg
                                    title = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[4]/td[2]""").text
                                    date = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[8]/td[2]""").text
                                    ques_type = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]""").text
                                    link_href = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/a""").get_attribute('href')
                                    category = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[12]/td[2]""").text
                                    topic=driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[13]/td[2]""").text
                                    keywords=driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[15]/td[2]""").text
                                    df.loc[i] = [date, legislator, title, category, topic, keywords, ques_type, link_href]
                                    # next page
                                    try:
                                        driver.implicitly_wait(60)
                                        driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr/td[2]/input[3]""").click()
                                        # print  Type (4)  elif i > 1 and continue the loop
                                        print("Format Type (4): number of rows, 15, 多「機關名稱」", leg, 'at page', i, 'as titled', title[:15], 'is webscraped!!')
                                    except NoSuchElementException:
                                        # print  Type (4)  elif i > 1 and break the loop due to last iteration
                                        print("Format Type (4): number of rows, 15, 多「機關名稱」", leg, 'at page', i, 'as titled', title[:15], 'is webscraped!!')
                                        break
                                except NoSuchElementException as e:
                                    count += 1
                                    df.loc[i] = [date, legislator, title, category, topic, keywords, ques_type, link_href]
                                    print(e, "Something wrong with the page", i, "Potential Error UP at line 379")
                                    break

                        except NoSuchElementException as e:
                            count += 1
                            print(e, "Something wrong with the page", i," loading", "Potential Error UP!! at line 317")
                            df.loc[i] = [date, legislator, title, category, topic, keywords, ques_type, link_href]
                            break

                    # Type (5): the format change: the number of the table is 15 rows,「答復人」 at row 7
                    # Example: 孔文吉, 9 term, page 1
                    elif driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[7]/td[1]""").text == '答復人':
                        try:
                            if i == 1:
                                # scrape and save the legislator's 專案質詢 if number of 專案質詢 is equal to 1
                                try:
                                    legislator = leg
                                    title = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[4]/td[2]""").text
                                    date = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[9]/td[2]""").text
                                    ques_type = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]""").text
                                    link_href = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/a""").get_attribute('href')
                                    category = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[13]/td[2]""").text
                                    topic=driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[14]/td[2]""").text
                                    keywords=driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[15]/td[2]""").text
                                    df.loc[i] = [date, legislator, title, category, topic, keywords, ques_type, link_href]
                                    # next page
                                    try:
                                        driver.implicitly_wait(60)
                                        driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr/td[2]/input[2]""").click()
                                        print("Format Type (5): number of rows, 15, 多「答復人」", leg, 'at page', i, 'as titled', title[:15], 'is webscraped!!')
                                    except NoSuchElementException:
                                        # print final Type (5)  elif i > 1  as legislator only has one 專案質詢
                                        print(leg, "only has", i , "『專案質詢』")
                                        break

                                except NoSuchElementException as e:
                                    count += 1
                                    df.loc[i] = [date, legislator, title, category, topic, keywords, ques_type, link_href]
                                    print(e, "Something wrong with the page", i, "Potential Error UP at line 417")
                                    break

                            elif i >1 :
                                try:
                                    legislator = leg
                                    title = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[4]/td[2]""").text
                                    date = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[9]/td[2]""").text
                                    ques_type = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]""").text
                                    link_href = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/a""").get_attribute('href')
                                    category = driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[13]/td[2]""").text
                                    topic=driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[14]/td[2]""").text
                                    keywords=driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[15]/td[2]""").text
                                    df.loc[i] = [date, legislator, title, category, topic, keywords, ques_type, link_href]
                                    # next page
                                    try:
                                        driver.implicitly_wait(60)
                                        driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr/td[2]/input[3]""").click()
                                        # print final Type (5)  elif i > 1
                                        print("Format Type (5): number of rows, 15, 多「答復人」", leg, 'at page', i, 'as titled', title[:15], 'is webscraped!!')
                                    except NoSuchElementException:
                                        # print final Type (5)  elif i > 1
                                        print("Format Type (5): number of rows, 15, 多「答復人」", leg, 'at page', i, 'as titled', title[:15], 'is webscraped!!')
                                        break
                                except NoSuchElementException as e:
                                    count += 1
                                    df.loc[i] = [date, legislator, title, category, topic, keywords, ques_type, link_href]
                                    print(e,"Something wrong with the page", i, "Potential Error UP!! at line 444")
                                    break

                        except NoSuchElementException as e:
                            count += 1
                            print(e, "Something wrong with the page", i," loading", "Potential Error UP!! at line 449")
                            df.loc[i] = [date, legislator, title, category, topic, keywords, ques_type, link_href]
                            break

                    # out of table's range
                    else:
                        count += 1
                        driver.implicitly_wait(60)
                        driver.find_element_by_xpath("""/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr/td[2]/input[2]""").click()
                        print(leg, "at page", i, "is not being included. at line 458")

                # store scraped data from for-loop
                df.to_csv(dirName + "/" + leg + "_" + term +".csv")
                print(leg, "has", "green", num_rows, "Q&As and ", count, "failure.")

            except NoSuchElementException:
                # empty data when clicking to 『專案質詢』
                df = pd.DataFrame(columns = ['date', 'legislator', 'title', 'category','topic','keywords', 'ques_type', 'link_href'],
                                  data = np.array([[0, leg, 0, 0, 0, 0, 0, 0]]))
                df.to_csv(dirName + "/" + leg + "_" + term +".csv")
                # final print
                print(leg, "has no 『專案質詢』")

        except NoSuchElementException:
            # empty data when clicking to 『委員質詢』
            df = pd.DataFrame(columns = ['date', 'legislator', 'title', 'category','topic','keywords', 'ques_type', 'link_href'],
                              data = np.array([[0, leg, 0, 0, 0, 0, 0, 0]]))
            df.to_csv(dirName + "/" + leg + "_" + term + ".csv")
            # final print
            print(leg, "has no 『專案質詢』 as clicking to 『委員質詢』")

        # close Chrome's browser
        print(leg, 'is completed', 'time spent:', (time.strftime("%I %M %p",time.localtime(time.time() - start_time))))
        print('------------------------------------------------------------------------------------------------------------')

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        driver.quit()



if __name__ == '__main__': main()