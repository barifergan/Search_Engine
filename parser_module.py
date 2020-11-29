from nltk import RegexpTokenizer, TweetTokenizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from document import Document
import re
import math


class Parse:

    def __init__(self):
        self.stop_words = stopwords.words('english')

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
        # TODO: decide what exactly to enter into the text to parse, so we get the most relevant information
        # if quote_url is None and quote_text is None:
        #     text_to_tokenize = full_text + ' ' + url
        # else:
        #     text_to_tokenize = full_text + ' ' + url + ' ' + ' ' + quote_text + ' ' + quote_url

        # url to parse:
        if url == '{}' or url is None:
            if retweet_url == '{}' or retweet_url is None:
                if quote_url is None:
                    if retweet_quote_url is None:
                        url_to_token = full_text[full_text.find('http'):]
                    else:
                        url_to_token = retweet_quote_url[retweet_quote_url.find('":"') + 3:]
                else:
                    url_to_token = quote_url[quote_url.find('":"') + 3:]
            elif quote_url is not None:
                url_to_token = retweet_url[retweet_url.find('":"') + 3:] + ' ' + quote_url[quote_url.find('":"') + 3:]
            elif retweet_quote_url is not None:
                url_to_token = retweet_url[retweet_url.find('":"') + 3:] + ' ' + retweet_quote_url[
                                                                                 retweet_quote_url.find('":"') + 3:]
            else:
                url_to_token = retweet_url[retweet_url.find('":"') + 3:]
        else:
            url_to_token = url[url.find('":"') + 3:]

        if 'http' in full_text:
            text_to_tokenize = full_text[0:full_text.find('http')]
        else:
            text_to_tokenize = full_text

        tokenized_full_text = self.parse_sentence(text_to_tokenize)

        if quote_text is None:
            text_to_tokenize = url_to_token
        else:
            text_to_tokenize = quote_text + ' ' + url_to_token

        tokenized_rest = self.parse_sentence(text_to_tokenize)

        tokenized_text = tokenized_full_text + tokenized_rest

        doc_length = len(tokenized_text)  # after text operations.
        for term in tokenized_text:  # dict of all parsed tokens
            if term not in term_dict.keys():
                term_dict[term] = 1
            else:
                term_dict[term] += 1

        document = Document(tweet_id, tweet_date, full_text, url, indices, retweet_text, retweet_url, retweet_indices,
                            quote_text,
                            quote_url, quote_indices, retweet_quote_text, retweet_quote_url, retweet_quote_indices,
                            term_dict, doc_length)

        return document

    def parse_sentence(self, text):
        """
        This function tokenize, remove stop words and apply lower case for every word within the text
        :param text:
        :return:
        """
        # space_tokenizer = RegexpTokenizer("\s+", gaps=True)
        # text_tokens = space_tokenizer.tokenize(re.sub(r'[^\x00-\x7f]', r' ', text))
        after_parse = []
        # tokenizer:
        tweet_tokenizer = TweetTokenizer()
        text_tokens = tweet_tokenizer.tokenize(re.sub(r'[^\x00-\x7f]', r' ', text))

        symbols = '.,...,:;{}()[]"?!&-_/\''
        text_tokens_without_stopwords = [w for w in text_tokens if
                                         w.lower() not in self.stop_words and w not in symbols]
        all_upper = True
        j = 0

        while j < len(text_tokens_without_stopwords):
            if not text_tokens_without_stopwords[j].isupper():
                all_upper = False
            if '-' in text_tokens_without_stopwords[j] and 'http' not in text_tokens_without_stopwords[j]:
                if text_tokens_without_stopwords[j][0] == '-':
                    j += 1
                    continue
                temp = text_tokens_without_stopwords[j].split('-')
                text_tokens_without_stopwords.remove(text_tokens_without_stopwords[j])
                text_tokens_without_stopwords.insert(j, temp[0])
                if temp[1] != '':
                    text_tokens_without_stopwords.insert(j + 1, temp[1])
                j += 1

            j += 1

        i = 0
        while i < len(text_tokens_without_stopwords):
            parsed = False  # if parsed according one of the roles

            if all_upper:
                after_parse.append(text_tokens_without_stopwords[i])
                parsed = True

            # if text_tokens_without_stopwords[i].upper() == 'COVID' or text_tokens_without_stopwords[
            #     i].upper() == 'COVID19':
            #     after_parse.append('COVID19')

            # hashtag
            if text_tokens_without_stopwords[i][0] == '#':
                hashtag = self.parse_hashtags(text_tokens_without_stopwords[i])
                after_parse.extend(hashtag)
                parsed = True

            # tagging
            if text_tokens_without_stopwords[i][0] == '@':
                tag = self.parse_tagging(text_tokens_without_stopwords[i])
                after_parse.extend(tag)
                parsed = True

            # url
            if 'http' in text_tokens_without_stopwords[i]:
                url = self.parse_url(text_tokens_without_stopwords[i])
                after_parse.extend(url)
                parsed = True

            # percent
            last_token = len(text_tokens_without_stopwords) - 2
            if (i < last_token) and (text_tokens_without_stopwords[i + 1] == 'percent' or text_tokens_without_stopwords[
                i + 1] == 'percentage' or text_tokens_without_stopwords[i + 1] == '%'):
                percentage = self.parse_percentages(text_tokens_without_stopwords[i])
                after_parse.append(percentage)
                parsed = True

            # numbers
            if text_tokens_without_stopwords[i].replace(',', '').replace('.', '', 1).isdigit():
                if '.' in text_tokens_without_stopwords[i]:
                    curr_num = float(text_tokens_without_stopwords[i].replace(',', ''))
                else:
                    curr_num = int(text_tokens_without_stopwords[i].replace(',', ''))

                if i == len(text_tokens_without_stopwords) - 1:  # if this is the last word, send only the current word
                    number = self.parse_numbers(curr_num, '')
                else:
                    number = self.parse_numbers(curr_num, text_tokens_without_stopwords[i + 1])

                after_parse.append(number)
                parsed = True

            # names and entities
            if text_tokens_without_stopwords[i][0].isupper():
                names_and_entities = self.parse_names_and_entities(text_tokens_without_stopwords[i:])
                after_parse.append(names_and_entities[0])
                i += names_and_entities[1] - 1
                parsed = True

            if parsed is False:
                after_parse.append(text_tokens_without_stopwords[i])

            i += 1

        return after_parse

    # hashtags
    def parse_hashtags(self, token):
        hashtag_lst = []
        hashtag = token.replace('#', '')
        if hashtag.find('_') != -1:
            hashtag_lst = [s.lower() for s in hashtag.split('_')]
            merge_words = hashtag.replace('_', '')
            hashtag_lst.append('#' + merge_words.lower())

        elif any(x.isupper() for x in hashtag):
            """
            This case handles uppercase letters
            :param two_capital_in_row: helps find amount_of_rows.
            :param amount_of_rows: indicates if seperation is by uppercase letters ==1: Yes, <1: No.
            :param low_or_up: resembles hashtag 'u': uppercase, 'l': lowercase.
            """
            two_capital_in_row = False
            amount_of_rows = 0
            low_or_up = ''
            for i in range(len(hashtag)):
                if hashtag[i].isupper():
                    low_or_up += 'u'
                    if i + 1 < len(hashtag) and hashtag[i + 1].isupper():
                        if not two_capital_in_row:
                            two_capital_in_row = True
                            amount_of_rows += 1
                else:
                    low_or_up += 'l'
                    two_capital_in_row = False

            if amount_of_rows > 1:
                hashtag_lst = [s.lower() for s in re.findall('|[A-Z]+|[a-z]+|', hashtag)]
                while '' in hashtag_lst: hashtag_lst.remove('')
            else:
                part_of_hashtag = ''
                for i in range(len(low_or_up)):
                    if low_or_up[i] == 'u':
                        if part_of_hashtag == '':
                            part_of_hashtag += hashtag[i]
                        elif part_of_hashtag[-1].islower():
                            hashtag_lst.append(part_of_hashtag.lower())
                            part_of_hashtag = hashtag[i]
                        else:
                            if i + 1 < len(low_or_up) and low_or_up[i + 1] == 'l':
                                hashtag_lst.append(part_of_hashtag.lower())
                                part_of_hashtag = hashtag[i]
                            elif i + 1 < len(low_or_up) and low_or_up[i + 1] == 'u':
                                part_of_hashtag += hashtag[i]
                            else:
                                # check if last char
                                part_of_hashtag += hashtag[i]
                                hashtag_lst.append(part_of_hashtag.lower())

                    else:
                        part_of_hashtag += hashtag[i]
                        # check if last char
                        if i == len(low_or_up) - 1:
                            hashtag_lst.append(part_of_hashtag.lower())

            hashtag_lst.append(token.lower())

        elif len(hashtag) != 0:
            hashtag_lst.append(hashtag)

        while '' in hashtag_lst: hashtag_lst.remove('')
        return hashtag_lst

    # url
    def parse_url(self, token):

        url_parts = re.split('/|{|}|://|:|=|"|-|[?]|#', token)

        for i in range(len(url_parts)):
            if 'www' in url_parts[i]:
                sub_url1 = url_parts[i][:3]
                sub_url2 = url_parts[i][4:]
                url_parts.remove(url_parts[i])
                url_parts.insert(i, sub_url1)
                url_parts.insert(i + 1, sub_url2)

        # for i in range(len(url_parts)):
        #     if url_parts[i] != '':
        # if url_parts[i][0] == '?':
        #     word = url_parts[i][1:]
        #     url_parts[i] = word

        while '' in url_parts: url_parts.remove('')
        return url_parts

    # tagging
    def parse_tagging(self, token):
        tag_lst = []

        if token[1:] != '':
            tag_lst = [token, token[1:]]  # TODO: decide if we want to save both tokens

        return tag_lst

    # percent
    def parse_percentages(self, token):

        token.replace('%', '', 1)
        return token + '%'

    # numbers
    def parse_numbers(self, number, next_word):
        num = ''
        if number < 1000:
            if next_word == "Thousand" or next_word == "thousand":
                num = str(number) + 'K'
            elif next_word == "Million" or next_word == "million":
                num = str(number) + 'M'
            elif next_word == "Billion" or next_word == "billion":
                num = str(number) + 'B'
            elif (next_word.replace('/', '').isdigit()) & ('/' in next_word):
                num = str(number) + " " + next_word
            else:
                num = str(number)

        elif 1000 <= number < 1000000:
            if next_word == "Million":
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

        if num[-3:-1] == '.0':  # reformat number
            num = num[0:-3] + num[-1]
        return num

    # names and entities
    def parse_names_and_entities(self, text):
        curr_name = ''
        for i in range(len(text)):
            if text[i] == '':
                print(text)
            if text[i][0].isupper():
                if curr_name == '':  # for first word ignore space
                    curr_name += text[i]
                else:
                    curr_name += ' ' + text[i]
            else:
                return curr_name, i
        return curr_name, len(text)

# text1 = '#virusIsBad #infection_blabla #animals \n\nhttps://t.co/NrBpYOp0dR'
# text2 = 'https://www.instagram.com/p/CD7fAPWs3WM/?igshid=o9kf0ugp1l8x'
# text3 = 'this is @Ronen and @Bar'
# text4 = '6% 106 percent 10.6 percentage'
# # text5 = '1000 Million 204 14.7 123,470.11 1.2 Million 10,123 1010.56 10,123,000 55 Million 10123000000 10,123,000,000 55 Billion '
# text6 = ['Alexandria', 'Ocasio-cortez', 'is', 'Doctor Cortez']
# parse1 = Parse()
# # # parse1.parse_hashtags(text1)
# # parse1.parse_url(text2)
# # parse1.parse_tagging(text3)
# # parse1.parse_precentages(text4)
# # parse1.parse_numbers(text5)
# parse1.parse_names_and_entities(text6)
