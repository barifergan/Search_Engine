import collections
import copy
import itertools
import json
import operator
import pickle
import time
from configuration import ConfigClass
import utils
import statistics
from tqdm import tqdm


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
    docs_set = set()
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
                for curr_doc in val:
                    docs_set.add(curr_doc[0])
                rows.remove(rows[0])

                if not rows:
                    break
            lines_counter += 1
    val_to_return = dict_to_return[key]
    return val_to_return, docs_set


class GlobalMethod(object):
    associations_matrix = {}
    relevant_terms = []

    @classmethod
    def build_matrix(cls):
        #
        # with open('C:\\Users\\barif\\PycharmProjects\\Search_Engine\\WithoutStem\\a' + '.json') as f:
        #     line = next(itertools.islice(f, 20, 20 + 1), None)
        #     # line = f.readline()
        #     print(line)

        start_time = time.time()
        print('load inverted index')
        with open('inverted_idx.pkl', 'rb') as inverted_idx:
            inverted_idx = pickle.load(inverted_idx)
        print('inverted index loaded')

        all_df = []
        for term in inverted_idx.keys():
            all_df.append(inverted_idx[term][0])
        df = sorted(all_df, reverse=True)
        print(df[:4000])

        sorted_inverted_idx = sorted(inverted_idx, key=inverted_idx.get, reverse=True)

        cls.relevant_terms = sorted_inverted_idx[:4000]

        # for term in inverted_idx.keys():
        #     if lower_threshold < inverted_idx[term][0] < upper_threshold:
        #         cls.relevant_terms.append(term)

        relevant_words = sorted(cls.relevant_terms)
        print(cls.relevant_terms)
        print(relevant_words)
        # associations_matrix = np.zeros(shape=(len(relevant_words), len(relevant_words)), dtype=int)
        cls.associations_matrix = {i: [0] * len(relevant_words) for i in relevant_words}
        print('association matrix build with zeros')
        words_dict = {}
        docs_sets_dict = {}

        for word in tqdm(relevant_words):
            words_dict[word] = []
            lines_in_posting = inverted_idx[word][1]  # all the lines that this word appear in posting file

            if not lines_in_posting:
                print(word, inverted_idx[word])

            docs_list, docs_set = extract_from_posting_file(word, lines_in_posting,
                                                            'C:\\Users\\barif\\PycharmProjects\\Search_Engine\\WithoutStem')  # ConfigClass.get__outputPath())
            words_dict[word] = docs_list
            docs_sets_dict[word] = docs_set

            for key_word in tqdm(words_dict.keys()):
                if key_word == word or key_word == word.upper() or key_word == word.lower():
                    cii = 0
                    for val in words_dict[key_word]:
                        cii += val[1] ** 2

                    idx = relevant_words.index(word)
                    cls.associations_matrix[word][idx] = cii

                else:
                    cij = 0
                    common_docs = docs_sets_dict[word].intersection(docs_sets_dict[key_word])
                    for doc in common_docs:
                        temp_cij = 0
                        for val in words_dict[word]:
                            if val[0] == doc:
                                temp_cij = val[1]
                        for val2 in words_dict[key_word]:
                            if val2[0] == doc:
                                temp_cij = temp_cij * val2[1]
                        cij += temp_cij

                    idx_i = relevant_words.index(word)
                    idx_j = relevant_words.index(key_word)
                    cls.associations_matrix[key_word][idx_i] = cij
                    cls.associations_matrix[word][idx_j] = cij


                    # for val1 in words_dict[word]:
                    #     for val2 in words_dict[key_word]:
                    #         if val1[0] == val2[0]:
                    #             cij += val1[1] * val2[1]
                    #     idx_i = relevant_words.index(word)
                    #     idx_j = relevant_words.index(key_word)
                    #     cls.associations_matrix[key_word][idx_i] = cij
                    #     cls.associations_matrix[word][idx_j] = cij

        print('association matrix build without normalize')

        for row in tqdm(cls.associations_matrix.keys()):
            for idx_col in range(len(cls.associations_matrix[row])):
                idx_row = relevant_words.index(row)
                col = relevant_words[idx_col]

                cii = cls.associations_matrix[row][idx_row]
                cjj = cls.associations_matrix[col][idx_col]
                cij = cls.associations_matrix[row][idx_col]
                if row != col:
                    demon = (cii + cjj - cij)
                    sij = cij / demon
                    cls.associations_matrix[row][idx_col] = sij

        print('association matrix build with normalize')

        #
        utils.save_obj(cls.associations_matrix, "associations_matrix")

        end_time = time.time()
        print("--- %s seconds ---" % (end_time - start_time))

        return cls.associations_matrix

    @classmethod
    def expand_query(cls, query):

        with open('associations_matrix.pkl', 'rb') as matrix_from_file:
            association_matrix = pickle.load(matrix_from_file)
        expansion = []
        relevant_terms = sorted(association_matrix, key=association_matrix.get, reverse=True)
        for term in query:
            if term not in association_matrix.keys():
                continue
            lst = association_matrix[term]
            idx_max_val = lst.index(max(lst))
            expansion.append(relevant_terms[idx_max_val])

        return query.extend(expansion)


# GlobalMethod.build_matrix()
