# Import Libraries
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import numpy as np
from random import randint

# Import Queries for each topic
"""
Topic Name
sub-Query 1
Query 1
sub-Query 2
Query 2
"""
def readLines(filepath):
    lines = []
    with open(filepath, 'r') as file:
        for line in file:
            lines.append(line.replace('\n', ''))
    return lines

# Retrieve results for the current search engine's page
def retrievePageResults(browser):
    results_list = []
    results = browser.find_elements_by_css_selector('div.g')
    for j in range(len(results)):
        link = results[j].find_element_by_tag_name("a")
        href = link.get_attribute("href")[:60]
        results_list.append(href)   
    return results_list

# Open Browser
# Enter query on google's search engine
# Retrieve results for the first X pages (adjust max_pages variable)
# Quit Browser
def googleSearch(query, browser, choice = 'Mozilla'):
    max_pages = 3 # Change this variable to retrieve more pages
    browser.get('http://www.google.com')
    search = browser.find_element_by_name('q')
    search.send_keys(query + Keys.RETURN)
    results_list = []
    for i in range(max_pages):
        time.sleep(randint(2, 10))  
        try:
            if choice == 'Mozilla':
                browser.find_element_by_css_selector('#nav > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(' + str(i+3) + ') > a:nth-child(1)')
            elif choice == 'Chrome':
                browser.find_element_by_css_selector('#nav > tbody > tr > td:nth-child(' + str(i+3) + ') > a')
        except:
            input('System Paused')
        results_list += retrievePageResults(browser)
        # Move to next page
        if choice == 'Mozilla':
            browser.find_element_by_css_selector('#nav > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(' + str(i+3) + ') > a:nth-child(1)').click()
        elif choice == 'Chrome':
            browser.find_element_by_css_selector('#nav > tbody > tr > td:nth-child(' + str(i+3) + ') > a').click()
    time.sleep(randint(2, 10))
    return results_list

# Print in the console the retrieved dictionary
"""
{topic_1:
    {query_1: 
        [result_1], [result_2], ..., [result_n]
    },
    {query_2: 
        [result_1], [result_2], ..., [result_n]
    },
    {query_3: 
        [result_1], [result_2], ..., [result_n]
    },
    {query_4: 
        [result_1], [result_2], ..., [result_n]
    },
},
{topic_2:
    {query_1: 
        [result_1], [result_2], ..., [result_n]
    },
    {query_2: 
        [result_1], [result_2], ..., [result_n]
    },
    {query_3: 
        [result_1], [result_2], ..., [result_n]
    },
    {query_4: 
        [result_1], [result_2], ..., [result_n]
    },
},
...,
{topic_n:
    {query_1: 
        [result_1], [result_2], ..., [result_n]
    },
    {query_2: 
        [result_1], [result_2], ..., [result_n]
    },
    {query_3: 
        [result_1], [result_2], ..., [result_n]
    },
    {query_4: 
        [result_1], [result_2], ..., [result_n]
    },
}
"""
def printResults(results):
    for key in results.keys():
        print(key)
        for key2 in results[key].keys():
            print(key2)
            for page in results[key][key2]:
                print(page)

# Generate country_name_player.csv file based on a nested dictionary
# Outer key as index, inner keys as columns
def exportResults(results, country_name, player, part):
    if not os.path.exists('PartialResults'):
        os.mkdir('PartialResults')
    path = os.path.join(os.getcwd(), './PartialResults/')
    df = pd.DataFrame.from_dict(results, orient='index')
    df.to_csv(path + country_name + '_' + str(player) + ('_a.csv' if part == 1 else '_b.csv'), encoding='utf-8')

def openBrowser(choice = 'Mozilla'):
    if choice == 'Mozilla':
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
        browser = webdriver.Firefox(executable_path='./Drivers/geckodriver', firefox_profile=firefox_profile)
    elif choice == 'Chrome':
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--icognito")
        browser = webdriver.Chrome(executable_path='./Drivers/chromedriver.exe', options=chrome_options)
    time.sleep(randint(2,10))
    return browser

def quitBrowser(browser):
    browser.quit()
    time.sleep(randint(2,10))

# Import Topics and Queries from each topic based on specific file
def getFileToImportInput():
    file_to_read = ''
    while not (file_to_read.endswith('.txt') and os.path.isfile(os.path.join(os.getcwd(), './Input/' + file_to_read))):
        if file_to_read != '':
            print('Something went terribly wrong.\nMake sure there is a file with this name and this extension in \"' + os.getcwd() + '\\Input\"')
        file_to_read = input('Queries text file:\n(i.e. test.txt)\n').strip()
    return os.path.join(os.getcwd(), './Input/' + file_to_read)

# Variable Country
def getCountryNameInput():
    country_dict = { 1 : 'France', 2 : 'UK', 3: 'Netherlands'}
    country_code = -1
    print("Country Code".ljust(20), "Country Name")
    for key,val in country_dict.items():
        print(str(key).ljust(20), str(val))
    while country_code not in country_dict.keys():
        if country_code != -1:
            print('Wrong Input.\nExpected value would be in range ' + str(min(country_dict.keys())) + ' and ' + str(max(country_dict.keys())) + '.')
        try:
            country_code = int(input('Give the corresponding country\'s number:\n'))
        except ValueError:
            print('Not an Integer.')
    return country_dict.get(country_code)

# Variable Player
def getPlayerInput():
    player = -1
    while player != 1 and player != 2:
        if player != -1:
            print('Wrong Input.\nJust press \"1\" or \"2\" for god\'s sake!')
        try:
            player = int(input('Player 1 or 2?\n'))
        except ValueError:
            print('Not an Integer.')
    return player

# Variable Part
def getPartInput():
    part = -1
    while part != 1 and part != 2:
        if part != -1:
            print('Wrong Input.\nExpecting  \"1\" or \"2\"  as input.')
        try:
            part = int(input('Part 1 or 2?\n\"1\": First 10 Topics\n\"2\": Next 10 Topics\n'))
        except ValueError:
            print('Not an Integer.')
    return part

if __name__ == '__main__':
    file_to_read = getFileToImportInput()
    country = getCountryNameInput()
    player = getPlayerInput()
    part = getPartInput() 
    # Run Script for the first or the second half of the queries located in the .txt file
    topics_n_queries = readLines(file_to_read)[(part*10-10)*5:(part*10)*5]
    # Begin search
    results = {}
    for i, line in enumerate(topics_n_queries):
        if i%5 == 0:
            topic = line
            results[topic] = {}
            browser = openBrowser()
        if i%5 == 1 and player == 1:
            results[list(results.keys())[-1]]['sub-Query 1'] = googleSearch(line, browser)
        if i%5 == 2:
            results[list(results.keys())[-1]]['Query 1'] = googleSearch(line, browser) 
            time.sleep(60*30)
            browser.quit()
            browser = openBrowser()
        if i%5 == 3 and player == 2:
            results[list(results.keys())[-1]]['sub-Query 2'] = googleSearch(line, browser)
        if i%5 == 4:
            results[list(results.keys())[-1]]['Query 2'] = googleSearch(line, browser)
            time.sleep(60*30)
            browser.quit()
    printResults(results)
    exportResults(results, country, player, part)