import pandas as pd

from get_pages_and_html_source import *
from os import listdir
from os.path import isfile, join
import re


def get_query_from_file_name(filename):
    result = re.search('query_(.*)__', filename)
    query = result.group(1)
    return query


if __name__ == '__main__':
    version = 7

    driver = webdriver.Chrome(ChromeDriverManager().install())
    search_google_url = "https://www.google.pl/search?q="
    click_accept_cookies_button(driver, search_google_url)

    df_links = pd.read_csv("links_clear.csv")
    list_links = df_links["links"].values.tolist()

    index_start = 301
    index_end = len(list_links)
    htmls_from_query = get_html_source_code_from_pages(driver, list_links[index_start:index_end])

    collected_links_with_html_code = {'link': list_links[index_start:index_end], 'html': htmls_from_query}
    query = "links_and_html_from_{}_to_{}_".format(index_start, index_end)
    save_the_dictionary("", collected_links_with_html_code, query, 10, version, "clear_results/")

    # finish webscrapping bu closing the driver
    driver.close()
