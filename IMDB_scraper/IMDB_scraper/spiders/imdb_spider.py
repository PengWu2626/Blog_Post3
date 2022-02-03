# to run 
# scrapy crawl imdb_spider -o results.csv

import scrapy
from scrapy.spiders import Spider
from scrapy.http import Request

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    
    # The URL is for 'Star Wars: Episode VI - Return of the Jedi' from IMDB page
    start_urls = ['https://www.imdb.com/title/tt0086190/']
   
    def parse(self, response):
       """
       This function starting at the website 'https://www.imdb.com/title/tt0086190/' 
       for the movie 'Star Wars: Episode VI - Return of the Jedi' from IMDB;
       then navigate to the Cast & Crew page with URL of the form
       'https://start_urls/fullcredits/'
       """

       # get the link for the Cast & Crew page (fullcredits/)
       # Notes: No slash at the begining of the path "fullcredits/"
       next_link = next_link = response.css('div.SubNav__SubNavContentBlock-sc-11106ua-2 ul.ipc-inline-list a').attrib['href']
       # join the link of the Cast & Crew page to our current URL path
       # hers is : https://www.imdb.com/title/tt0086190/fullcredits/
       cast_link = response.urljoin(next_link)

       # yield a request to follow the Cast & Crew page,
       # and call the method parse_full_credits() once get there
       yield Request(cast_link, callback = self.parse_full_credits)


    def parse_full_credits(self, response):
       """
       This function pareses the Full Cast & Crew page
       of the movie from URL the 'https://start_urls/fullcredits/',
       then navigate to each actors page (Crew members are not included).
       """
       
       # list of links for negative to each actor page (ex: '/name/nm0000434/')
       # Notes: There is a slash at the begining of the path "/name/nm0000434/"
       links = [a.attrib["href"] for a in response.css("td.primary_photo a")]
       
       # for all actors on the current page,
       # yield a request to follow those actor's link,
       # and call the method parse_actor_page () when each actor’s page is reached
       for link in links:
          # add the base URL (https://www.imdb.com) to each actor's link (ex: https://www.imdb.com/name/nm0000434/)
          url= response.urljoin(link)
          yield Request(url, callback= self.parse_actor_page)


    def parse_actor_page(self, response):
       """
       This function get each actor's page,
       It should yield a dictionary with the name of the actor and the name of each movie or TV show   
       """
       # get the actor's name
       actor_name = response.css('span.itemprop ::text').get()

       # a list contains all movies or TV shows name for the current page's actor
       # male is under actor
       # female is under actress
       filmography_actor = [actor_name.css("a::text").get() for actor_name in response.css('div.filmo-row') if actor_name.css("[id^=actor]") or actor_name.css("[id^=actress]")]
       # for all movie or TV show name on this actor's page, 
       # yield one dictionary contains the actor's name and each movie or TV show
       for movie_or_TV_name in filmography_actor:
        yield{
           "actor" : actor_name,
           "movie_or_TV_name" : movie_or_TV_name
        }