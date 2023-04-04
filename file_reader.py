from os import listdir
from os.path import isfile, join
import re
import pandas as pd


def replacing_in_link(string):
    return string.replace('\n', ' ')


def merge_csv_files_from_directory():
    version = 7

    # read the csv files with links_google
    links_path = 'links_duck/clear/'
    files_with_links = [f for f in listdir(links_path) if isfile(join(links_path, f))]

    df_links_all = pd.DataFrame()

    for file in files_with_links:
        df_links_from_file = pd.read_csv(links_path + file)
        frames = [df_links_all, df_links_from_file]
        df_links_all = pd.concat(frames, ignore_index=True)

    del df_links_from_file
    del file
    del files_with_links
    del frames

    print("before: {}".format(df_links_all.info()))
    df_links_all = df_links_all.drop(df_links_all.columns[0], axis=1)
    df_links_all = df_links_all.sort_values('link', ascending=True)
    df_links_all = df_links_all.drop_duplicates()
    df_links_all = df_links_all.reset_index(drop=True)
    df_links_all.apply(lambda row: replacing_in_link(row['html']), axis=1)
    print("\nafter: {}".format(df_links_all.info()))
    df_links_all.to_csv(links_path+"links_and_html_all_duck_ready_to_send.csv", index_label=False)
    print(df_links_all.head(10))

def get_difference_Between_two_df():
    links_google = pd.read_csv("links_clear.csv")
    links_duck = pd.read_csv("links_clear_duck_short.csv")

    # print(links_google.info())
    # print(links_google.head(10))
    # print(links_duck.info())
    # print(links_duck.head(10))
    common = links_google.merge(links_duck, on=['links'])
    print(common)
    difference_btw_google_and_duck_links = links_google[(~links_google.links.isin(common.links))]
    # print(difference_btw_google_and_duck_links.info())
    # print(difference_btw_google_and_duck_links.head(10))
    difference_btw_google_and_duck_links = difference_btw_google_and_duck_links.reset_index(drop=True)
    difference_btw_google_and_duck_links.to_csv("difference_btw_google_and_duck_links.csv", index_label=False)


if __name__ == '__main__':
    merge_csv_files_from_directory()




