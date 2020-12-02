import json
import pickle
import time

import utils

class GlobalMethod:
    def __init__(self):
        self.associations_matrix = {}
        self.relevant_terms = []

    def build_matrix(self):

    # --------------------build matrix-----------------------------------

        start_time = time.time()
        with open('inverted_idx.pkl', 'rb') as inverted_idx:
            inverted_idx = pickle.load(inverted_idx)
        start_time = time.time()

        df = 0
        for term in inverted_idx.keys():
            df += inverted_idx[term][0]

        avg = df / 10000000

        if 500 < inverted_idx[term][0] < 10000:
            self.relevant_terms.append(term)

        relevant_words = sorted(self.relevant_terms)

        # associations_matrix = np.zeros(shape=(len(relevant_words), len(relevant_words)), dtype=int)
        self.associations_matrix = {i: [0]*len(relevant_words) for i in relevant_words}
        words_dict = {}

        for word in relevant_words:
            words_dict[word] = []
            lines_in_file = inverted_idx[word][1]

            posting_doc = self.extract_from_posting_file(word, lines_in_file, 'C:\\Users\\barif\\PycharmProjects\\Search_Engine\\json_files')
            words_dict[word] = posting_doc[word]

            for key_word in words_dict:
                if key_word == word:
                    cii = 0
                    for val in words_dict[key_word]:
                        cii += val[1] ** 2

                    idx = relevant_words.index(key_word)
                    self.associations_matrix[idx, idx] = cii

                else:
                    cij = 0
                    for val in words_dict[key_word]:
                        for tup in words_dict[word]:
                            if tup[0] == val[0]:
                                cij += tup[1] * val[1]
                        idx_i = relevant_words.index(key_word)
                        idx_j = relevant_words.index(word)
                        self.associations_matrix[idx_i, idx_j] = cij
                        self.associations_matrix[idx_j, idx_i] = cij

        utils.save_obj(self.associations_matrix, "associations_matrix")

        end_time = time.time()
        print("--- %s seconds ---" % (end_time - start_time))


    def extract_from_posting_file(self, term, rows_num, output_path):
        if term[0].isalpha():
            file_name = term[0]
        elif term[0] == '#':
            file_name = 'hashtag'
        elif term[0] == '@':
            file_name = 'tagging'
        elif term[0].isdigit():
            file_name = 'number'
        else:
            file_name = 'other'

        with open(output_path + '\\' + file_name + '.json') as f:
            lines_counter = 1
            dict_to_return = {}
            for line in f:
                if lines_counter == rows_num[0]:
                    j_content = json.loads(line)
                    key = [*j_content][0]
                    val = j_content[key]
                    if key not in dict_to_return:
                        dict_to_return[key] = []

                    dict_to_return[key].append(val)
                    rows_num.remove(rows_num[0])

                    if not rows_num:
                        break
                lines_counter += 1
        return dict_to_return



    def expand_query(self, query):
        for term in query:
            lst = self.associations_matrix[term]
            idx_max_val = lst.index(max(lst))
            expantion = self.relevant_terms[idx_max_val]





build_matrix()