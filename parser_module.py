from nltk import RegexpTokenizer, TweetTokenizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from document import Document
import re
import math


class Parse:

    def __init__(self):
        self.stop_words = stopwords.words('english')

    def parse_sentence(self, text):
        """
        This function tokenize, remove stop words and apply lower case for every word within the text
        :param text:
        :return:
        """
        space_tokenizer = RegexpTokenizer("\s+", gaps=True)
        text_tokens = space_tokenizer.tokenize(re.sub(r'[^\x00-\x7f]', r' ', text))
        after_parse = []

        # tweet_tokenizer = TweetTokenizer()
        # text_tokens = tweet_tokenizer.tokenize(text)

        text_tokens_without_stopwords = [w.lower() for w in text_tokens if w not in self.stop_words]

        for i in range(len(text_tokens_without_stopwords)):
            if text_tokens_without_stopwords[i][0] == '#':
                hashtag = self.parse_hashtags(text_tokens_without_stopwords[i])
                after_parse.append(hashtag)


        return text_tokens_without_stopwords

    def parse_doc(self, doc_as_list):
        """
        This function takes a tweet document as list and break it into different fields
        :param doc_as_list: list re-preseting the tweet.
        :return: Document object with corresponding fields.
        """
        tweet_id = doc_as_list[0]
        tweet_date = doc_as_list[1]
        full_text = doc_as_list[2]
        url = doc_as_list[3]
        indices = doc_as_list[4]
        retweet_text = doc_as_list[5]
        retweet_url = doc_as_list[6]
        retweet_indices = doc_as_list[7]
        quote_text = doc_as_list[8]
        quote_url = doc_as_list[9]
        quote_indices = doc_as_list[10]
        retweet_quote_text = doc_as_list[11]
        retweet_quote_url = doc_as_list[12]
        retweet_quote_indices = doc_as_list[13]
        term_dict = {}
        text_to_tokenize = full_text + ' ' + url + ' ' + ' ' + quote_text + ' ' + quote_url
        tokenized_text = self.parse_sentence(text_to_tokenize)

        doc_length = len(tokenized_text)  # after text operations.

        for term in tokenized_text:
            if term not in term_dict.keys():
                term_dict[term] = 1
            else:
                term_dict[term] += 1

        document = Document(tweet_id, tweet_date, full_text, url, indices, retweet_text, retweet_url, retweet_indices,
                            quote_text,
                            quote_url, quote_indices, retweet_quote_text, retweet_quote_url, retweet_quote_indices,
                            term_dict, doc_length)
        return document

    def parse_hashtags(self, token):
        # txt_list = text.split()
        hashtag_lst = []
        # for word in txt_list:
        #     if word[0] == '#':
        hashtag = token.replace('#', '')
        if hashtag.find('_') != -1:
            hashtag_lst = hashtag.split('_')
            merge_words = hashtag.replace('_', '')
            hashtag_lst.append('#' + merge_words)

        elif any(x.isupper() for x in hashtag):
            pos = [i for i, e in enumerate(hashtag + 'A') if e.isupper()]
            pos.insert(0, 0)
            hashtag_lower = hashtag.lower()
            hashtag_lst = [hashtag_lower[pos[j]:pos[j + 1]] for j in range(len(pos) - 1)]
            hashtag_lst.append('#' + hashtag_lower)

        else:
            hashtag_lst.append(hashtag)

        return hashtag_lst

    def parse_url(self, text):

        url_parts = re.split('://|/|:|=', text)

        sub_url1 = url_parts[1][0:3]
        sub_url2 = url_parts[1][4:]
        url_parts.pop(1)
        url_parts.insert(1, sub_url1)
        url_parts.insert(2, sub_url2)
        for i in range(len(url_parts)):
            if url_parts[i][0] == '?':
                word = url_parts[i][1:]
                url_parts[i] = word

        # print(url_parts)
        return url_parts

    def parse_tagging(self, text):
        txt_list = text.split()
        tag_lst = []
        for word in txt_list:
            if word[0] == '@':
                tag_lst.append(word[1:])
        return tag_lst

    def parse_percentages(self, text):
        txt_list = text.split()
        percent_lst = []
        for i in range(len(txt_list)):
            print(txt_list[i])
            if txt_list[i].replace('.', '', 1).isdigit():
                if txt_list[i + 1] == 'percent' or txt_list[i + 1] == 'percentage':
                    percent_lst.append(txt_list[i] + '%')
            elif txt_list[i][-1] == '%' and txt_list[i][:-1].isdigit():
                percent_lst.append(txt_list[i][:-1] + '%')

        return percent_lst

    def parse_numbers(self, text):
        txt_list = text.split()
        numbers_list = []
        for i in range(len(txt_list)):
            if txt_list[i].replace(',', '').replace('.', '', 1).isdigit():
                if '.' in txt_list[i]:
                    curr_num = float(txt_list[i].replace(',', ''))
                else:
                    curr_num = int(txt_list[i].replace(',', ''))

                if curr_num < 1000:
                    if txt_list[i + 1] == "Thousand":
                        numbers_list.append(str(curr_num) + 'K')
                    elif txt_list[i + 1] == "Million":
                        numbers_list.append(str(curr_num) + 'M')
                    elif txt_list[i + 1] == "Billion":
                        numbers_list.append(str(curr_num) + 'B')
                    elif (txt_list[i].replace('/', '').isdigit()) & ('/' in txt_list[i + 1]):
                        numbers_list.append(str(curr_num) + " " + txt_list[i + 1])
                    else:
                        numbers_list.append(str(curr_num))

                elif 1000 <= curr_num < 1000000:
                    if txt_list[i + 1] == "Million":
                        curr_num = math.floor((curr_num / 1000) * 10 ** 3) / 10 ** 3
                        numbers_list.append(str(curr_num) + 'B')
                    else:
                        curr_num = math.floor((curr_num / 1000) * 10 ** 3) / 10 ** 3
                        numbers_list.append(str(curr_num) + 'K')
                elif 1000000 <= curr_num < 1000000000:
                    curr_num = math.floor((curr_num / 1000000) * 10 ** 3) / 10 ** 3
                    numbers_list.append(str(curr_num) + 'M')
                elif curr_num >= 1000000000:
                    curr_num = math.floor((curr_num / 1000000000) * 10 ** 3) / 10 ** 3
                    numbers_list.append(str(curr_num) + 'B')
        # print(txt_list)
        # print(numbers_list)

        return numbers_list

    def parse_names_and_entities(self, text):
        text_list = text.split()
        curr_name = ''
        names_list = set()
        i = 0
        while i < len(text_list):
            j = 0
            if text_list[i][0].isupper():
                curr_name = text_list[i]
                if i != len(text_list)-1:
                    j = i+1

                    while j < len(text_list):
                        if text_list[j][0].isupper():
                            curr_name += " " + text_list[j]
                            j += 1
                        else:
                            names_list.add(curr_name)
                            break
                    i = j-1
                i += 1

            else:
                i += 1

        names_list.add(curr_name)

        print(names_list)
        return names_list



# text1 = '#virusIsBad #infection_blabla #animals \n\nhttps://t.co/NrBpYOp0dR'
# text2 = 'https://www.instagram.com/p/CD7fAPWs3WM/?igshid=o9kf0ugp1l8x'
# text3 = 'this is @Ronen and @Bar'
# text4 = '6% 106 percent 10.6 percentage'
# text5 = '1000 Million 204 14.7 123,470.11 1.2 Million 10,123 1010.56 10,123,000 55 Million 10123000000 10,123,000,000 55 Billion '
# text6 = 'Alexandria Ocasio-Cortez is Doctor Cortez'
parse1 = Parse()
# # parse1.parse_hashtags(text1)
# parse1.parse_url(text2)
# parse1.parse_tagging(text3)
# parse1.parse_precentages(text4)
# parse1.parse_numbers(text5)
# parse1.parse_names_and_entities(text6)


