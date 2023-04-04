from os import listdir
from os.path import isfile, join
import re
import pandas as pd


def replacing_in_link(string):
    return string.replace('\n', ' ')


if __name__ == '__main__':
    version = 7

    # read the csv files with links
    links_path = 'clear_results/'
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
    # df_links_all = df_links_all.sort_values('link', ascending=True)
    df_links_all = df_links_all.drop_duplicates()
    df_links_all = df_links_all.reset_index(drop=True)
    df_links_all.apply(lambda row: replacing_in_link(row['html']), axis=1)
    print("\nafter: {}".format(df_links_all.info()))
    df_links_all.to_csv(links_path+"links_clear_all_2.csv", index_label=False)
    print(df_links_all.head(10))
