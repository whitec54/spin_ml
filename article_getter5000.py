import praw
import config

def get_submissions(query,subreddit,limit=3):
	return subreddit.search(query, syntax='lucene',limit=limit)

def make_query(site,topic):
	return 'site:'+site+'.com'+' '+topic

def get_subreddit(name):
	reddit = praw.Reddit(client_id=config.client_id,
                     client_secret=config.client_secret,
                     user_agent=config.user_agent)

	return reddit.subreddit(name)

def fetch_sources(topic, subreddit_name = 'all',
				  quantity = 1,sites = ['cnn','foxnews','msnbc','usatoday']):
	
	subreddit = get_subreddit(subreddit_name)
	res = []

	for site in sites:
		query = make_query(site,topic)
		submissions = get_submissions(query,subreddit,quantity)
		
		for submission in submissions:
			res.append({'site':site,'url':submission.url})

	return res


sources = fetch_sources('bernie sanders')

for source in sources:
	print(source['site'])
	print(source['url'])


