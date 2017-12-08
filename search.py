import twitter
#Setting up Twitter API
api = twitter.api(
 consumer_key='JJFgGgN8neum0VTXsGO72F3Ex',
 consumer_secret='MZCljH6ndfJm8N4rt0ZReqQg6bv70NPu16eU89uf08L2lLXosK',
 access_token_key='2611457064-J1nZTCizycFuFqrGsY7HFdtRAlx7HNvl2wzhidr',
 access_token_secret='GraY5KHNJWCFpFxqrgko4xWCozoUvrQCRxAQy5VHtXzAO',
 )

search = api.GetSearch(term='adventure', lang='en', result_type='recent', count=10, max_id='')
for t in search:
 print (t.user.screen_name + ' (' + t.created_at + ')')
 #Add the .encode to force encoding
 print (t.text.encode('utf-8'))
 print ('')
