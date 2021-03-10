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

class CollectTweets:
    """Collect replies via twitter api v2."""

    def __init__(self, datapath, outputPath, token, tweet_fields, query, until_id):
        '''define the main path'''
        self.datapath = datapath# input path
        self.outputPath = outputPath# output path
        #self.handlesFile = handlesFile
        self.bearer_token = token
        self.tweet_fields = tweet_fields
        self.query = query
        self.until_id = until_id

    

    #search all allows 500 posts maximum
    def search_twitter(self):
        """Define search twitter function."""
        #curl "https://api.twitter.com/2/tweets/search/all?query=from%3Atwitterdev&max_results=500&start_time=2020-01-01T00%3A00%3A00Z&end_time=2020-03-31T11%3A59%3A59Z"

        headers = {"Authorization": "Bearer {}".format(self.bearer_token)}

        url = "https://api.twitter.com/2/tweets/search/all?query={}&{}&max_results=500&until_id={}".format(
            self.query, self.tweet_fields, self.until_id)
        response = requests.request("GET", url, headers=headers)

        print(response.status_code)

        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json()



    def get_tweets(self):

        search_result = self.search_twitter()

        file_exists = os.path.isfile(self.outputPath + 'tweets_test.csv')

        if not file_exists:
            f = open(self.outputPath + 'tweets_test.csv', 'a', encoding='utf-8-sig')
            writer_top = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            writer_top.writerow(["text"] + ["author_id"] + ["created_at"] + ["conversation_id"] + ["tweet_id"] + ["retweet_count"] + ['reply_count'] + ['like_count'] + ['quote_count'] + ['in_reply_to_user_id'] + ["referenced_tweets_type"] + ["reference_tweet_id"])
            f.close()

        # query user profile for each handle
        if file_exists:
            f = open(self.outputPath + 'tweets_test.csv', 'a', encoding='utf-8-sig')
            writer_top = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)

            for tweet in search_result['data']:
                #print(i['conversation_id'])
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



class Loop_files:
    def __init__(self, datapath, outputPath, token, tweet_fields, handlesFile):
        '''define the main path'''
        self.inputP = datapath# input path
        self.outputP = outputPath# output path
        self.handlesFile = handlesFile
        self.bearer_token = token
        self.tweet_fields = tweet_fields
        #self.query = query
        # self.until_id = until_id

    def read_handles(self, handlesFile):
        """Read handle files"""

        handles = pd.read_csv(outputP + self.handlesFile)
        return handles


    def search_twitter_recent(self, bearer_token, query, tweet_fields):
        """Define search twitter function."""
        #curl "https://api.twitter.com/2/tweets/search/all?query=from%3Atwitterdev&max_results=500&start_time=2020-01-01T00%3A00%3A00Z&end_time=2020-03-31T11%3A59%3A59Z"

        headers = {"Authorization": "Bearer {}".format(self. bearer_token)}

        url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}&max_results=10".format(query, self.tweet_fields)
        response = requests.request("GET", url, headers=headers)

        print(response.status_code)

        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json()


    def big_loop(self):
        handles = self.read_handles(self.handlesFile)

        for handle, status in zip(handles['screen_name'], handles['statuses_count']):
            # get handle name and pass it to query
            query = 'from:{}'.format(handle)

            #define how many loops we need in order to collect all the tweets of an account
            loop_num = (status//500) + 1 

            #get the most recent 10 tweets of an account
            search_result = self.search_twitter_recent(self.bearer_token, query, self.tweet_fields)
            #You want to get the most recent post id as the until id
            until_id = search_result['data'][1]['id']
            # if handle=='eu_eeas':
            #     until_id = 707221617353617000

            # else:
            #     until_id = search_result['data'][1]['id']

            # here you can manually reset the id
            print(query, loop_num, until_id)
            time.sleep(30) #check rate limit to adjust this
            #https://developer.twitter.com/en/docs/twitter-api/rate-limits#v2-limits 
            

            # loop everything
        
            for i in range(1, loop_num + 1):
                try:
                    # collect tweets using query, for each loop, we get 500 tweets
                    c = CollectTweets(self.inputP, self.outputP, self.bearer_token, self.tweet_fields, query, until_id)
                    #search_result = c.search_twitter()
                    search_result = c.get_tweets()  #store result
                    print('search id:', search_result['data'][-1]['id'])

                    #set the new until_id as the last one on the list, next loop will continue up to this id
                    new_until_id = search_result['data'][-1]['id']
                    until_id = new_until_id

                    time.sleep(30)#sleep 10s

                except Exception:
                    time.sleep(60)
                # if time.time() > timeout:
                #     time.sleep(20)
                #     timeout = time.time() + 60*2
               


evn_path = '/disk/data/share/s1690903/collect_tweets/environment/'
env = load_experiment(evn_path + 'env.yaml')


inputP = '/disk/data/share/s1690903/collect_tweets/data/'
outputP = '/disk/data/share/s1690903/collect_tweets/data/tweets/'
handles = 'handle_list_1.csv'
bearer_token = env['twitter_api']['bearer_token']
tweet_fields = "tweet.fields=text,author_id,created_at,conversation_id,in_reply_to_user_id,referenced_tweets,public_metrics"
handlesFile = 'handle_list_1.csv_profile.csv'


lf = Loop_files(datapath=inputP, outputPath=outputP, token=bearer_token, tweet_fields=tweet_fields, handlesFile=handlesFile)

lf.big_loop()

#Exception: (429, '{"title":"Too Many Requests","type":"about:blank","status":429,"detail":"Too Many Requests"}')



#print(json.dumps(json_response, indent=4, sort_keys=True))















