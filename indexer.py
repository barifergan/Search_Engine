import json
import string
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
        self.stop_words.extend(['https', 'http', 'rt', 'www', 't.co'])
        self.stop_words.extend(list(string.ascii_lowercase))
        self.num_of_docs_in_corpus = 0
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
                    index_in_text = [n for n, x in enumerate(d.full_text.split()) if x == term]
                    if document_dictionary[term] == 1:  # save the amount of unique words in document
                        count_unique_words += 1
                    # first char is uppercase
                    if term[0].isupper():
                        # entity
                        if term in names_dict:
                            if names_dict[term] > 1:
                                if term not in self.inverted_idx.keys():
                                    temp_term = term
                                    self.inverted_idx[temp_term] = [1, []]
                                    self.postingDict[temp_term] = []
                                    if temp_term in self.waiting_list.keys():
                                        self.inverted_idx[temp_term][0] += 1
                                        self.postingDict[temp_term].append(
                                            (self.waiting_list[temp_term][0], self.waiting_list[temp_term][1],
                                             self.waiting_list[temp_term][2]))
                                        del (self.waiting_list[temp_term])
                                else:
                                    temp_term = term
                                    self.inverted_idx[temp_term][0] += 1
                            else:
                                self.waiting_list[term] = (d.tweet_id, document_dictionary[term], index_in_text)

                        # regular word
                        elif term.lower() in self.inverted_idx.keys():
                            temp_term = term.lower()
                            self.inverted_idx[temp_term][0] += 1
                            if temp_term not in self.postingDict.keys():
                                self.postingDict[temp_term] = []
                        elif term.upper() in self.inverted_idx.keys():
                            temp_term = term.upper()
                            self.inverted_idx[temp_term][0] += 1
                            if temp_term not in self.postingDict.keys():
                                self.postingDict[temp_term] = []
                        else:
                            temp_term = term.upper()
                            self.inverted_idx[temp_term] = [1, []]
                            self.postingDict[temp_term] = []

                    # first char is number
                    elif term[0].isdigit():
                        temp_term = term.upper()
                        if term not in self.inverted_idx.keys():
                            self.inverted_idx[temp_term] = [1, []]
                            self.postingDict[temp_term] = []
                        elif term not in self.postingDict.keys():
                            self.postingDict[temp_term] = []
                            self.inverted_idx[temp_term][0] += 1
                        else:
                            self.inverted_idx[temp_term][0] += 1



                    # first char is @
                    elif term[0] == '@':
                        temp_term = term
                        if term not in self.inverted_idx.keys():
                            self.inverted_idx[temp_term] = [1, []]
                            self.postingDict[temp_term] = []
                        elif term not in self.postingDict.keys():
                            self.postingDict[temp_term] = []
                            self.inverted_idx[temp_term][0] += 1
                        else:
                            self.inverted_idx[temp_term][0] += 1

                    # other
                    else:
                        if term.lower() in self.inverted_idx.keys():
                            temp_term = term.lower()
                            self.inverted_idx[temp_term][0] += 1
                            if temp_term not in self.postingDict.keys():
                                self.postingDict[temp_term] = []
                        elif term.upper() in self.inverted_idx.keys():
                            temp_term = term.lower()
                            self.inverted_idx[temp_term] = self.inverted_idx[term.upper()]
                            del (self.inverted_idx[term.upper()])
                            if term.upper() not in self.postingDict.keys():
                                self.postingDict[temp_term] = []
                            else:
                                self.postingDict[temp_term] = self.postingDict[term.upper()]
                                del (self.postingDict[term.upper()])
                        else:
                            temp_term = term.lower()
                            self.inverted_idx[temp_term] = [1, []]
                            self.postingDict[temp_term] = []

                    if temp_term in self.postingDict.keys():
                        self.postingDict[temp_term].append((d.tweet_id, document_dictionary[term], index_in_text))
                    term_num_check += 1

                except:
                    print('problem with the following key {}'.format(term))
                    print(document_dictionary.keys())
                    print(counter_check, self.num_of_docs_in_corpus, term_num_check)
            self.num_of_docs_in_corpus += 1

            if document_dictionary:  # if dict isn't empty
                self.docs_dict[d.tweet_id] = (
                    document_dictionary[max(document_dictionary, key=document_dictionary.get)], d.tweet_date,
                    count_unique_words)

        with open('docs_dict.json', 'a') as outfile:
            for key in self.docs_dict.keys():
                json.dump({key: self.docs_dict[key]}, outfile)
                outfile.write('\n')

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
                            json.dump({sorted_posting_keys[i]: self.postingDict[sorted_posting_keys[i]]}, outfile)
                            outfile.write('\n')
                            if ' ' in sorted_posting_keys[i]:
                                to_add = sorted_posting_keys[i]
                            elif sorted_posting_keys[i].lower() in self.inverted_idx.keys():
                                to_add = sorted_posting_keys[i].lower()
                            elif sorted_posting_keys[i].upper() in self.inverted_idx.keys():
                                to_add = sorted_posting_keys[i].upper()
                            else:
                                to_add = sorted_posting_keys[i]
                            self.inverted_idx[to_add][1].append(self.file_line_indexes[curr_char])
                            self.file_line_indexes[curr_char] += 1

                            i += 1
                        else:
                            break
            elif sorted_posting_keys[i][0] == '#':
                with open((output_path + '\\hashtag.json'), 'a') as outfile:
                    while i < len(sorted_posting_keys) and sorted_posting_keys[i][0] == '#':
                        json.dump({sorted_posting_keys[i]: self.postingDict[sorted_posting_keys[i]]}, outfile)
                        outfile.write('\n')
                        self.inverted_idx[sorted_posting_keys[i]][1].append(self.file_line_indexes['hashtag'])
                        self.file_line_indexes['hashtag'] += 1
                        i += 1
            elif sorted_posting_keys[i][0] == '@':
                with open((output_path + '\\tagging.json'), 'a') as outfile:
                    while i < len(sorted_posting_keys) and sorted_posting_keys[i][0] == '@':
                        json.dump({sorted_posting_keys[i]: self.postingDict[sorted_posting_keys[i]]}, outfile)
                        outfile.write('\n')
                        self.inverted_idx[sorted_posting_keys[i]][1].append(self.file_line_indexes['tagging'])
                        self.file_line_indexes['tagging'] += 1
                        i += 1
            elif sorted_posting_keys[i][0].isdigit():
                with open((output_path + '\\number.json'), 'a') as outfile:
                    while i < len(sorted_posting_keys) and sorted_posting_keys[i][0].isdigit():
                        json.dump({sorted_posting_keys[i]: self.postingDict[sorted_posting_keys[i]]}, outfile)
                        outfile.write('\n')
                        self.inverted_idx[sorted_posting_keys[i]][1].append(self.file_line_indexes['number'])
                        self.file_line_indexes['number'] += 1
                        i += 1
            else:
                with open((output_path + '\\other.json'), 'a') as outfile:
                    while i < len(sorted_posting_keys) and not sorted_posting_keys[i][0].isalpha() and not \
                    sorted_posting_keys[i][0] == '@' and not sorted_posting_keys[i][0].isdigit() and not \
                    sorted_posting_keys[i][0] == '#':
                        json.dump({sorted_posting_keys[i]: self.postingDict[sorted_posting_keys[i]]}, outfile)
                        outfile.write('\n')
                        self.inverted_idx[sorted_posting_keys[i]][1].append(self.file_line_indexes['other'])
                        self.file_line_indexes['other'] += 1
                        i += 1
