import argparse
import urllib.parse
import json
import os
import oauth2

class TwitterData:
    def parse_config(self):
        config = {}
        # from file args
        if os.path.exists('config.json'):
            with open('config.json') as f:
                config.update(json.load(f))
        else:
            # may be from command line
            parser = argparse.ArgumentParser()

            parser.add_argument('-ck', '--consumer_key', default=None, help='Your developper `Consumer Key`')
            parser.add_argument('-cs', '--consumer_secret', default=None, help='Your developper `Consumer Secret`')
            parser.add_argument('-at', '--access_token', default=None, help='A client `Access Token`')
            parser.add_argument('-ats', '--access_token_secret', default=None, help='A client `Access Token Secret`')

            args_ = parser.parse_args()
            def val(key):
                return config.get(key)\
                    or getattr(args_, key)\
                    or raw_input('Your developper `%s`: ' % key)
            config.update({
                'consumer_key': val('consumer_key'),
                'consumer_secret': val('consumer_secret'),
                'access_token': val('access_token'),
                'access_token_secret': val('access_token_secret'),
            })
        # should have something now
        return config
    #end

    def oauth_req(self, url, http_method="GET", post_body=None,
                  http_headers=None):
        config = self.parse_config()
        consumer = oauth2.Consumer(key=config.get('consumer_key'), secret=config.get('consumer_secret'))
        token = oauth2.Token(key=config.get('access_token'), secret=config.get('access_token_secret'))
        client = oauth2.Client(consumer, token)

        resp, content = client.request(
            url,
            method=http_method,
            body=post_body or '',
            headers=http_headers
        )
        return content
    #end

    #start getTwitterData
    def getData(self, keyword, params = {}):
        maxTweets = 50
        url = 'https://api.twitter.com/1.1/search/tweets.json?'
        data = {'q': keyword, 'lang': 'en', 'result_type': 'recent', 'count': maxTweets, 'include_entities': 0}

        #Add if additional params are passed
        if params:
            for key, value in params.iteritems():
                data[key] = value

        url += urllib.parse.urlencode(data)

        response = self.oauth_req(url)
        jsonData = json.loads(response)
        tweets = []
        if 'errors' in jsonData:
            print ("API Error")
            print (jsonData['errors'])
        else:
            for item in jsonData['statuses']:
                tweets.append(item['text'])
        return tweets
    #end
#end class

## Usage
## =====




td = TwitterData()
l= (td.getData('barca'))
print (l)
