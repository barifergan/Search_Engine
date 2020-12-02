import search_engine
from configuration import ConfigClass

if __name__ == '__main__':
    search_engine.main(ConfigClass.get__corpusPath(), ConfigClass.get__outputPath(), ConfigClass.to_stem())# queries, num_docs_to_retrieve)


# def main(corpus_path) :#, output_path, stemming, queries, num_docs_to_retrieve):

# def test_parse(path):
    # reader1 = reader.ReadFile(path)
    # text = reader1.read_file('covid19_07-11.snappy.parquet')
    # parse1 = parser_module.Parse()
    # sentence = parse1.parse_sentence(text)
    # document = parse1.parse_doc(sentence)
    # print(document)

# path = 'C:\\Users\\barif\\PycharmProjects\\Search_Engine\\Data'
