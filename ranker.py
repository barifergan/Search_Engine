import json

import numpy as np


class Ranker:
    def __init__(self, inverted_index):

        relevant_words = []
        for term in inverted_index.keys():
            avg = inverted_index[term][0] / 1000000
            if avg < 0.5:
                relevant_words.append(inverted_index[term])

        relevant_words = sorted(relevant_words)

        associations_matrix = np.zeros(len(relevant_words)+1, dtype=int)
        row = 1
        col = 1
        for word in relevant_words:
            associations_matrix[0][col] = word
            associations_matrix[row][0] = word
            row += 1
            col += 1

        i = 1
        for word in relevant_words:
            list_of_rows = inverted_index[word][3]
            counter = 0
            if word[0].isalpha():
                with open(output_path + '\\' + word[0] + '.jason') as f:
                    for line in f:
                        if counter == list_of_rows[0]:
                            j_content = json.loads(line)
                            list_of_rows.remove(list_of_rows[0])
                        counter += 1


    @staticmethod
    def rank_relevant_doc(relevant_doc):
        """
        This function provides rank for each relevant document and sorts them by their scores.
        The current score considers solely the number of terms shared by the tweet (full_text) and query.
        :param relevant_doc: dictionary of documents that contains at least one term from the query.
        :return: sorted list of documents by score
        """
        return sorted(relevant_doc.items(), key=lambda item: item[1], reverse=True)

    @staticmethod
    def retrieve_top_k(sorted_relevant_doc, k=1):
        """
        return a list of top K tweets based on their ranking from highest to lowest
        :param sorted_relevant_doc: list of all candidates docs.
        :param k: Number of top document to return
        :return: list of relevant document
        """
        return sorted_relevant_doc[:k]

    def create_matrix(self, inverted_index):

        relevant_terms = []
        for term in inverted_index.keys():
            if inverted_index[term][0] > 5:
                relevant_terms.append(term)

        relevant_words = sorted(relevant_terms)

        for term1 in relevant_words:
            lines_in_file = inverted_index[term1][3]
            tweet_ids_and_freq_of_term1 = []
            line_counter = 0
            if term1[0].isalpha():
                with open(output_path + '\\' + term1[0] + '.jason') as f:
                    for line in f:
                        if line_counter == lines_in_file[0]:
                            j_content = json.loads(line)
                            tweet_ids_and_freq_of_term1.append(j_content)
                            lines_in_file.remove(lines_in_file[0])
                            if not lines_in_file:
                                break
                        line_counter += 1
            else:
                with open(output_path + '\\' + 'other' + '.jason') as f:
                    for line in f:
                        if line_counter == lines_in_file[0]:
                            j_content = json.loads(line)
                            tweet_ids_and_freq_of_term1.append(j_content)
                            lines_in_file.remove(lines_in_file[0])
                            if not lines_in_file:
                                break
                        line_counter += 1

            for term2 in relevant_words:
                lines_in_file = inverted_index[term2][3]
                tweet_ids_and_freq_of_term2 = []
                line_counter = 0
                if term2[0].isalpha():
                    with open(output_path + '\\' + term2[0] + '.jason') as f:
                        for line in f:
                            if line_counter == lines_in_file[0]:
                                j_content = json.loads(line)
                                tweet_ids_and_freq_of_term2.append(j_content)
                                lines_in_file.remove(lines_in_file[0])
                                if not lines_in_file:
                                    break
                            line_counter += 1
                else:
                    with open(output_path + '\\' + 'other' + '.jason') as f:
                        for line in f:
                            if line_counter == lines_in_file[0]:
                                j_content = json.loads(line)
                                tweet_ids_and_freq_of_term2.append(j_content)
                                lines_in_file.remove(lines_in_file[0])
                                if not lines_in_file:
                                    break
                            line_counter += 1

                cii = 0
                cij = 0
                cjj = 0
                for tup1 in tweet_ids_and_freq_of_term1:
                    for tup2 in tweet_ids_and_freq_of_term2:
                        if term1 == term2:
                            cii += tup1[1] * tup2[1]
                        elif tup1[0] == tup2[0]:
                            cij +=

























