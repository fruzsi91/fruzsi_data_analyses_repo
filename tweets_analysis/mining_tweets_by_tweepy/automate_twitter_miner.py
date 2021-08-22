import tweepy
import pandas as pd
import datetime
import os.path
import shutil

class TwitterMiner:
    '''
    Generic Class for collecing data by tweepy
    '''
    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # authenticating twitter api credentials, keys and tokens from the Twitter Developer account
        consumer_key = 'oooyScjOhTQhbOtBJ9Ln76ppy'
        consumer_secret = '7KNZeRe4J5fxZVtH7NFhrhLQyBUD6o00HurMlAufhfrGyn8yIL'
        access_token = '1417086199550853127-0yAmIS7jLBarHn2lhWJ7jqPh1fnGzS'
        access_token_secret = '6dbu6qi7SnjvnDQfkiGoqkEm3UfpScPtaiAe7FxnW3bQT'

        # create OAuthHandler object
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        # set access token and secret
        self.auth.set_access_token(access_token, access_token_secret)
        # create tweepy API object to fetch tweets
        self.api = tweepy.API(self.auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)


    def get_tweets(self, count, search_terms, since_id, max_id):
        '''
        Utility function to fetch tweets
        '''
        # call twitter api to fetch tweets
        tweets = tweepy.Cursor(self.api.search, q=search_terms,
        lang = "en", since_id = since_id, max_id = max_id, tweet_mode='extended' ).items(count)

        #store fetching tweets and their attributes in a python list and return it
        tweets_list = [[tweet.id,
        tweet.full_text,
        tweet.created_at,
        tweet.retweet_count,
        tweet.favorite_count,
        tweet.user.id_str,
        [v for lst in tweet.entities['hashtags'] for k,v in lst.items() if 'text' in k ],   # fetch only hashtags from the tweet entities belonging to a tweet                                                                                      ,
        tweet.user.name,
        tweet.user.screen_name,
        tweet.user.location,
        tweet.user.description,
        tweet.user.created_at,
        tweet.user.followers_count,
        tweet.user.friends_count, # following
        tweet.user.favourites_count, #likes
        tweet.user.statuses_count, #tweets
        tweet.user.listed_count] for tweet in tweets ]

        return tweets_list

    def data_path(self, name):
    
        '''
        Main function to ensure automate fetching of tweets without any duplication
        '''
        #determine max_id and since_id to put them in the get_tweets() attrributes
        since_id = self.determe_since_id() if os.path.exists('since_id.txt') else None
        max_id = self.determe_max_id() if os.path.exists('max_id.txt') else None

        try:
            #call the get_tweets() function and store the return value in a variable
            tweets_list = self.get_tweets(count = count, search_terms = search_terms, since_id = since_id, max_id =max_id)
            #convert list to pandas DF
            tweets_df = pd.DataFrame(tweets_list)
            #calculate the number of records
            count_rows = str(tweets_df.shape[0])
            #determine the since_id and max_id for the next mining
            since_id = tweets_df[0].max()
            max_id = tweets_df[0].min()
            # if loop check if a section of unprocessed tweets is ended (max_id.txt not exists) or not. 
            # Great explaination about the role of max_id and since_id in twitter api is: https://stackoverflow.com/questions/6412188/what-exactly-does-since-id-and-max-id-mean-in-the-twitter-api
            if os.path.exists('max_id.txt'): # this condition runs to collect unprocessed/"fragment" tweets
                # call functions
                self.export_max_id(max_id = max_id)
                self.writeToCSV(name = name, data = tweets_df)
                self.log_data(name = name, count_rows = count_rows)

            else: 
                if os.path.exists('since_id.txt'):
                    # this condition runs by the first mining of a section
                    self.export_max_id(max_id = max_id)
                    # need to save since_id used in the next section
                    with open('new_since_id.txt', '+a') as new_since_id:
                        new_since_id.writelines("{0}\n".format(since_id))
                    #writing to csv
                    self.writeToCSV(name = name, data = tweets_df)
                    #log the data saving
                    self.log_data(name = name, count_rows =count_rows)
            
                else: # this condition runs at the firt time of running
                    with open('since_id.txt', '+a') as since_id_f:
                        since_id_f.writelines("{0}\n".format(since_id))                
                    #self.export_max_id(max_id = max_id)
                    self.writeToCSV(name = name, data = tweets_df)
                    self.log_data(name = name, count_rows =count_rows)                

        
        except KeyError: # this part runs when get_tweets() function shows a key error. It means a section is ended, must change since_id and no need max_id.txt.
            with open('new_since_id.txt', 'rb') as f2, open('since_id.txt', 'wb') as f1:
                shutil.copyfileobj(f2, f1)
            self.log_no_data(name = name)
            os.remove('new_since_id.txt')
            os.remove('max_id.txt')
            

    def determe_max_id(self):
        '''
        Main function calls this function to determine the actual value of max_id which is the value of max_id in get_tweets function
        '''
        with open('max_id.txt', 'r') as max_id_file:
            lines = max_id_file.read().splitlines()
            max_id = int(lines[-1]) - 1
        return max_id

    def determe_since_id(self):
        '''
        Main function calls this function to determine the actual value of since_id which is the value of since_id in get_tweets function
        '''
        with open('since_id.txt', 'r') as since_id_file:
            since_id = int(since_id_file.read())
        return since_id
    
    def export_max_id(self, max_id):
        '''
        Main function calls this function to store max_id when the program works within a session
        '''
        with open('max_id.txt', 'a') as max_id_f:
            max_id_f.writelines("{0}\n".format(max_id))

    def log_data(self, name, count_rows):
        '''
        Main function calls this function to create a log if it can collect data
        '''
        with open("%s.log" %name, '+a') as log_file: #check filename
            now = str(datetime.datetime.now())
            line = "---------------------------- \nlatest data ({0} rows) copied to the csv at {1}\n".format(count_rows, now)
            log_file.writelines(line)
    
    def log_no_data(self, name):
        '''
        Main function calls this function to create a log if it can not collect data 
        '''
        with open("%s.log" %name, '+a') as log_file: #filename!!!
            now = str(datetime.datetime.now()) 
            line = "---------------------------- \nKeyError 0 at {0}\n".format(now)
            log_file.writelines(line)
    
    def writeToCSV(self, name, data):
        with open("%s.csv" %name, 'a', newline = '\n', encoding = "utf-8") as file: #encoding argument not necessary in linux                                                                                       ename
            data.to_csv(file, mode='a', index=False, header=False, sep = ";")

    
if __name__ == "__main__":
        # creating object of TwitterClient Class
        api = TwitterMiner()
        # need to set the number of tweets you want to fetch during one running. More information about twitter api rate limits please visit to https://developer.twitter.com/en/docs/twitter-api/v1/rate-limits
        count = 20 
        #in this program the tweets-search based on keywords, need to use seach terms, 
        # by more than one keywords use "search_terms = ('#artificalintelligence OR artifical_intelligence OR #AI OR AI')" format 
        search_terms =('#artificalintelligence OR artifical_intelligence OR #AI OR AI')
        #define the name of the csv and log file globally
        api.data_path(name = 'artifical_intelligence')