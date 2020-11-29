import numpy as np


class Ranker:
    def __init__(self, inverted_index):

        relevant_words = []
        for term in inverted_index.keys():
            avg = inverted_index[term][0] / 1000000
            if avg < 0.5:
                relevant_words.append(inverted_index[term])

        associations_matrix = np.zeros(len(relevant_words)+1, dtype=int)
        row = 1
        col = 1
        for word in relevant_words:
            associations_matrix[0][col] = word
            associations_matrix[row][0] = word
            row += 1
            col += 1

        i = 1
        # for word_row in associations_matrix:











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
