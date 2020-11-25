import json
import collections

from string import ascii_lowercase


class Indexer:

    def __init__(self, config):
        self.inverted_idx = {}
        self.postingDict = {}
        self.config = config
        self.file_line_indexes = {}
        for c in ascii_lowercase:
            self.file_line_indexes[c] = 0
        self.file_line_indexes['other'] = 0

    def add_new_doc(self, documents, names_dict, output_path, counter_check):
        """
        This function perform indexing process for a document object.
        Saved information is captures via two dictionaries ('inverted index' and 'posting')
        :param document: a document need to be indexed.
        :return: -
        """

        doc_num_check = 1
        for d in documents:
            # document_dictionary = document
            document_dictionary = d.term_doc_dictionary
            # for term in document_dictionary.keys():
            #     posting_dict = {document.tweet_id: document_dictionary[term]}
            #     with open(term[0].lower() + ".jason", "w") as outfile:
            #         json.dump(posting_dict, outfile)
            #
            #     if term not in self.inverted_idx.keys():
            #         self.inverted_idx[term] = 1

            # Go over each term in the doc
            term_num_check = 1
            for term in document_dictionary.keys():
                try:
                    # Update inverted index and posting
                    if term not in self.inverted_idx.keys():
                        if term[0].isupper():
                            # entity
                            if ' ' in term:
                                if term in names_dict and names_dict[term] > 1:
                                    # TODO if to save parts of the entity
                                    self.inverted_idx[term] = [1]
                                    self.postingDict[term] = []
                            # regular word
                            else:
                                # TODO decide if we save lower or upper case
                                self.inverted_idx[term] = [1]
                                self.postingDict[term] = []
                        else:
                            self.inverted_idx[term] = [1]
                            self.postingDict[term] = []

                    else:
                        self.inverted_idx[term][0] += 1

                    if term in self.postingDict.keys():
                        self.postingDict[term].append((d.tweet_id, document_dictionary[term]))
                    term_num_check += 1
                except:
                    print('problem with the following key {}'.format(term))
                    print(document_dictionary.keys())
                    print(counter_check, doc_num_check, term_num_check)
            doc_num_check += 1


        # SORT POSTINGDICT!!!!!!!!!!!
        temp = sorted(self.postingDict.keys(), key=lambda x: x.lower())

        curr_char = ''
        i = 0
        while i < len(temp):
            # for key in temp:
            if not temp[i][0].isalpha():
                file = output_path + '\other.jason'
                with open((output_path + '\other.jason'), 'w') as outfile:
                    while i < len(temp) and not temp[i][0].isalpha():
                        for value in self.postingDict[temp[i]]:
                            json.dump({value[0]: value[1]}, outfile)
                            outfile.write('\n')
                            self.inverted_idx[temp[i]].append(('other.jason', self.file_line_indexes['other']))
                            self.file_line_indexes['other'] += 1
                        i += 1
            else:
                curr_char = temp[i][0].lower()
                with open(output_path + '\\' + curr_char + '.jason', 'w') as outfile:
                    while i < len(temp):
                        if temp[i][0].lower() == curr_char:
                            for value in self.postingDict[temp[i]]:
                                json.dump({value[0]: value[1]}, outfile)
                                outfile.write('\n')
                                self.inverted_idx[temp[i]].append(
                                    (curr_char + ".jason", self.file_line_indexes[curr_char]))
                                self.file_line_indexes[curr_char] += 1
                            i += 1
                        else:
                            i += 1
                            break

# config = ConfigClass()
# indexer1 = Indexer(config)
# dict = {'RT': '1', 'COVID': '4'}
# indexer1.add_new_doc(dict)
