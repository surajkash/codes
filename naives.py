import re
import csv
import nltk
import tweepy
from tweepy import OAuthHandler
import sys

#start process_tweet
def processTweet(tweet):
    # process the tweets

    #Convert to lower case
    tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','AT_USER',tweet)
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')
    return tweet
#end

stopWords = []

#start replaceTwoOrMore
def replaceTwoOrMore(s):
    #look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)
#end

#start getStopWordList
def getStopWordList(stopWordListFileName):
    #read the stopwords file and build a list
    stopWords = []
    stopWords.append('AT_USER')
    stopWords.append('URL')

    fp = open(stopWordListFileName, 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        stopWords.append(word)
        line = fp.readline()
    fp.close()
    return stopWords
#end

#start getfeatureVector
def getFeatureVector(tweet):
    featureVector = []
    #split tweet into words
    words = tweet.split()
    for w in words:
        #replace two or more with two occurrences
        w = replaceTwoOrMore(w)
        #strip punctuation
        w = w.strip('\'"?,.')
        #check if the word stats with an alphabet
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
        #ignore if it is a stop word
        if(w in stopWords or val is None):
            continue
        else:
            featureVector.append(w.lower())
    return featureVector
#end




#start extract_features
def extract_features(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in featureList:
        features['contains(%s)' % word] = (word in tweet_words)
    return features
#end


inpTweets = csv.reader(open('min2.csv',encoding='latin1'), delimiter=',', quotechar='|')
stopWords = getStopWordList('stopwords.txt')
featureList = []

# Get tweet words
tweets = []
for row in inpTweets:
    sentiment = row[0]
    tweet = row[1]
    #print(row[1])
    processedTweet = processTweet(tweet)
    featureVector = getFeatureVector(processedTweet)
    featureList.extend(featureVector)
    tweets.append((featureVector, sentiment));
#end loop

# Remove featureList duplicates
featureList = list(set(featureList))

# Extract feature vector for all tweets in one shote
training_set = nltk.classify.util.apply_features(extract_features, tweets)
#train_set= nltk.classify.util.apply_features(extract_features, tweets[10000:])
#test_set = nltk.classify.util.apply_features(extract_features, tweets[:9000])

# Train the classifier
NBClassifier = nltk.NaiveBayesClassifier.train(training_set)

# Test the classifier
#testTweet = 'had loads of fun today...'
accuracy=nltk.classify.accuracy(NBClassifier, training_set)
print("Accuracy for naives bayes = " +str(accuracy))
NBClassifier.show_most_informative_features(10)

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
#print(status.translate(non_bmp_map))
 
consumer_key = 'JJFgGgN8neum0VTXsGO72F3Ex'
consumer_secret = 'MZCljH6ndfJm8N4rt0ZReqQg6bv70NPu16eU89uf08L2lLXosK'
access_token = '2611457064-J1nZTCizycFuFqrGsY7HFdtRAlx7HNvl2wzhidr'
access_secret = 'GraY5KHNJWCFpFxqrgko4xWCozoUvrQCRxAQy5VHtXzAO'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

#search_results =api.search(q="elclassico",rpp=100,page=2,lang="en")
query = 'ram mandir'
max_tweets = 100
search_results = [status for status in tweepy.Cursor(api.search, q=query, 
                    since="2017-5-20", 
                    until="2017-5-24",lang="en").items(max_tweets)]

p=0
neg=0
n=0
#csvFile = open('fifth.csv', 'a')
#Use csv Writer
#csvWriter = csv.writer(csvFile)
    

for testTweet in search_results:#tweepy.Cursor(api.home_timeline).items(25):
    # Process a single status
    #print(status.text.translate(non_bmp_map))
    #if testTweet.lang == "en":
        processedTestTweet = processTweet(testTweet.text.translate(non_bmp_map))
        print(processedTestTweet)
        result=NBClassifier.classify(extract_features(getFeatureVector(processedTestTweet)))
        print(result)
        if result=="positive":
            p=p+1
        if result=="negative":
            neg=neg+1
        if result=="neutral":
            n=n+1;
        ##csvWriter.writerow([testTweet.text.encode('utf-8')])
            
print("positive="+str(p))
print("negative="+str(neg))
print("neutral="+str(n))
#csvFile.close()
                                              
