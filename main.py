# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time


def get_data(search_google_url, list_of_queries_to_search, list_of_words_to_find_on_webpage):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    click_accept_cookies_button(driver, search_google_url)

    for query in list_of_queries_to_search:
        number_of_results_sets_to_check = 1
        links_from_query = collect_links_from_search_query(driver, query, search_google_url, number_of_results_sets_to_check)

        # save backup of collected links
        links_dict = {"links": links_from_query}
        df = pd.DataFrame(links_dict)
        saving_directory = "results/"
        version = 3
        filename = "links__query_{}__sets_{}__version_{}".format(query, number_of_results_sets_to_check, version)
        df.to_excel(saving_directory + filename + str(version) + ".xlsx")
        df.to_csv(saving_directory + filename + str(version) + ".csv")

        convert_list_of_links_to_html(driver, links_from_query, number_of_results_sets_to_check, query)


def convert_list_of_links_to_html(driver, links_from_query, number_of_results_sets_to_check, query):
    # convert each link into html
    htmls_from_query = []
    for link in links_from_query:
        driver.get(link)
        html_code = driver.page_source
        time.sleep(2)
        htmls_from_query.append(html_code)
    new_links = {'link': links_from_query, 'html': htmls_from_query}
    df = pd.DataFrame(new_links)
    saving_directory = "results/"
    version = 3
    filename = "results__query_{}__sets_{}__version_{}".format(query, number_of_results_sets_to_check, version)
    df.to_excel(saving_directory + filename + str(version) + ".xlsx")
    df.to_csv(saving_directory + filename + str(version) + ".csv")


def collect_links_from_search_query(driver, query, search_google_url, number_of_results_sets_to_check):
    """

    :param driver:
    :param query:
    :param search_google_url:
    :param number_of_results_sets_to_check: number of "o"s to click at the bottom of the page in order to go
            to another set of results; adjust this variable to your needs
    :return:
    """
    links_from_query = []
    search_query = search_google_url + query
    driver.get(search_query)
    for google_result_set in range(number_of_results_sets_to_check):
        time.sleep(2)  # wait until the results are loaded
        results_list = driver.find_elements(By.TAG_NAME, 'a')
        results_list = list(filter(None, results_list))  # remove all 'None's from list
        links = []
        for result in results_list:
            links.append(result.get_attribute('href'))  # get the link out of the element

        links = list(filter(lambda item: item is not None, links))  # remove all 'None's from list
        links = list(dict.fromkeys(links))  # remove duplicates from list

        links = [x for x in links if "google" not in x]  # remove all links with 'google' from list

        print("Result set no.: {}".format(google_result_set))
        for link in links:
            print(link)

        links_from_query += links  # save the collected links to the main list

        # go to the next page set:
        if google_result_set < number_of_results_sets_to_check - 1:  # don't click it at the last checked result set
            next_page_set_xpath = "/html/body/div[7]/div/div[11]/div/div[4]/div/div[2]/table/tbody/tr/td[{}]/a".format(
                google_result_set + 3)
            next_page_set_button = driver.find_element(By.XPATH, next_page_set_xpath)
            next_page_set_button.click()

    return links_from_query


def click_accept_cookies_button(driver, search_google_url):
    search_query = search_google_url
    driver.get(search_query)
    time.sleep(1)  # wait until the page is loaded

    # click the "accept cookies" button
    accept_cookies_button_xpath = '/html/body/div[2]/div[2]/div[3]/span/div/div/div/div[3]/div[1]/button[2]/div'
    accept_cookies_button = driver.find_element(By.XPATH, accept_cookies_button_xpath)
    accept_cookies_button.click()


if __name__ == '__main__':
    list_of_words_to_find_on_webpage = ["Politechnika Gdańska"]
    list_of_queries_to_search = ["Politechnika Gdańska Wydział Zarządzania i Ekonomii"]
    search_google_url = "https://www.google.pl/search?q="
    get_data(search_google_url, list_of_queries_to_search, list_of_words_to_find_on_webpage)
