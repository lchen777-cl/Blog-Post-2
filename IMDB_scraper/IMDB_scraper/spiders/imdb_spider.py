# to run
# scrapy crawl imdb_spider -o movies.csv
import scrapy

class ImdbSpider(scrapy.Spider):

	name = 'imdb_spider'

	start_urls = ['https://www.imdb.com/title/tt0065571/']

	def parse(self, response):
		# get the link for Cast & Crew page
		link = 'https://www.imdb.com/title/tt0065571/fullcredits/'
		#link = str(self.start_urls[0]) + 'fullcredits/'
		# go to the Cast & Crew page and call parse_full_credits
		yield scrapy.Request(link, callback = self.parse_full_credits)

	def parse_full_credits(self, response):
		 # get a list of relaive paths for each actor
		cast = [a.attrib["href"] for a in response.css("td.primary_photo a")]
		# loop through the list to enter each actor path and call parse_actor_page
		for actor in cast:
			yield scrapy.Request('https://www.imdb.com' + str(actor), callback = self.parse_actor_page)
	def parse_actor_page(self, response):
		# get actor name
		actor_name = response.css('span.itemprop::text').get()
		# get movies list
		movies_list = response.css('div.filmo-row').css('a::text').getall()
		# remove specific episode
		movies = [x for x in movies_list if not x.startswith('Episode')]
		# yield our data
		for x in movies:
			yield{
					"actor" : actor_name,
					"movie" : x
				 }