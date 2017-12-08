import tweepy
from tweepy import OAuthHandler
import sys

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
#print(status.translate(non_bmp_map))
 
consumer_key = 'JJFgGgN8neum0VTXsGO72F3Ex'
consumer_secret = 'MZCljH6ndfJm8N4rt0ZReqQg6bv70NPu16eU89uf08L2lLXosK'
access_token = '2611457064-J1nZTCizycFuFqrGsY7HFdtRAlx7HNvl2wzhidr'
access_secret = 'GraY5KHNJWCFpFxqrgko4xWCozoUvrQCRxAQy5VHtXzAO'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)
#replace='?'
search_results =api.search(q="demonetization",count=50)
str(search_results).encode('utf-8', 'ignore').decode('utf-8')
#sys.stdout=open("t.txt","w")


for status in search_results:#tweepy.Cursor(api.home_timeline).items(25):
    # Process a single status
    print(status.text.translate(non_bmp_map))


#sys.stdout.close()
