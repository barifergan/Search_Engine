import json

from parser_module import Parse
from ranker import Ranker
import utils


class Searcher:

    def __init__(self, inverted_index):
        """
        :param inverted_index: dictionary of inverted index
        """
        self.parser = Parse()
        self.ranker = Ranker(inverted_index)
        self.inverted_index = inverted_index

    def relevant_docs_from_posting(self, query):
        """
        This function loads the posting list and count the amount of relevant documents per term.
        :param query: query
        :return: dictionary of relevant documents.
        """
        relevant_docs = {} # key- tweet id , value
        tweets = {} # key- term , value- (tweet id, fi)
        for term in query:
            try:
                if term not in self.inverted_index.keys():
                    continue
                if term[0].isalpha():
                    filename = term[0].lower()
                elif term[0] == '@':
                    filename = 'tagging'
                elif term[0] == '#':
                    filename = 'hashtag'

                else:

                with open(output_path + '\\' + term[0]. + '.json') as f:
                    lines_in_file = self.inverted_indexx[term][3]
                    line_counter = 0
                    for line in f:
                        if line_counter == lines_in_file[0]:
                            j_content = json.loads(line)
                            key = [*j_content][0]
                            val = j_content[key]
                            if key not in relevant_docs.keys():
                                relevant_docs[key] = []
                            if term not in tweets.keys():
                                tweets[term] = []
                            tweets[term].append(key, val)
                            lines_in_file.remove(lines_in_file[0])
                            if not lines_in_file:
                                break
                        line_counter += 1

            except:
                print('term {} not found in posting'.format(term))

        for key in relevant_docs.keys():
            for tweet_id in tweets:
                if key == tweets[tweet_id][0]:
                    relevant_docs[key].append(tweets[tweet_id][1])

        with open(output_path + '\\' + 'docs_dict' + '.json') as f:



        return relevant_docs


