import requests
import json
from ruamel import yaml
import gc
import csv
import os
import time
import pandas as pd
import time


def load_experiment(path_to_experiment):
    """load experiment"""
    data = yaml.safe_load(open(path_to_experiment))
    return data



class CollectReplies:
    def __init__(self, datapath, outputPath, token, tweet_fields, cidFile, outputFile):
        '''define the main path'''
        self.datapath = datapath# input path
        self.outputPath = outputPath# output path
        self.cidFile = cidFile
        self.bearer_token = token
        self.tweet_fields = tweet_fields
        self.outputFile = outputFile
        #self.query = query

    def read_conversation_id(self):

        conversation_id = pd.read_csv(self.outputPath + cidFile)
        return conversation_id
       

    def search_twitter(self, query):
        """Search replies according to conversation_id."""
        #curl "https://api.twitter.com/2/tweets/search/all?query=from%3Atwitterdev&max_results=500&start_time=2020-01-01T00%3A00%3A00Z&end_time=2020-03-31T11%3A59%3A59Z"

        headers = {"Authorization": "Bearer {}".format(self.bearer_token)}

        url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}&max_results=100".format(query, self.tweet_fields) #get the most recent 500 replies
        response = requests.request("GET", url, headers=headers)

        #print(response.status_code) 

        if response.status_code != 200:
            #raise Exception(response.status_code, response.text)
            time.sleep(120)

        return response.json()


    def get_tweets(self, query):
        """Get replies"""

        search_result = self.search_twitter(query)

        file_exists = os.path.isfile(self.outputPath + self.outputFile)

        if not file_exists:
            f = open(self.outputPath + self.outputFile, 'a', encoding='utf-8-sig')
            writer_top = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            writer_top.writerow(["text"] + ["author_id"] + ["created_at"] + ["conversation_id"] + ["tweet_id"] + ["retweet_count"] + ['reply_count'] + ['like_count'] + ['quote_count'] + ['in_reply_to_user_id'] + ["referenced_tweets_type"] + ["reference_tweet_id"])
            f.close()

        # query user profile for each handle
        if file_exists:
            f = open(self.outputPath + self.outputFile, 'a', encoding='utf-8-sig')
            writer_top = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)


            if 'data' in search_result.keys():
                print('data exist')
                for tweet in search_result['data']:

                    if 'in_reply_to_user_id' in tweet.keys():
                        if 'referenced_tweets' in tweet.keys():
                            content = [[tweet['text'], tweet['author_id'], tweet['created_at'], tweet['conversation_id'], tweet['id'], tweet['public_metrics']['retweet_count'], tweet['public_metrics']['reply_count'], tweet['public_metrics']['like_count'], tweet['public_metrics']['quote_count'], tweet['in_reply_to_user_id'],  tweet['referenced_tweets'][0]['type'], tweet['referenced_tweets'][0]['id']]]
                        else:
                            content = [[tweet['text'], tweet['author_id'], tweet['created_at'], tweet['conversation_id'], tweet['id'], tweet['public_metrics']['retweet_count'], tweet['public_metrics']['reply_count'], tweet['public_metrics']['like_count'], tweet['public_metrics']['quote_count'], tweet['in_reply_to_user_id'], None, None]]

                    else:
                        content = [[tweet['text'], tweet['author_id'], tweet['created_at'], tweet['conversation_id'], tweet['id'], tweet['public_metrics']['retweet_count'], tweet['public_metrics']['reply_count'], tweet['public_metrics']['like_count'], tweet['public_metrics']['quote_count'], None, None, None]]

                    writer_top.writerows(content)

            f.close()
            gc.collect()

            return search_result


    def loop_file(self):
        """Loop conversation id according to tweet file """

        # conversation_id = self.read_conversation_id()
        # for cid in conversation_id['conversation_id'][470::]:

        #   query = "conversation_id:{}".format(cid)
        #   search_result = self.get_tweets(query)

        #   print('conversation id:', query)
        #   time.sleep(2)
        query = 'conversation_id:1345038502581460000'
        search_result = self.search_twitter(query)
    

        return search_result




evn_path = '/disk/data/share/s1690903/collect_tweets/environment/'
env = load_experiment(evn_path + 'env.yaml')


inputP = '/disk/data/share/s1690903/collect_tweets/data/'
outputP = '/disk/data/share/s1690903/collect_tweets/data/tweets/'
cidFile = 'tweets_test.csv'
bearer_token = env['twitter_api']['bearer_token']
tweet_fields = "tweet.fields=text,author_id,created_at,conversation_id,in_reply_to_user_id,referenced_tweets,public_metrics"
outputFile = 'tweet_replies.csv'

c = CollectReplies(datapath=inputP, outputPath=outputP, token=bearer_token, tweet_fields=tweet_fields, cidFile=cidFile, outputFile=outputFile)

result = c.loop_file()


# {'public_metrics': {'retweet_count': 0,
#     'reply_count': 0,
#     'like_count': 29,
#     'quote_count': 0},
#    'in_reply_to_user_id': '1226290896817225728',
#    'id': '1368979627574763524',
#    'author_id': '637018221',
#    'referenced_tweets': [{'type': 'replied_to', 'id': '1368979165085634573'}],
#    'created_at': '2021-03-08T17:39:12.000Z',
#    'text': '@CAPYBARA_MAN Most graceful thing in the animal kingdom',
#    'conversation_id': '1368979165085634573'}


# you can search converstion id
# query = 'conversation_id:1368979165085634573'
# search_result = search_twitter(query, tweet_fields, BEARER_TOKEN)

#search reply
#query = "from:IUSSP -is:reply"