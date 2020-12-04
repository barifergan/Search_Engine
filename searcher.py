import copy
import json
import math
import numpy as np
from configuration import ConfigClass
from parser_module import Parse
from ranker import Ranker


class Searcher:

    def __init__(self, inverted_index):
        """
        :param inverted_index: dictionary of inverted index
        """
        self.parser = Parse()
        self.ranker = Ranker()
        self.inverted_index = inverted_index
        self.output_path = ConfigClass.get__outputPath()

    def relevant_docs_from_posting(self, query, num_of_docs_in_corpus=10000000):
        """
        This function loads the posting list and count the amount of relevant documents per term.
        :param query: query
        :return: dictionary of relevant documents.
        """
        relevant_docs = {}  # key- tweet id , value
        terms = {}  # key- term , value- (tweet id, fi)
        docs_content = {}

        query_dict = {}  # to check how many times word appear in the query
        for term in query:
            try:
                if term in self.inverted_index.keys():
                    temp_term = term
                elif term.lower() in self.inverted_index.keys():
                    temp_term = term.lower()
                elif term.upper() in self.inverted_index.keys():
                    temp_term = term.upper()
                else:
                    continue
                dict_of_doc_ids = self.extract_from_posting_file(temp_term, self.inverted_index[temp_term][1])
                key = [*dict_of_doc_ids][0]
                terms[temp_term] = dict_of_doc_ids[key][0]
                for doc in terms[temp_term]:
                    if doc[0] not in docs_content.keys():
                        docs_content[doc[0]] = [[temp_term, doc[1]]]
                        relevant_docs[doc[0]] = []
                    else:
                        exists = False
                        for pair in docs_content[doc[0]]:
                            if pair[0] == term:
                                pair[1] += 1
                                exists = True
                        if not exists:
                            docs_content[doc[0]].append([term, doc[1]])

                if temp_term not in query_dict.keys():
                    query_dict[temp_term] = 1
                else:
                    query_dict[temp_term] += 1

            except:
                print('term {} not found in posting'.format(term))

        idf = []
        query_vec = []

        for term in query_dict:
            query_vec.append(query_dict[term])

        print(query_dict)
        mx = max(query_vec)
        normalized_query = np.divide(query_vec, max(query_vec))
        for word in query_dict.keys():
            try:
                if word in self.inverted_index.keys():
                    dfi = self.inverted_index[word][0]
                    idf.append(math.log(num_of_docs_in_corpus / dfi, 2))

                    for doc in docs_content.keys():
                        exist = False
                        for pair in docs_content[doc]:
                            if word == pair[0]:
                                relevant_docs[doc].append(pair[1])
                                exist = True

                        if not exist:
                            relevant_docs[doc].append(0)

            except:
                print('term {} not found in inverted index'.format(word))

        # divide each element in the vector by thr max(f) of the doc. the information in docs_dict

        with open('docs_dict.json', 'r') as f:
            for line in f:
                j_content = json.loads(line)
                key = [*j_content][0]
                if key in relevant_docs.keys():
                    max_tf = j_content[key][0]
                    relevant_docs[key] = np.divide(relevant_docs[key], max_tf)
                    relevant_docs[key] = np.multiply(relevant_docs[key], idf)

        # calculate idf of each element in the vector (idf is log2(number of docs in the corpus \ df(from inverted index)

        # multiply tf*idf of each element

        # return relevant docs

        return relevant_docs, normalized_query

    def extract_from_posting_file(self, term, rows_num):
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

        with open(self.output_path + '\\' + file_name + '.json') as f:
            lines_counter = 1
            dict_to_return = {}  # key: term, value:list of tweets id
            for line in f:
                if lines_counter == rows[0]:
                    j_content = json.loads(line)
                    key = [*j_content][0]
                    val = j_content[key]
                    if key not in dict_to_return:
                        dict_to_return[key] = []

                    dict_to_return[key].append(val)
                    rows.remove(rows[0])

                    if not rows:
                        break
                lines_counter += 1
        return dict_to_return
