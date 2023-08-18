import scrapy

class nbaSpider(scrapy.Spider):
    name = 'scoringLeaders'
    start_urls = ['https://www.espn.com/nba/seasonleaders/_/league/nba/sort/avgPoints']

    def parse(self, response):
        title = response.css('title::text').get()

        for players in response.css('div.mod-content'):
                yield {
                'ppg': players.css('td:nth-child(14)::text').getall(),
                'name': players.css('td:nth-child(2) a::text').getall(),
                'team': players.css('td:nth-child(3)::text').getall()
                }