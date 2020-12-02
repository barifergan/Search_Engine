import collections
import json
import os
import pickle
import time

import utils
from reader import ReadFile
from configuration import ConfigClass
from parser_module import Parse
from indexer import Indexer
from searcher import Searcher
from global_method import GlobalMethod
import numpy as np




def run_engine():  # , stemming, queries, num_docs_to_retrieve):
    """

    :return:
    """
    start_time = time.time()

    config = ConfigClass()
    r = ReadFile(ConfigClass.get__corpusPath())
    p = Parse()
    indexer = Indexer(config)
    names_and_entities = {}

    corpus_path = ConfigClass.get__corpusPath()
    parsed_documents = []
    counter_check = 1
    num_of_docs_in_corpus = 0

    for subdir, dirs, files in os.walk(corpus_path):
        for file in files:
            file_type = file[-8:]
            if file_type == '.parquet':
                file_name = file
                documents_list = r.read_file(file_name)
                for idx, document in enumerate(documents_list):
                    # parse the document
                    exist_in_doc = False
                    parsed_document = p.parse_doc(document)
                    # index the document data
                    for term in parsed_document.term_doc_dictionary:

                        if (len(term) > 0) and (term[0].isupper()) and ' ' in term:
                            if term not in names_and_entities.keys():
                                names_and_entities[term] = 1
                                exist_in_doc = True

                            elif exist_in_doc is True:
                                continue
                            else:
                                names_and_entities[term] += 1
                                exist_in_doc = True

                    parsed_documents.append(parsed_document)
                    limit_to_index = 10000
                    if len(parsed_documents) == limit_to_index:
                        indexer.add_new_doc(parsed_documents, names_and_entities, ConfigClass.get__outputPath(),
                                            counter_check)
                        print('Parsed and indexed ' + str(counter_check * limit_to_index) + ' files')
                        counter_check += 1
                        parsed_documents = []
                        num_of_docs_in_corpus += limit_to_index

    print('Finished parsing and indexing. Starting to export files')

    utils.save_obj(indexer.inverted_idx, "inverted_idx")
    # utils.save_obj(indexer.postingDict, "posting")

    end_parse_index_time = time.time()
    print("--- %s seconds ---" % (end_parse_index_time - start_time))


# --------------------------------------------------------------end here-------------------------------------------------------------------------

def load_index():
    print('Load inverted index')
    inverted_index = utils.load_obj("inverted_idx")
    return inverted_index


def search_and_rank_query(query, inverted_index, k):
    if query is list:
        query = ' '.join(query)

    num_of_docs_in_corpus = 10000000

    p = Parse()
    query_as_list = p.parse_sentence(query)
    searcher = Searcher(inverted_index)
    # matrix = GlobalMethod.build_matrix()
    # for key, value in matrix.items():
    #     print(key, ' : ', value)
    # query_as_list = GlobalMethod.expand_query(query_as_list)
    relevant_docs = searcher.relevant_docs_from_posting(query_as_list, num_of_docs_in_corpus)
    ranked_docs = searcher.ranker.rank_relevant_doc(relevant_docs)
    return searcher.ranker.retrieve_top_k(ranked_docs, k)


def main(corpus_path, output_path, stemming):  # queries, num_docs_to_retrieve):

    start_time = time.time()

    run_engine()  # , stemming, queries, num_docs_to_retrieve)

    ConfigClass.set__corpusPath(corpus_path)
    ConfigClass.set__outputPath(output_path)
    ConfigClass.set__toStem(stemming)

    end_time = time.time()
    print("--- %s seconds ---" % (end_time - start_time))

    query = input("Please enter a query: ")
    k = int(input("Please enter number of docs to retrieve: "))
    inverted_index = load_index()
    for doc_tuple in search_and_rank_query(query, inverted_index, k):
        print('tweet id: {}, score (unique common words with query): {}'.format(doc_tuple[0], doc_tuple[1]))
