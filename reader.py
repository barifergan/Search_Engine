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
        root_dir = self.corpus_path
        exist = 0

        for curr_dir in os.walk(root_dir):
            for file in curr_dir[2]:
                if file == file_name:
                    path_file = curr_dir[0]
                    exist = 1
                    break
            else:
                continue
            break

        if exist == 1:
            full_path = os.path.join(path_file, file_name)
            df = pd.read_parquet(full_path, engine="pyarrow")
            # print(df.values.tolist())
            return df.values.tolist()
        return
