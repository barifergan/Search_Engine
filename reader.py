import os
import pandas as pd


class ReadFile:
    def __init__(self, corpus_path):
        self.corpus_path = corpus_path

    def read_file(self, file_name):
        """
        This function is reading a parquet file contains several tweets
        The file location is given as a string as an input to this function.
        :param file_name: string - indicates the path to the file we wish to read.
        :return: a dataframe contains tweets.
        """
        full_path = os.path.join(self.corpus_path, file_name)
        df = pd.read_parquet(full_path, engine="pyarrow")
        return df.values.tolist()

    def open_folder(self, corpus_path):
        root_dir = corpus_path
        tweets_list = []

        # iterate trough all inner folders and pulls out all parquet files, send to read_file function
        for subdir, dirs, files in os.walk(root_dir):
            for file in files:
                file_type = file[-8:]
                if file_type == '.parquet':
                    self.corpus_path = subdir
                    tweets_list += self.read_file(file)
                    # print(tweets_list)
        # print(tweets_list[3])

        return tweets_list


# corpus_path1 = "C:\\Users\\ronen\\Downloads\\Data"
# read = ReadFile(corpus_path1)
# path1 = read.open_folder(corpus_path1)
