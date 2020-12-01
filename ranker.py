import collections
import json
import math
import pickle

import numpy as np


class Ranker:
    def __init__(self):
        pass

    @staticmethod
    def rank_relevant_doc(relevant_doc):
        """
        This function provides rank for each relevant document and sorts them by their scores.
        The current score considers solely the number of terms shared by the tweet (full_text) and query.
        :param relevant_doc: dictionary of documents that contains at least one term from the query.
        :return: sorted list of documents by score
        """
        results= {}
        for doc in relevant_doc:
            sum_wij = sum(relevant_doc[doc])
            sum_wij2 = sum([x**2 for x in relevant_doc[doc]])
            sum_wiq2 = len(relevant_doc[doc])
            cos_sim = sum_wij / math.sqrt(sum_wij2 * sum_wiq2)
            results[doc] = cos_sim

        return sorted(results.items(), key=lambda item: item[1], reverse=True)

    @staticmethod
    def retrieve_top_k(sorted_relevant_doc, k=1):
        """
        return a list of top K tweets based on their ranking from highest to lowest
        :param sorted_relevant_doc: list of all candidates docs.
        :param k: Number of top document to return
        :return: list of relevant document
        """
        return sorted_relevant_doc[:k]



























