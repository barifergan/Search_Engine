import json
import collections

from string import ascii_lowercase


class Indexer:

    def __init__(self, config):

        self.config = config
        self.inverted_idx = {}
        self.postingDict = {}
        self.waiting_list = {}
        self.file_line_indexes = {}
        self.docs_dict = {}
        self.unwanted_words = ['RT', 'http', 'https', 'www']
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
        self.postingDict = {}
        self.docs_dict = {}
        for d in documents:
            to_associations_matrix = {}
            count_unique_words = 0
            document_dictionary = d.term_doc_dictionary
            # Go over each term in the doc
            term_num_check = 1
            for term in document_dictionary.keys():
                try:  # Update inverted index and posting
                    # first char is uppercase
                    temp_term = ''
                    index_in_text = d.full_text.find(term)
                    if document_dictionary[term] == 1:  # save the amount of unique words in document
                        count_unique_words += 1
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

                    elif term[0].isdigit():
                        if term not in self.inverted_idx.keys():
                            temp_term = term.upper()
                            self.inverted_idx[temp_term] = [1, d.tweet_date, index_in_text, []]
                            self.postingDict[temp_term] = []
                        else:
                            temp_term = term.upper()
                            self.inverted_idx[temp_term][0] += 1

                    # first char is lowercase
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

                    to_associations_matrix[temp_term] = document_dictionary[term]

                except:
                    print('problem with the following key {}'.format(term))
                    print(document_dictionary.keys())
                    print(counter_check, doc_num_check, term_num_check)
            doc_num_check += 1

            if document_dictionary:  # if dict isn't empty
                self.docs_dict[d.tweet_id] = (
                    document_dictionary[max(document_dictionary, key=document_dictionary.get)], count_unique_words)

            with open((output_path + '\\associations_matrix.jason'), 'a') as outfile:
                json.dump(to_associations_matrix, outfile)
                outfile.write('\n')

        # to_remove_from_waiting_list = []
        # for waiting_term in self.waiting_list.keys():
        #     if names_dict[waiting_term] > 1:
        #         self.inverted_idx[waiting_term][0] += 1
        #         self.postingDict[waiting_term].append(self.waiting_list[waiting_term])
        #         to_remove_from_waiting_list.append(waiting_term)
        #
        # for l in to_remove_from_waiting_list:
        #     del(self.waiting_list[l])

        temp = sorted(self.postingDict.keys(), key=lambda x: x.lower())

        curr_char = ''
        i = 0
        while i < len(temp):
            # for key in temp:
            if not temp[i][0].isalpha():
                with open((output_path + '\other.jason'), 'a') as outfile:
                    while i < len(temp) and not temp[i][0].isalpha():
                        for value in self.postingDict[temp[i]]:
                            json.dump({value[0]: value[1]}, outfile)
                            outfile.write('\n')
                            self.inverted_idx[temp[i]][3].append(self.file_line_indexes['other'])
                            self.file_line_indexes['other'] += 1
                        i += 1
            else:
                curr_char = temp[i][0].lower()
                with open(output_path + '\\' + curr_char + '.jason', 'a') as outfile:
                    while i < len(temp):
                        if temp[i][0].lower() == curr_char:
                            for value in self.postingDict[temp[i]]:
                                json.dump({value[0]: value[1]}, outfile)
                                outfile.write('\n')
                                to_add = ''
                                if temp[i].lower() in self.inverted_idx.keys():
                                    to_add = temp[i].lower()
                                elif temp[i].upper() in self.inverted_idx.keys():
                                    to_add = temp[i].upper()
                                else:
                                    to_add = temp[i]
                                self.inverted_idx[to_add][3].append(self.file_line_indexes[curr_char])
                                self.file_line_indexes[curr_char] += 1
                            i += 1
                        else:
                            i += 1
                            break

        # restart posting dict

# config = ConfigClass()
# indexer1 = Indexer(config)
# dict = {'RT': '1', 'COVID': '4'}
# indexer1.add_new_doc(dict)
