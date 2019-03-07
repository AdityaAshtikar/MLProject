#!/usr/bin/env python
# coding: utf-8

# In[3]:

from clint.textui import colored
import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 
  
class TwitterClient(object): 
    ''' 
    Generic Twitter Class for sentiment analysis. 
    '''
    def __init__(self): 
        ''' 
        Class constructor or initialization method. 
        '''
        # keys and tokens from the Twitter Dev Console 
        consumer_key = 'KurKqm7zDgQAOGe20d6C477Vn'
        consumer_secret = 'eaEmpDVncnoMWkjQDVu3fUsD9VRyf3UqRZTx7eMko70ZEndXG7'
        access_token = '1067804649938272256-0TWU4H5UBetjinQpWDrOxE8bQXMYmn'
        access_token_secret = 'PxRrqHe8ugkwZKV9r4xN8JjsCu9KWftM0sM2QGMafq17V'
  
        # attempt authentication 
        try: 
            # create OAuthHandler object 
            self.auth = OAuthHandler(consumer_key, consumer_secret) 
            # set access token and secret 
            self.auth.set_access_token(access_token, access_token_secret) 
            # create tweepy API object to fetch tweets 
            self.api = tweepy.API(self.auth) 
        except: 
            print("Error: Authentication Failed") 
  
    def clean_tweet(self, tweet): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])  |(\w+:\/\/\S+)", " ", tweet).split()) 
  
    def get_tweet_sentiment(self, tweet): 
        ''' 
        Utility function to classify sentiment of passed tweet 
        using textblob's sentiment method 
        '''
        # create TextBlob object of passed tweet text 
        # print(tweet)
        analysis = TextBlob(self.clean_tweet(tweet)) 
        # set sentiment 
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'
  
    def get_tweets(self, query, count = 10): 
        ''' 
        Main function to fetch tweets and parse them. 
        '''
        # empty list to store parsed tweets 
        tweets = [] 
  
        try: 
            # call twitter api to fetch tweets 
            fetched_tweets = self.api.search(q = query, count = count) 
  
            # parsing tweets one by one 
            for tweet in fetched_tweets: 
                # empty dictionary to store required params of a tweet 
                parsed_tweet = {} 
  
                # saving text of tweet 
                parsed_tweet['text'] = tweet.text 
                # saving sentiment of tweet 
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 
  
                # appending parsed tweet to tweets list 
                if tweet.retweet_count > 0: 
                    # if tweet has retweets, ensure that it is appended only once 
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet) 
  
            # return parsed tweets 
            return tweets 
  
        except tweepy.TweepError as e: 
            # print error (if any) 
            print("Error : " + str(e)) 
  
def main(): 
    # creating object of TwitterClient Class 
    api = TwitterClient() 
    # calling function to get tweets 
    print("Enter query to search")
    query = input()
    print("\n\n");
    tweets = api.get_tweets(query, count = 10) 
    # print(tweets)
    tcount = 1;
    for tweet in tweets:
        print("----------------------------------------------------------");
        print("\n{}.) " .format(tcount))
        print("Text: {}\n". format(tweet['text']))
        tcount+=1
        print("\nSentiment: {}\n". format(tweet['sentiment']))
        print("----------------------------------------------------------");
    print("Length of tweets: {}" . format(len(tweets)))
  
    # picking positive tweets from tweets 
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
    p=(100*len(ptweets)/len(tweets))
    # picking negative tweets from tweets 
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    n=(100*len(ntweets)/len(tweets))

    nu_tweets = (len(tweets) - len(ntweets) - len(ptweets))
    # percentage of positive tweets 
    if (len(ptweets) > len(ntweets) and len(ptweets) > nu_tweets):
        print(colored.green("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets))))
    else:  
        print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
    # percentage of negative tweets 
    if(len(ntweets) > len(ptweets) and len(ntweets) > nu_tweets):
        print(colored.red("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets))))
    else:
        print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
    # percentage of neutral tweets
    if(nu_tweets > len(ptweets) and nu_tweets > len(ntweets)):
        print(colored.yellow("Neutral tweets percentage: {} %".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets))))
    else:
        print("Neutral tweets percentage: {} %".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)))
  
    # printing first 5 positive tweets 
    print("\n\nTop 10 Positive tweets:")
    for tweet in ptweets[:10]: 
        print(colored.green(tweet['text']))
  
    # printing first 5 negative tweets 
    print("\n\nTop 10 Negative tweets:") 
    for tweet in ntweets[:10]: 
        print(colored.red(tweet['text']))
  
if __name__ == "__main__": 
   
    main()