import search_engine
import reader
import parser_module


if __name__ == '__main__':
    search_engine.main()

def parse_test(path):
    reader1 = reader.ReadFile(path)
    text = reader1.open_folder(path)
    parse1 = parser_module.Parse()
    sentence = parse1.parse_sentence(text)
    parse1.parse_doc(sentence)

test = parse_test('C:\\Users\\barif\\PycharmProjects\\Search_Engine\\Data')




