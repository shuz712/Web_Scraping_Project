from reddit.items import RedditItem
import scrapy
from datetime import datetime
from bs4 import BeautifulSoup as soup
import re

class reddit_spider(scrapy.Spider):
	name = 'reddit_spider'
	allowed_urls = ['reddit.com']
	start_urls=['https://www.reddit.com/r/dataisbeautiful/',
	'https://www.reddit.com/r/MachineLearning/',
	'https://www.reddit.com/r/Frugal/',
	#'https://www.reddit.com/r/technology/',
	'https://www.reddit.com/r/soccer',
	'https://www.reddit.com/r/statistics/'
	#'https://www.reddit.com/r/todayilearned/'
	]

	def parse(self, response):
		news = response.xpath('//div[@onclick="click_thing(this)"]')
		next_button_url = response.xpath('//span[@class="next-button"]/a/@href').extract_first()
		for new in news:

			comment_url = new.xpath('.//li[@class="first"]/a/@href').extract_first()
			#rank = new.xpath('@data-rank').extract_first()
			title = new.xpath('.//p[@class ="title"]/a/text()').extract_first()
			source = new.xpath('.//span[@class = "domain"]/a/text()').extract_first()
			link = new.xpath('.//@data-url').extract_first()
			link = [link if 'http' in link else 'https://www.reddit.com'+link][0]
			date= new.xpath('.//time[@class = "live-timestamp"]/@datetime').extract_first()[:10]
			time = new.xpath('.//time[@class = "live-timestamp"]/@datetime').extract_first()[11:19]
			topic_vote = new.xpath('.//div[@class = "midcol unvoted"]/div[@class ="score unvoted"]/@title').extract_first()
			num_of_comments = new.xpath('.//li[@class = "first"]/a/text()').extract_first().split(' ')[0]
			submitter = new.xpath('.//p[@class = "tagline "]/a/text()').extract_first()
			submitter_link = new.xpath('.//p[@class = "tagline "]/a/@href').extract()[0]
			subreddit = new.xpath('@data-subreddit').extract()[0]

			yield scrapy.Request(comment_url, callback=self.parse_comments, 
								meta={#'rank':rank, 
								'title': title, 'source': source,'date':date,'time':time, 'topic_vote': topic_vote, 'link':link,
								'num_of_comments':num_of_comments,'submitter':submitter,'submitter_link':submitter_link, 'subreddit':subreddit})
		yield scrapy.Request(next_button_url, callback = self.parse)

		


	def parse_comments(self, response):
		#rank = response.meta['rank']
		title = response.meta['title']
		source = response.meta['source']
		date = response.meta['date']
		time = response.meta['time']
		topic_vote = response.meta['topic_vote']
		link = response.meta['link']
		num_of_comments = response.meta['num_of_comments']
		submitter = response.meta['submitter']
		submitter_link = response.meta['submitter_link']
		subreddit = response.meta['subreddit']
		# use beautifulsoup to parse the comment, since many comments having multiple paragraphs (p tags)
		top_comment_container=response.xpath('//div[@class="commentarea"]//div[@class="md"]').extract()[0]
		top_comment_container = soup(top_comment_container, "html.parser")
		# get all the text below 
		top_comment= top_comment_container.get_text().replace('\n',' ')
		top_comment_vote = response.xpath('.//div[@class="commentarea"]//div[@class="sitetable nestedlisting"]/div/div[2]/p/span[4]/text()').\
		extract()[0].split(' ')[0]
		top_comment_child = response.xpath('.//div[@class="entry unvoted"]/p[@class="tagline"]/a[@class="numchildren"]/text()').extract()[0].split(' ')[0][1:]
		percentage_of_upvotes = response.xpath('/html//div[@class="side"]//div[@class="score"]/text()').extract()\
		[1].strip()[1:4]
		commenter_url = response.xpath('//div[@class="commentarea"]//p[@class="tagline"]/a[2]/@href').extract()[0]
		top_comment_username = re.findall(r'user/\w+',commenter_url)[0][5:]
		
		yield scrapy.Request(commenter_url,callback=self.parse_interests,
			meta={#'rank':rank,
			'title': title, 'source': source,'date':date,'time':time, 'topic_vote': topic_vote, 'link':link,
								'num_of_comments':num_of_comments,'submitter':submitter,'submitter_link':submitter_link, 'subreddit':subreddit,
								'top_comment':top_comment, 'top_comment_vote':top_comment_vote, 'percentage_of_upvotes': percentage_of_upvotes,
								'top_comment_username':top_comment_username, 'top_comment_child':top_comment_child})


	def parse_interests(self, response):
		#rank = response.meta['rank']
		meta = response.meta

		title = response.meta['title']
		source = response.meta['source']
		date = response.meta['date']
		time = response.meta['time']
		topic_vote = response.meta['topic_vote']
		link = response.meta['link']
		num_of_comments = response.meta['num_of_comments']
		submitter = response.meta['submitter']
		submitter_link = response.meta['submitter_link']
		subreddit = response.meta['subreddit']
		top_comment = response.meta['top_comment']
		top_comment_vote = response.meta['top_comment_vote']
		top_comment_child = response.meta['top_comment_child']
		percentage_of_upvotes = response.meta['percentage_of_upvotes']
		top_comment_username = response.meta['top_comment_username']
		# find subreddits that the user is interested in
		next_page = response.xpath('//span[@class="next-button"]/a/@href').extract_first()
		user_interests = response.meta.get('user_interests', [])
		user_interests.extend((response.xpath('//div[@onclick="click_thing(this)"and @data-type="comment"]/@data-subreddit').extract()))
		meta['user_interests'] = user_interests
		yield scrapy.Request(next_page, callback=self.parse_interests, meta=meta)



		item = RedditItem()
		#item['rank'] = rank
		item['title'] = title
		item['source'] = source
		item['date'] = date
		item['time'] = time
		item['topic_vote'] = topic_vote
		item['link'] = link
		item['num_of_comments'] = num_of_comments
		item['submitter'] = submitter
		item['submitter_link'] = submitter_link
		item['subreddit'] = subreddit
		item['top_comment'] = top_comment
		item['top_comment_vote'] = top_comment_vote
		item['percentage_of_upvotes'] = percentage_of_upvotes
		item['top_comment_username'] = top_comment_username
		item['user_interests'] = set(user_interests)
		item['top_comment_child'] = top_comment_child
	
		yield item
	














