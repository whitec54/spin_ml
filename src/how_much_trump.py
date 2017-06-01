## Very simple script that prints an RSS feed from r/THE_DONALD\
## and counts how many times his name is mentioned
## Created to get familiar with the idea of scanning an rss feed
## Can be made dynamic to work with any subreddit/site
## I chose reddit because...I like reddit

import feedparser

# Entry point
def __main__():
	rss_feed = get_rss_feed()
	num_times = count_and_print_feed(rss_feed)
	print_results(num_times)

# Gathers URL prints relavant information about the subreddit
def get_rss_feed():
	d = feedparser.parse('https://www.reddit.com/r/The_Donald/.rss')

	print(d['feed']['title'])
	print(d['feed']['link'])
	print(d.feed.subtitle)
	print(len(d['entries']))
	print( "\n\n\n")

	return d

# Prints each element in the RSS feed
# Chose some buzzwords that would refer to POTUS
# Counted how many times he was referred to in the hottest 25 posts
def count_and_print_feed(rss_feed):
	buzz_count = 0
	trump_buzzwords = ['Donald Trump', 'President Trump','POTUS', "Trump", 'Donald', 'President of the United States']
	for post in rss_feed.entries:
		print(post.title + "\n" + "Link: " + post.link)
		if any(x in post.title for x in trump_buzzwords):
			buzz_count+=1
		
		print("\n")
	return buzz_count

# Prints number of times Donald's name was mentioned
def print_results(num_times):
		print("Right now Donald Trump is mentioned {} times in the 25 hottest posts on r/The_Donald.".format(num_times))

__main__()