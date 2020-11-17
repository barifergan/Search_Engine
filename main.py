import search_engine
import reader
import parser_module


if __name__ == '__main__':
    search_engine.main()

def main(corpus_path,output_path,stemming,queries,num_docs_to_retrieve):
    reader1 = reader.ReadFile(corpus_path)
    text = reader1.open_folder(path)
    parse1 = parser_module.Parse()
    sentence = parse1.parse_sentence(text)
    parse1.parse_doc(sentence)

test = main('C:\\Users\\barif\\PycharmProjects\\Search_Engine\\Data')




