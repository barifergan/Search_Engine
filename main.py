import search_engine
from configuration import ConfigClass

if __name__ == '__main__':
    search_engine.main(ConfigClass.get__corpusPath(), ConfigClass.get__outputPath(), ConfigClass.get__toStem(), queries, num_docs_to_retrieve)

