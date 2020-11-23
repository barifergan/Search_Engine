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
        # space_tokenizer = RegexpTokenizer("\s+", gaps=True)
        # text_tokens = space_tokenizer.tokenize(re.sub(r'[^\x00-\x7f]', r' ', text))
        after_parse = []

        tweet_tokenizer = TweetTokenizer()
        text_tokens = tweet_tokenizer.tokenize(re.sub(r'[^\x00-\x7f]', r' ', text))

        text_tokens_without_stopwords = [w for w in text_tokens if w.lower() not in self.stop_words]
        symbols_to_remove = '.,:;{}"?!&-'
        i = 0
        while i < len(text_tokens_without_stopwords):
            parsed = False
            if text_tokens_without_stopwords[i] in symbols_to_remove:
                i += 1
                continue
            # hashtag
            if text_tokens_without_stopwords[i][0] == '#':
                hashtag = self.parse_hashtags(text_tokens_without_stopwords[i])
                after_parse.extend(hashtag)
                parsed = True
            # taging
            if text_tokens_without_stopwords[i][0] == '@':
                tag = self.parse_tagging(text_tokens_without_stopwords[i])
                after_parse.extend(tag)
                parsed = True
            # url
            if 'http' in text_tokens_without_stopwords[i]:
                url = self.parse_url(text_tokens_without_stopwords[i], text_tokens)
                after_parse.extend(url)
                parsed = True
            # percent
            last_token = len(text_tokens_without_stopwords) - 2
            if ('%' in text_tokens_without_stopwords[i]) or ((i < last_token) and (
                    text_tokens_without_stopwords[i + 1] == 'percent' or text_tokens_without_stopwords[
                i + 1] == 'percentage')):
                percentage = self.parse_percentages(text_tokens_without_stopwords[i])
                after_parse.append(percentage)
                parsed = True
            # numbers
            if text_tokens_without_stopwords[i].replace(',', '').replace('.', '', 1).isdigit():
                if '.' in text_tokens_without_stopwords[i]:
                    curr_num = float(text_tokens_without_stopwords[i].replace(',', ''))
                else:
                    curr_num = int(text_tokens_without_stopwords[i].replace(',', ''))

                number = self.parse_numbers(curr_num, text_tokens_without_stopwords[i + 1])
                after_parse.append(number)
                parsed = True
            # names and entities
            if text_tokens_without_stopwords[i][0].isupper():
                tup = self.parse_names_and_entities(text_tokens_without_stopwords[i:])
                after_parse.extend(tup[0])
                i += tup[1]-1
                parsed = True

            if parsed is False:
                after_parse.append(text_tokens_without_stopwords[i])

            i += 1

        return after_parse




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
        if quote_url is None and quote_text is None:
            text_to_tokenize = full_text + ' ' + url
        # if quote_url is None and quote_text is not None:
        #     text_to_tokenize = full_text + ' ' + url + ' ' + ' ' + quote_text
        #
        # if quote_url is not None and quote_text is None:
        #     text_to_tokenize = full_text + ' ' + url + ' ' + ' ' + quote_text + ' ' + quote_url
        else:
            text_to_tokenize = full_text + ' ' + url + ' ' + ' ' + quote_text + ' ' + quote_url

        tokenized_text = self.parse_sentence(text_to_tokenize)

        doc_length = len(tokenized_text)  # after text operations.

        for term in tokenized_text:
            if term not in term_dict.keys():
                term_dict[term] = 1
            else:
                term_dict[term] += 1

        # print(tokenized_text)

        document = Document(tweet_id, tweet_date, full_text, url, indices, retweet_text, retweet_url, retweet_indices,
                            quote_text,
                            quote_url, quote_indices, retweet_quote_text, retweet_quote_url, retweet_quote_indices,
                            term_dict, doc_length)

        return document

    def parse_hashtags(self, token):
        hashtag_lst = []
        hashtag = token.replace('#', '')
        if hashtag.find('_') != -1:
            hashtag_lst = [s.lower() for s in hashtag.split('_')]
            merge_words = hashtag.replace('_', '')
            hashtag_lst.append('#' + merge_words.lower())

        elif any(x.isupper() for x in hashtag):
            condition = False
            for i in range(len(token) - 1):
                if token[i].isupper() and token[i + 1].isupper():
                    condition = True
                    break
            if condition:
                hashtag_lst = [s.lower() for s in re.findall('|[A-Z]+|[a-z]+|', token)]
            else:
                hashtag_lst = [s.lower() for s in re.findall('|[A-Z]+[a-z]*|[a-z]+|', token)]
            while '' in hashtag_lst: hashtag_lst.remove('')
            hashtag_lst.append('#' + hashtag.lower())
        else:
            hashtag_lst.append(hashtag)
        return hashtag_lst

    def parse_url(self, token, text_tokens):

        url_parts = re.split('{|}|://|/|:|=|"|":"', token)

        # index_of_dot = url_parts[1].find()
        for i in range(len(url_parts)):
            if 'www' in url_parts[i]:
                sub_url1 = url_parts[i][:3]
                sub_url2 = url_parts[i][4:]
                url_parts.pop(i)
                url_parts.insert(i, sub_url1)
                url_parts.insert(i+1, sub_url2)

        # print("im here:")
        # for i in url_parts:
        #     print(i)

        for i in range(len(url_parts)):
            if url_parts[i] != '':
                if url_parts[i][0] == '?':
                    word = url_parts[i][1:]
                    url_parts[i] = word

        # print(url_parts)
        return url_parts

    def parse_tagging(self, token):
        tag_lst = [token, token[1:]]
        return tag_lst

    def parse_percentages(self, token):

        token.replace('%', '', 1)
        return token + '%'

    def parse_numbers(self, number, str_to_check):
        num = ''
        if number < 1000:
            if str_to_check == "Thousand" or str_to_check == "thousand":
                num = str(number) + 'K'
            elif str_to_check == "Million" or str_to_check == "million":
                num = str(number) + 'M'
            elif str_to_check == "Billion" or str_to_check == "billion":
                num = str(number) + 'B'
            elif (str_to_check.replace('/', '').isdigit()) & ('/' in str_to_check):
                num = str(number) + " " + str_to_check
            else:
                num = str(number)

        elif 1000 <= number < 1000000:
            if str_to_check == "Million":
                curr_num = math.floor((number / 1000) * 10 ** 3) / 10 ** 3
                num = str(curr_num) + 'B'
            else:
                curr_num = math.floor((number / 1000) * 10 ** 3) / 10 ** 3
                num = str(curr_num) + 'K'
        elif 1000000 <= number < 1000000000:
            curr_num = math.floor((number / 1000000) * 10 ** 3) / 10 ** 3
            num = str(curr_num) + 'M'
        elif number >= 1000000000:
            curr_num = math.floor((number / 1000000000) * 10 ** 3) / 10 ** 3
            num = str(curr_num) + 'B'

        if num[-3:-1] == '.0':
            num = num[0:-3] + num[-1]
        return num

    def parse_names_and_entities(self, text):
        # text.replace('-', ' ')
        names_lst = []
        curr_name = ''
        for i in range(len(text)):
            if text[i][0].isupper():
                # for first word ignore space
                if curr_name == '':
                    curr_name += text[i]
                    names_lst.append(curr_name)
                else:
                    curr_name += ' ' + text[i]
                    names_lst.append(text[i])
                    names_lst.append(curr_name)
            else:
                return names_lst, i


# text1 = '#virusIsBad #infection_blabla #animals \n\nhttps://t.co/NrBpYOp0dR'
# text2 = 'https://www.instagram.com/p/CD7fAPWs3WM/?igshid=o9kf0ugp1l8x'
# text3 = 'this is @Ronen and @Bar'
# text4 = '6% 106 percent 10.6 percentage'
# # text5 = '1000 Million 204 14.7 123,470.11 1.2 Million 10,123 1010.56 10,123,000 55 Million 10123000000 10,123,000,000 55 Billion '
# text6 = 'Alexandria Ocasio-Cortez is Doctor Cortez'
# parse1 = Parse()
# # # parse1.parse_hashtags(text1)
# # parse1.parse_url(text2)
# # parse1.parse_tagging(text3)
# # parse1.parse_precentages(text4)
# # parse1.parse_numbers(text5)
# parse1.parse_names_and_entities(text6)
