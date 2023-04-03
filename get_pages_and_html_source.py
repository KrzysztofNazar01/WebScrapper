"""
Authors: Krzysztof Nazar and ...
Version: 1.1
Last release: 28/03/2023
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time
from tqdm import tqdm
from selenium.common.exceptions import NoSuchElementException


def remove_duplicates_from_list(given_list):
    """
    From the given list remove all duplicates of its elements.

    :param given_list: list of elements
    :return: filtered list without duplicates of its elements
    """
    return list(dict.fromkeys(given_list))


def remove_nones_from_list(given_list):
    """
    From the given list remove all elements that are "None"s.

    :param given_list: list of elements
    :return: filtered list without elements that are "None"s
    """
    return list(filter(None, given_list))


def remove_elements_from_list_with_substring(given_list, substring):
    """
    From the given list remove all elements that contain the substring.

    :param given_list: list of elements
    :param substring: string to look for in the elements of the given list
    :return: filtered list without elements that contain the substring
    """
    return [element for element in given_list if substring not in element]


def save_the_dictionary(filename_beginning, dictionary, query, number_of_results_sets_to_check, version):
    """
    Save a dictionary as a file to read. Data is exported with Pandas using export methods - DataFrame is saved as a *.csv file.

    :param filename_beginning: the type of results - only links or links with htmls
    :param dictionary: the collected data
    :param query: the query searched in Google search
    :param number_of_results_sets_to_check: number of "o"s to click at the bottom of the page in order to go
                                            to another set of results;
    :param version: the version of files where the results are saved
    """
    print("Saving the DataFrame with {}. It may take a while...".format(filename_beginning))
    df = pd.DataFrame(dictionary)
    saving_directory = "results/"
    filename = "{}__query_{}__sets_{}__version_{}".format(filename_beginning, query.replace(" ", "_"),
                                                          number_of_results_sets_to_check, version)
    # df.to_excel(saving_directory + filename + ".xlsx")  # works longer than "to_csv" method
    df.to_csv(saving_directory + filename + ".csv")
    print("Finished saving the DataFrame with {}.".format(filename_beginning))


def get_html_source_code_from_pages(driver, links_from_query):
    """
    Get the html source code of each page from the list of links.

    :param driver: webdriver from Selenium
    :param links_from_query: list of links collected from query results from the set number of results set
    :return: list of html code source
    """
    print("Getting the HTML source code from pages. This may take a while...")
    htmls_from_query = []
    for link in tqdm(links_from_query):
        driver.get(link)
        time.sleep(1)  # wait for the page to load
        html_code = driver.page_source
        time.sleep(3)  # wait for the page to load
        htmls_from_query.append(html_code)

    print("Finished getting the HTML source code from pages.")

    return htmls_from_query


def collect_links_from_search_query(driver, query, search_google_url, number_of_results_sets_to_check):
    """
    Collect a list of links available on the page with search results.
    The filtering of links can be adjusted - for example to remove links that contain a given substring.

    :param driver: webdriver from Selenium
    :param query: value searched in Google search
    :param search_google_url: template for Google search url
    :param number_of_results_sets_to_check: number of "o"s to click at the bottom of the page in order to go
                                            to another set of results; adjust this variable to your needs
    :return: list of links collected from query results from the set number of results set
    """
    links_from_query = []
    search_query = search_google_url + query.replace(" ", "+")
    driver.get(search_query)  # open page with the search query

    for google_result_set in tqdm(range(number_of_results_sets_to_check)):
        time.sleep(2)  # wait until the results are loaded
        results_list = driver.find_elements(By.TAG_NAME, 'a')
        results_list = remove_nones_from_list(results_list)
        links = []
        for result in results_list:
            links.append(result.get_attribute('href'))  # get the link out of the element

        links = remove_nones_from_list(links)
        links = remove_duplicates_from_list(links)
        links = remove_elements_from_list_with_substring(links, "google")
        links = remove_elements_from_list_with_substring(links, "youtube")

        print("Result set no.: {} - found {} links for search query: {}".format(google_result_set + 1, len(links),
                                                                                search_query))

        links_from_query += links  # save the collected links to the main list

        open_next_pages_set(driver, google_result_set, number_of_results_sets_to_check)

    return links_from_query


def open_next_pages_set(driver, google_result_set, number_of_results_sets_to_check):
    """
    Go to the page with next results set. IT is done by clicking the "o" at the bottom of the page.

    :param driver: webdriver from Selenium
    :param google_result_set: current number of already visited results sets
    :param number_of_results_sets_to_check: number of "o"s to click at the bottom of the page in order to go
                                            to another set of results; adjust this variable to your needs
    """
    if google_result_set < number_of_results_sets_to_check - 1:  # don't click it at the last checked result set
        div_number = google_result_set + 3
        try:
            next_page_set_xpath = "/html/body/div[7]/div/div[11]/div/div[4]/div/div[2]/table/tbody/tr/td[{}]/a".format(
                div_number)
            next_page_set_button = driver.find_element(By.XPATH, next_page_set_xpath)
            next_page_set_button.click()
        except NoSuchElementException:  # spelling error making this code not work as expected
            pass


def click_accept_cookies_button(driver, search_google_url):
    """
    This method is responsible for clicking the "accept cookies" button at the first query that is searched after
    initialization of the driver.

    :param driver: webdriver from Selenium
    :param search_google_url: template for Google search url
    """
    # search example webpage - just to trigger opening the "accpet cookies" button
    search_query = search_google_url
    driver.get(search_query)
    time.sleep(1)  # wait until the page is loaded

    # click the "accept cookies" button
    accept_cookies_button_xpath = '/html/body/div[2]/div[2]/div[3]/span/div/div/div/div[3]/div[1]/button[2]/div'
    accept_cookies_button = driver.find_element(By.XPATH, accept_cookies_button_xpath)
    if accept_cookies_button is None:
        time.sleep(5)
        accept_cookies_button = driver.find_element(By.XPATH, accept_cookies_button_xpath)
    accept_cookies_button.click()


def run_scrapper(search_google_url, list_of_queries_to_search, number_of_results_sets_to_check, version):
    """
    Search for query in Google search. Collect all the results and save their links into a list. Next, open each page
    and save its HTML source code. Finally, save the results of scrapping into a DataFrame and export it into a file
    with results.

    :param search_google_url: template for Google search url
    :param list_of_queries_to_search: list of
    queries that will be searched for with the Google search tool
    :param number_of_results_sets_to_check: number of "o"s to click at the bottom of the page in order to
                                            go to another set of results; adjust this variable to your needs
    :param version: the version of files where the results are saved
    """
    driver = webdriver.Chrome(ChromeDriverManager().install())
    click_accept_cookies_button(driver, search_google_url)

    for query in tqdm(list_of_queries_to_search):
        print("\nSTARTING SEARCH WITH QUERY: {}".format(query))
        links_from_query = collect_links_from_search_query(driver, query, search_google_url,
                                                           number_of_results_sets_to_check)

        links_from_query = remove_duplicates_from_list(links_from_query)

        # save backup of collected links
        collected_links = {"links": links_from_query}
        save_the_dictionary("links", collected_links, query, number_of_results_sets_to_check, version)

        # # get html of each page
        # htmls_from_query = get_html_source_code_from_pages(driver, links_from_query)
        #
        # # save the links with htmls into a Pandas DataFrame
        # collected_links_with_html_code = {'link': links_from_query, 'html': htmls_from_query}
        #
        # save_the_dictionary("results", collected_links_with_html_code, query, number_of_results_sets_to_check, version)
        # save_the_dictionary("results", collected_links, query, number_of_results_sets_to_check, version)

    driver.close()


if __name__ == '__main__':
    search_google_url = "https://www.google.pl/search?q="

    # adjust these parameters:
    list_of_words_to_find_on_webpage = ["Politechnika Gdańska",
                                        "Zarządzania i Ekonomii"]
    list_of_queries_to_search = ["Politechnika Gdańska Wydział Zarządzania i Ekonomii social media",
                                 "Politechnika Gdańska Wydział Zarządzania i Ekonomii",
                                 "Politechnika Gdańska W ZiE",
                                 "Politechnika Gdańska Wydział Zarządzania i Ekonomii facebook instagram twitter",
                                 "Politechnika Gdańska Wydział Zarządzania i Ekonomii gazety artykuł",
                                 "Politechnika Gdańska Wydział Zarządzania i Ekonomii praca naukowa",
                                 "Google Scholar Politechnika Gdańska Wydział Zarządzania i Ekonomii"
                                 ]
    number_of_results_sets_to_check = 10  # number of "o"s to click at the bottom of the page in order to go to
    # another set of results
    version = 6  # the version of files where the results are saved

    # get the links and html source code
    run_scrapper(search_google_url, list_of_queries_to_search, number_of_results_sets_to_check, version)
