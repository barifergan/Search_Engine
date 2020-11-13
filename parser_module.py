from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from document import Document
import re


class Parse:

    def __init__(self):
        self.stop_words = stopwords.words('english')

    def parse_sentence(self, text):
        """
        This function tokenize, remove stop words and apply lower case for every word within the text
        :param text:
        :return:
        """
        text_tokens = word_tokenize(text)
        text_tokens_without_stopwords = [w.lower() for w in text_tokens if w not in self.stop_words]
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
        retweet_text = doc_as_list[4]
        retweet_url = doc_as_list[5]
        quote_text = doc_as_list[6]
        quote_url = doc_as_list[7]
        term_dict = {}
        tokenized_text = self.parse_sentence(full_text)

        doc_length = len(tokenized_text)  # after text operations.

        for term in tokenized_text:
            if term not in term_dict.keys():
                term_dict[term] = 1
            else:
                term_dict[term] += 1

        document = Document(tweet_id, tweet_date, full_text, url, retweet_text, retweet_url, quote_text,
                            quote_url, term_dict, doc_length)
        return document

    def parse_hashtags(self, text):
        txt_list = text.split()
        hashtag_lst = []
        for word in txt_list:
            if word[0] == '#':
                hashtag = word.replace('#', '')
                if hashtag.find('_') != -1:
                    hashtag_lst = hashtag.split('_')
                    merge_words = hashtag.replace('_', '')
                    hashtag_lst.append('#'+merge_words)

                elif any(x.isupper() for x in hashtag):
                    pos = [i for i, e in enumerate(hashtag + 'A') if e.isupper()]
                    pos.insert(0, 0)
                    hashtag_lower = hashtag.lower()
                    hashtag_lst = [hashtag_lower[pos[j]:pos[j + 1]] for j in range(len(pos) - 1)]
                    hashtag_lst.append('#'+hashtag_lower)

                else:
                    hashtag_lst.append(hashtag)

        return hashtag_lst

    def parse_url(self, text):
        url_parts = re.split('://|/|:|=', text)

        # indices = [0, 4]
        # parts = [url_parts[1][indices[i]:indices[i + 1]] for i in range(len(indices) - 1)]
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










text1 = '#virusIsBad #infection_blabla #animals \n\nhttps://t.co/NrBpYOp0dR'
text2 = 'https://www.instagram.com/p/CD7fAPWs3WM/?igshid=o9kf0ugp1l8x'
parse1 = Parse()
# parse1.parse_hashtags(text1)
parse1.parse_url(text2)