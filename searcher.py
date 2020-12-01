import json
import numpy as np
from parser_module import Parse
from ranker import Ranker
import utils


class Searcher:

    def __init__(self, inverted_index, path):
        """
        :param inverted_index: dictionary of inverted index
        """
        self.parser = Parse()
        self.ranker = Ranker()
        self.inverted_index = inverted_index
        self.path = path

    def relevant_docs_from_posting(self, query, output_path, num_of_docs_in_corpus):
        """
        This function loads the posting list and count the amount of relevant documents per term.
        :param query: query
        :return: dictionary of relevant documents.
        """
        relevant_docs = {}  # key- tweet id , value
        terms = {}  # key- term , value- (tweet id, fi)
        docs_content = {}

        for term in query:
            try:
                if term not in self.inverted_index.keys():
                    continue
                else:
                    dict_of_doc_ids = self.extract_from_posting_file(term, self.inverted_index[term][3], self.path)
                    key = [*dict_of_doc_ids][0]
                    terms[term] = dict_of_doc_ids[key][0]
                    for doc in terms[term]:
                        if doc[0] not in docs_content.keys():
                            docs_content[doc[0]] = [[term, doc[1]]]
                            relevant_docs[doc[0]] = []
                        else:
                            exists = False
                            for pair in docs_content[doc[0]]:
                                if pair[0] == term:
                                    pair[1] += 1
                                    exists = True
                            if not exists:
                                docs_content[doc[0]].append([term, doc[1]])

            except:
                print('term {} not found in posting'.format(term))

        for word in query:
            for doc in docs_content.keys():
                exist = False
                for pair in docs_content[doc]:
                    if word == pair[0]:
                        relevant_docs[doc].append(pair[1])
                        exist = True
                if not exist:
                    relevant_docs[doc].append(0)

        # devide each element in the vector by thr max(f) of the doc. the information in docs_dict

        with open(output_path + '\\' + 'docs_dict.json') as f:
            for line in f:
                j_content = json.loads(line)
                key = [*j_content][0]
                if key in relevant_docs.keys():
                    max_tf = j_content[key][0]
                    relevant_docs[key] = np.divide(relevant_docs[key], max_tf)

        # calculate idf of each element in the vector (idf is log2(number of docs in the corpus \ df(from inverted index)

        # multiply tf*idf of each element

        # return relevant docs

        return relevant_docs

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

        #         if term not in self.inverted_index.keys():
        #             continue
        #         if term[0].isalpha():
        #             filename = term[0].lower()
        #         elif term[0] == '@':
        #             filename = 'tagging'
        #         elif term[0] == '#':
        #             filename = 'hashtag'
        #
        #         else:
        #
        #         with open(output_path + '\\' + term[0]. + '.json') as f:
        #             lines_in_file = self.inverted_indexx[term][3]
        #             line_counter = 0
        #             for line in f:
        #                 if line_counter == lines_in_file[0]:
        #                     j_content = json.loads(line)
        #                     key = [*j_content][0]
        #                     val = j_content[key]
        #                     if key not in relevant_docs.keys():
        #                         relevant_docs[key] = []
        #                     if term not in tweets.keys():
        #                         tweets[term] = []
        #                     tweets[term].append(key, val)
        #                     lines_in_file.remove(lines_in_file[0])
        #                     if not lines_in_file:
        #                         break
        #                 line_counter += 1
        #
        #     except:
        #         print('term {} not found in posting'.format(term))
        #
        # for key in relevant_docs.keys():
        #     for tweet_id in tweets:
        #         if key == tweets[tweet_id][0]:
        #             relevant_docs[key].append(tweets[tweet_id][1])
        #
        # with open(output_path + '\\' + 'docs_dict' + '.json') as f:

#
# s = Searcher()
# query = 'Computer science'
