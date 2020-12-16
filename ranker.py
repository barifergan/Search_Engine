import math
import numpy as np
from numpy import dot
from numpy.linalg import norm


class Ranker:
    def __init__(self):
        pass

    @staticmethod
    def rank_relevant_doc(relevant_docs):
        """
        This function provides rank for each relevant document and sorts them by their scores.
        The current score considers solely the number of terms shared by the tweet (full_text) and query.
        :param relevant_docs: dictionary of documents that contains at least one term from the query.
        :return: sorted list of documents by score
        """
        ranked_results = {}
        for doc in relevant_docs:
            sum_wij = sum(relevant_docs[doc])
            sum_wij2 = sum([x ** 2 for x in relevant_docs[doc]])
            sum_wiq2 = len(relevant_docs[doc])
            cos_sim = sum_wij / math.sqrt(sum_wij2 * sum_wiq2)
            ranked_results[doc] = cos_sim

        return sorted(ranked_results.items(), key=lambda item: item[1], reverse=True)

    @staticmethod
    def retrieve_top_k(sorted_relevant_doc, k=1):
        """
        return a list of top K tweets based on their ranking from highest to lowest
        :param sorted_relevant_doc: list of all candidates docs.
        :param k: Number of top document to return
        :return: list of relevant document
        """
        if k > 2000:
            k = 2000
        return sorted_relevant_doc[:k]
