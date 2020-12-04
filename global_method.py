import copy
import json
import operator
import pickle
import time
from configuration import ConfigClass
import utils
import statistics


def extract_from_posting_file(term, rows_num, output_path):
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

    rows = copy.deepcopy(rows_num)
    with open(output_path + '\\' + file_name + '.json') as f:
        lines_counter = 1
        dict_to_return = {}
        for line in f:
            if lines_counter == rows[0]:
                j_content = json.loads(line)
                key = [*j_content][0]
                val = j_content[key]
                if key not in dict_to_return:
                    dict_to_return[key] = []

                dict_to_return[key].extend(val)
                rows.remove(rows[0])

                if not rows:
                    break
            lines_counter += 1
    val_to_return = dict_to_return[key]
    return val_to_return


class GlobalMethod(object):
    associations_matrix = {}
    relevant_terms = []

    @classmethod
    def build_matrix(cls):

        start_time = time.time()
        with open('inverted_idx.pkl', 'rb') as inverted_idx:
            inverted_idx = pickle.load(inverted_idx)

        all_df = []
        for term in inverted_idx.keys():
            all_df.append(inverted_idx[term][0])

        # sorted_inverted_idx = sorted(inverted_idx.items(), key=lambda item: item[1][0], reverse=True)
        sorted_inverted_idx = sorted(inverted_idx, key=inverted_idx.get, reverse=True)
        cls.relevant_terms = sorted_inverted_idx[:100]

        # for term in inverted_idx.keys():
        #     if lower_threshold < inverted_idx[term][0] < upper_threshold:
        #         cls.relevant_terms.append(term)

        relevant_words = sorted(cls.relevant_terms)

        # associations_matrix = np.zeros(shape=(len(relevant_words), len(relevant_words)), dtype=int)
        cls.associations_matrix = {i: [0] * len(relevant_words) for i in relevant_words}
        words_dict = {}

        for word in relevant_words:
            words_dict[word] = []
            lines_in_posting = inverted_idx[word][1] #all the lines that this word appear in posting file

            if not lines_in_posting:
                print(word , inverted_idx[word])

            docs_list = extract_from_posting_file(word, lines_in_posting, ConfigClass.get__outputPath()) # 'C:\\Users\\barif\\PycharmProjects\\Search_Engine\\WithStem'
            words_dict[word] = docs_list

            for key_word in words_dict.keys():
                if key_word == word or key_word == word.upper() or key_word == word.lower():
                    cii = 0
                    for val in words_dict[key_word]:
                        cii += val[1] ** 2

                    idx = relevant_words.index(word)
                    cls.associations_matrix[word][idx] = cii

                else:
                    cij = 0
                    for val1 in words_dict[word]:
                        for val2 in words_dict[key_word]:
                            if val1[0] == val2[0]:
                                cij += val1[1] * val2[1]
                        idx_i = relevant_words.index(word)
                        idx_j = relevant_words.index(key_word)
                        cls.associations_matrix[key_word][idx_i] = cij
                        cls.associations_matrix[word][idx_j] = cij

        for row in cls.associations_matrix.keys():
            for idx_col in range(len(cls.associations_matrix[row])):
                idx_row = relevant_words.index(row)
                col = relevant_words[idx_col]

                cii = cls.associations_matrix[row][idx_row]
                cjj = cls.associations_matrix[col][idx_col]
                cij = cls.associations_matrix[row][idx_col]
                if row != col:
                    demon = (cii + cjj - cij)
                    if demon == 0:
                        print('problem!!!!!!!!!!', cii, cjj, cij)
                    else:

                        sij = cij / demon
                        cls.associations_matrix[row][idx_col] = sij

                #
        utils.save_obj(cls.associations_matrix, "associations_matrix")

        end_time = time.time()
        print("--- %s seconds ---" % (end_time - start_time))

        return cls.associations_matrix

    @staticmethod
    def expand_query(cls, query):
        expansion = []
        for term in query:
            lst = cls.associations_matrix[term]
            idx_max_val = lst.index(max(lst))
            expansion.append(cls.relevant_terms[idx_max_val])

        return query.extend(expansion)


# matrix = GlobalMethod.build_matrix()
# for key, value in matrix.items():
#     print(key, ' : ', value)
