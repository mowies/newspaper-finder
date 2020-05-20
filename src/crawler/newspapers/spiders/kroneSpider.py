import scrapy
from datetime import datetime


class KroneSpider(scrapy.Spider):
    name = 'krone'
    url = 'http://www.krone.at/'
    startID = 1660000
    endID =   1725000
    currentID = startID

    def start_requests(self):
        for i in range(self.startID,self.endID):
            yield scrapy.Request(self.url + str(i), self.parse)

    def strip_first(self,textResponse):
        field = textResponse.extract_first()
        if field is None:
            return ""
        return field.strip();
    def strip_all(self,textResponse):
        result = []
        for text in textResponse.extract():
          result.append(text.strip())
    def parse(self, response):

        # get contents
        article = []
        for paragraph in response.css('div.c_content p'):
            article.append(''.join(paragraph.css("::text").extract()))

        yield {
            'url':response.url,
            'image-caption':self.strip_first(response.css('div.c_featured-image .c_caption::text')),
            'headline': self.strip_first(response.css('div.c_title h1::text')),
            'lead': self.strip_first(response.css('div.c_lead p ::text')),
            'content-headers': self.strip_all(response.css('div.c_content p strong::text')),
            'content': article,
            'category': self.strip_first(response.css('meta[name="krn-ressort-slug"]::attr(content)')),
            'date': datetime.strptime(self.strip_first(response.css('div.c_pretitle div.c_time::text')),'%d.%m.%Y %H:%M').astimezone().isoformat(),
        }