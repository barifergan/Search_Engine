import search_engine
from configuration import ConfigClass

if __name__ == '__main__':
    config = ConfigClass()
    search_engine.main(config.get__corpusPath(), 'C:\\Users\\ronen\\PycharmProjects\\Search_Engine\\json_files')#, stemming, queries, num_docs_to_retrieve)
