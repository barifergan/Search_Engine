import json
import collections

from string import ascii_lowercase

from nltk.corpus import stopwords


class Indexer:

    def __init__(self, config):

        self.config = config
        self.inverted_idx = {}
        self.postingDict = {}
        self.waiting_list = {}
        self.file_line_indexes = {}
        self.docs_dict = {}
        self.stop_words = stopwords.words('english')

        for c in ascii_lowercase:
            self.file_line_indexes[c] = 1
        self.file_line_indexes['hashtag'] = 1
        self.file_line_indexes['tagging'] = 1
        self.file_line_indexes['number'] = 1
        self.file_line_indexes['other'] = 1

    def add_new_doc(self, documents, names_dict, output_path, counter_check):
        """
        This function perform indexing process for a document object.
        Saved information is captures via two dictionaries ('inverted index' and 'posting')
        :param document: a document need to be indexed.
        :return: -
        """

        doc_num_check = 1
        self.postingDict = {}
        self.docs_dict = {}
        for d in documents:
            document_dictionary = {}
            count_unique_words = 0
            doc_dictionary = d.term_doc_dictionary
            for term in doc_dictionary:
                if term.lower() not in self.stop_words:
                    document_dictionary[term] = doc_dictionary[term]

            term_num_check = 1
            for term in document_dictionary.keys():
                try:  # Update inverted index and posting
                    temp_term = ''
                    index_in_text = d.full_text.find(term)
                    if document_dictionary[term] == 1:  # save the amount of unique words in document
                        count_unique_words += 1
                    # first char is uppercase
                    if term[0].isupper():
                        # entity
                        if term in names_dict:
                            if names_dict[term] > 1:
                                if term not in self.inverted_idx.keys():
                                    temp_term = term
                                    self.inverted_idx[temp_term] = [1, d.tweet_date, index_in_text, []]
                                    self.postingDict[temp_term] = []
                                    if temp_term in self.waiting_list.keys():
                                        self.inverted_idx[temp_term][0] += 1
                                        self.postingDict[temp_term].append(
                                            (self.waiting_list[temp_term][0], self.waiting_list[temp_term][1]))
                                        del (self.waiting_list[temp_term])
                                else:
                                    temp_term = term
                                    self.inverted_idx[temp_term][0] += 1
                            else:
                                self.waiting_list[term] = (d.tweet_id, document_dictionary[term])

                        # regular word
                        elif term.lower() in self.inverted_idx.keys():
                            temp_term = term.lower()
                            self.inverted_idx[temp_term][0] += 1
                        elif term.upper() in self.inverted_idx.keys():
                            temp_term = term.upper()
                            self.inverted_idx[temp_term][0] += 1
                        else:
                            temp_term = term.upper()
                            self.inverted_idx[temp_term] = [1, d.tweet_date, index_in_text, []]
                            self.postingDict[temp_term] = []
                    # first char is number
                    elif term[0].isdigit():
                        temp_term = term.upper()
                        if term not in self.inverted_idx.keys():
                            self.inverted_idx[temp_term] = [1, d.tweet_date, index_in_text, []]
                            self.postingDict[temp_term] = []
                        else:
                            self.inverted_idx[temp_term][0] += 1

                    # first char is @
                    elif term[0] == '@':
                        temp_term = term
                        if term not in self.inverted_idx.keys():
                            self.inverted_idx[temp_term] = [1, d.tweet_date, index_in_text, []]
                            self.postingDict[temp_term] = []
                        else:
                            self.inverted_idx[temp_term][0] += 1
                    else:
                        if term.lower() in self.inverted_idx.keys():
                            temp_term = term.lower()
                            self.inverted_idx[temp_term][0] += 1
                        elif term.upper() in self.inverted_idx.keys():
                            temp_term = term.lower()
                            self.inverted_idx[temp_term] = self.inverted_idx[term.upper()]
                            del (self.inverted_idx[term.upper()])
                        else:
                            temp_term = term.lower()
                            self.inverted_idx[temp_term] = [1, d.tweet_date, index_in_text, []]
                            self.postingDict[temp_term] = []

                    if temp_term in self.postingDict.keys():
                        self.postingDict[temp_term].append((d.tweet_id, document_dictionary[term]))
                    term_num_check += 1
                except:
                    print('problem with the following key {}'.format(term))
                    print(document_dictionary.keys())
                    print(counter_check, doc_num_check, term_num_check)
            doc_num_check += 1

            if document_dictionary:  # if dict isn't empty
                self.docs_dict[d.tweet_id] = (
                    document_dictionary[max(document_dictionary, key=document_dictionary.get)], count_unique_words)

        sorted_posting_keys = sorted(self.postingDict.keys(), key=lambda x: x.lower())

        curr_char = ''
        i = 0
        while i < len(sorted_posting_keys):
            # for key in temp:
            if sorted_posting_keys[i][0].isalpha():
                curr_char = sorted_posting_keys[i][0].lower()
                with open(output_path + '\\' + curr_char + '.json', 'a') as outfile:
                    while i < len(sorted_posting_keys):
                        if sorted_posting_keys[i][0].lower() == curr_char:
                            for value in self.postingDict[sorted_posting_keys[i]]:
                                json.dump({value[0]: value[1]}, outfile)
                                outfile.write('\n')
                                to_add = ''
                                if sorted_posting_keys[i].lower() in self.inverted_idx.keys():
                                    to_add = sorted_posting_keys[i].lower()
                                elif sorted_posting_keys[i].upper() in self.inverted_idx.keys():
                                    to_add = sorted_posting_keys[i].upper()
                                else:
                                    to_add = sorted_posting_keys[i]
                                self.inverted_idx[to_add][3].append(self.file_line_indexes[curr_char])
                                self.file_line_indexes[curr_char] += 1
                            i += 1
                        else:
                            i += 1
                            break
            elif sorted_posting_keys[i][0] == '#':
                with open((output_path + '\\hashtag.json'), 'a') as outfile:
                    while i < len(sorted_posting_keys) and not sorted_posting_keys[i][0].isalpha():
                        for value in self.postingDict[sorted_posting_keys[i]]:
                            json.dump({value[0]: value[1]}, outfile)
                            outfile.write('\n')
                            self.inverted_idx[sorted_posting_keys[i]][3].append(self.file_line_indexes['hashtag'])
                            self.file_line_indexes['hashtag'] += 1
                        i += 1
            elif sorted_posting_keys[i][0] == '@':
                with open((output_path + '\\tagging.json'), 'a') as outfile:
                    while i < len(sorted_posting_keys) and not sorted_posting_keys[i][0].isalpha():
                        for value in self.postingDict[sorted_posting_keys[i]]:
                            json.dump({value[0]: value[1]}, outfile)
                            outfile.write('\n')
                            self.inverted_idx[sorted_posting_keys[i]][3].append(self.file_line_indexes['tagging'])
                            self.file_line_indexes['tagging'] += 1
                        i += 1
            elif sorted_posting_keys[i][0].isdigit():
                with open((output_path + '\\number.json'), 'a') as outfile:
                    while i < len(sorted_posting_keys) and not sorted_posting_keys[i][0].isalpha():
                        for value in self.postingDict[sorted_posting_keys[i]]:
                            json.dump({value[0]: value[1]}, outfile)
                            outfile.write('\n')
                            self.inverted_idx[sorted_posting_keys[i]][3].append(self.file_line_indexes['number'])
                            self.file_line_indexes['number'] += 1
                        i += 1

            else:
                with open((output_path + '\\other.json'), 'a') as outfile:
                    while i < len(sorted_posting_keys) and not sorted_posting_keys[i][0].isalpha():
                        for value in self.postingDict[sorted_posting_keys[i]]:
                            json.dump({value[0]: value[1]}, outfile)
                            outfile.write('\n')
                            self.inverted_idx[sorted_posting_keys[i]][3].append(self.file_line_indexes['other'])
                            self.file_line_indexes['other'] += 1
                        i += 1

        # restart posting dict

# config = ConfigClass()
# indexer1 = Indexer(config)
# dict = {'RT': '1', 'COVID': '4'}
# indexer1.add_new_doc(dict)
