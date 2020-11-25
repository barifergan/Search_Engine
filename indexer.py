import json

from configuration import ConfigClass


class Indexer:

    def __init__(self, config):
        self.inverted_idx = {}
        self.postingDict = {}
        self.config = config

    def add_new_doc(self, document):
        """
        This function perform indexing process for a document object.
        Saved information is captures via two dictionaries ('inverted index' and 'posting')
        :param document: a document need to be indexed.
        :return: -
        """

        # document_dictionary = document
        document_dictionary = document.term_doc_dictionary
        for term in document_dictionary.keys():
            posting_dict = {document.tweet_id: document_dictionary[term]}
            with open(term[0].lower() + ".jason", "w") as outfile:
                json.dump(posting_dict, outfile)

            if term not in self.inverted_idx.keys():
                self.inverted_idx[term] = 1

        with open("a.jason", "w") as outfile:
            json.dump(document, outfile)
        document_dictionary['Ronen'] = 3
        with open("a.jason", "w") as outfile:
            json.dump(document, outfile)

        # Go over each term in the doc
        for term in document_dictionary.keys():
            try:
                # Update inverted index and posting
                if term not in self.inverted_idx.keys():
                    self.inverted_idx[term] = 1
                    # self.postingDict[term] = []

                else:
                    self.inverted_idx[term] += 1

                self.postingDict[term].append((document.tweet_id, document_dictionary[term]))

            except:
                print('problem with the following key {}'.format(term[0]))






# config = ConfigClass()
# indexer1 = Indexer(config)
# dict = {'RT': '1', 'COVID': '4'}
# indexer1.add_new_doc(dict)
