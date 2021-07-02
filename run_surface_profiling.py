"""
To do list
1. Read csv file/files from raw folder
2. Clean the file/files, replace -99.9999 with NaN
3. Merge into one df and plot line graph and save pdf file
"""
import pandas as pd
import glob
import os
import numpy as np
from datetime import datetime


def get_all_csv_file(path):
    """[Read csv file/files from raw folder]
    Args:
        path (string): [the folder path] 
    Returns:
        file_list (list): [all csv filenames] 
    """
    file_list = glob.glob(path + "/*.csv")
    return file_list


def clean_and_save(filename):
    """[Clean the file/files and save into csv file]

    Args:
        filename (string): [the filename of raw file]
    """
    print('cleaning filename: '+filename+"...")

    basename = os.path.basename(filename).split('.')[0]
    # read csv file
    data = pd.read_csv(filename)
    clean_data = data.iloc[:, 2]

    # replace -99.9999 with NaN
    clean_data = clean_data.replace(-99.9999, np.nan)

    # write to csv file
    save_filename = "clean/"+basename + "_clean.csv"
    clean_data.to_csv(save_filename,
                      index=False, header=[basename])

    print('Successfully cleaned and saved: '+save_filename)


def merge_and_plot(clean_path='clean'):
    """[Merge into one df]

    Args:
        clean_path (string, optional): [path of the clean data folder]. Defaults to 'clean'.
    Returns:
        merge_df (dataframe): the merged dataframe
    """
    clean_file_list = get_all_csv_file(clean_path)
    merge_df = pd.DataFrame()
    for each in clean_file_list:
        df = pd.read_csv(each)
        merge_df = pd.concat([merge_df, df], axis=1)
    return merge_df


def plot_and_save(merge_df):
    """[summary]

    Args:
        merge_df ([dataframe]): [the merged dataframe]
    """
    time_now = datetime.now()
    time_now_str = time_now.strftime('%Y%m%d_%H_%M_%S')
    save_filename = 'results-plots/'+time_now_str+'_surfaceprofiler.pdf'

    fig = merge_df.plot(kind='line',  figsize=(
        20, 16), fontsize=26).get_figure()
    fig.savefig(save_filename)
    print('Successfully saved to: '+save_filename)


def files_clean_up(raw='raw', clean='clean'):
    """[clean up used files]

    Args:
        raw (str, optional): [folder path for raw file]. Defaults to 'raw'.
        clean (str, optional): [folder path for clean file]. Defaults to 'clean'.
    """
    raw_file_list = get_all_csv_file(raw)
    clean_file_list = get_all_csv_file(clean)
    for each in raw_file_list:
        os.remove(each)
        print('Successfully remove to: '+each)
    for each in clean_file_list:
        os.remove(each)
        print('Successfully remove to: '+each)


def main():
    """[Run the profilling process]
    """
    print("Started the surface profileing process...")
    file_list = get_all_csv_file('raw')
    if len(file_list) == 0:
        print("Please insert raw files in the raw folder.")
        return
    for each in file_list:
        clean_and_save(each)
    merge_df = merge_and_plot()
    plot_and_save(merge_df)
    files_clean_up()
    print("Successfully done the surface profileing.")


if __name__ == '__main__':
    main()
