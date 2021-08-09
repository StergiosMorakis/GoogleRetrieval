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

def read_lines(filepath):
    lines = []
    with open(filepath, 'r') as file:
        for line in file:
            lines.append(line.replace('\n', ''))
    return lines

def retrieve_page_results(browser):
    ''' retrieve results for the current search engine's page
    '''
    results_list = []
    results = browser.find_elements_by_css_selector('div.g')
    for j in range(len(results)):
        link = results[j].find_element_by_tag_name("a")
        href = link.get_attribute("href")[:60]
        results_list.append(href)   
    return results_list

def google_search(
    query: str,
    browser: object,
    choice: str = 'mozilla',
    max_pages: int = 3          # change this variable to retrieve more pages
):
    ''' steps:
        1. open browser
        2. enter query on google's search engine
        3. retrieve results for the first X pages (adjust max_pages variable)
        4. quit Browser
    '''
    browser.get('http://www.google.com')
    search = browser.find_element_by_name('q')
    search.send_keys(query + Keys.RETURN)
    results_list = []
    for i in range(max_pages):
        time.sleep(randint(2, 10))  
        try:
            if choice == 'mozilla':
                browser.find_element_by_css_selector('#nav > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(' + str(i+3) + ') > a:nth-child(1)')
            elif choice == 'chrome':
                browser.find_element_by_css_selector('#nav > tbody > tr > td:nth-child(' + str(i+3) + ') > a')
        except:
            input('System Paused')
        results_list += retrieve_page_results(browser)
        # Move to next page
        if choice == 'mozilla':
            browser.find_element_by_css_selector('#nav > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(' + str(i+3) + ') > a:nth-child(1)').click()
        elif choice == 'chrome':
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
def print_results(results: dict, verbode: bool = True):
    if verbose:
        for key in results.keys():
            print(key)
            for key2 in results[key].keys():
                print(key2)
                for page in results[key][key2]:
                    print(page)

# Generate country_name_player.csv file based on a nested dictionary
# Outer key as index, inner keys as columns
def export_results(results: dict, country_name: str, player: int, part: int):
    if not os.path.exists('PartialResults'):
        os.mkdir('PartialResults')
    path = os.path.join(os.getcwd(), './PartialResults/')
    df = pd.DataFrame.from_dict(results, orient='index')
    df.to_csv(path + country_name + '_' + str(player) + ('_a.csv' if part == 1 else '_b.csv'), encoding='utf-8')

def openBrowser(choice = 'mozilla') -> object:\
    ''' requires chrome or mozilla webdriver
    '''
    assert os.path.exists('./drivers/'), 'Move webdriver to ./drivers/.'
    if choice == 'mozilla':
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
        browser = webdriver.Firefox(executable_path='./drivers/geckodriver', firefox_profile=firefox_profile)
    elif choice == 'chrome':
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--icognito")
        browser = webdriver.Chrome(executable_path='./drivers/chromedriver.exe', options=chrome_options)
    time.sleep(randint(2,10))
    return browser

def quitBrowser(browser):
    browser.quit()
    time.sleep(randint(2,10))

def get_file_to_import_input() -> str:
    ''' return datapath /Input/{placeholder}.txt
    '''
    file_to_read = ''
    while not (file_to_read.endswith('.txt') and os.path.isfile(os.path.join(os.getcwd(), './Input/' + file_to_read))):
        if file_to_read != '':
            print('Something went terribly wrong.\nMake sure there is a file with this name and this extension in \"' + os.getcwd() + '\\Input\"')
        file_to_read = input('Queries text file:\n(i.e. test.txt)\n').strip()
    return os.path.join(os.getcwd(), './Input/' + file_to_read)

# Variable Country
def get_country_name_input(
) -> str:
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

def get_player_input(
) -> int:
    ''' player variable
    '''
    player = -1
    while player != 1 and player != 2:
        if player != -1:
            print('Wrong Input.\nJust press \"1\" or \"2\" for god\'s sake!')
        try:
            player = int(input('Player 1 or 2?\n'))
        except ValueError:
            print('Not an Integer.')
    return player

def get_part_input(
) -> int:
    ''' part variable (batches of 10 topics)
    '''
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
    integrated_webdriver = 'mozilla'
    file_to_read = get_file_to_import_input()
    country = get_country_name_input()
    player = get_player_input()
    part = get_part_input() 
    # run Script for the first or the second half of the queries located in the .txt file
    topics_batch_const = 10
    topics_n_queries = read_lines(file_to_read)[
        ( ( part - 1 ) * topics_batch_const ) * 5
        : ( part * topics_batch_const ) * 5
    ]
    # begin search
    browser = openBrowser(integrated_webdriver)
    results = {}
    for i, line in enumerate(topics_n_queries):
        if i % 5 == 0:
            topic = line
            results[topic] = {}
        else:
            collected_results = google_search(
                line,
                browser,
                integrated_webdriver
            )
            if i % 5 == 1 or i % 5 == 3:
                results[topic][f'subquery_{player}'] = collected_results
            elif i % 5 == 2 or i % 4 == 3:
                results[topic][f'mainquery_{player}'] = collected_results
                browser.quit()
                time.sleep(60 * 30)
                browser = openBrowser(integrated_webdriver)
    print_results(results)
    export_results(results, country, player, part)