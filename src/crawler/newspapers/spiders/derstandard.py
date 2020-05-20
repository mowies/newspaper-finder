import scrapy
import json

class DerStandardSpider(scrapy.Spider):
    name = "derstandard"

    def start_requests(self):
        data = [
            # {"year": '2018', "month": '5', "days": 8},
            {"year": '2018', "month": '4', "days": 30},
            # {"year": '2018', "month": '3', "days": 31}
        ]
        for d in data:
            for i in range(0, d["days"]):
                urlbase = 'https://derstandard.at/archiv/' + d["year"] + '/' + d["month"] + '/'
                fullurl = urlbase + str(i)
                yield scrapy.Request(url=fullurl, callback=self.parse_archive)

    def parse_archive(self, response):
        links = response.css('#resultlist div.text h3 a::attr(href)').extract()
        day = response.css('#menu ul a.selected span.day::text').extract_first()

        for link in links:

            urlbase = 'https://derstandard.at'
            url = urlbase + link
            yield scrapy.Request(url=url, callback=self.parse_article)

    def parse_article(self, response):
        page = response.url.split("/")[-2]
        filename = 'tmp/derstandard-%s.json' % page

        with open(filename, 'w') as f:
            fullarticle = {}
            headline = response.css('#objectContent h1[itemprop="headline"]::text').extract_first()
            subheadline = response.css('#content-main h2::text').extract_first()
            articleHeaders = response.css('#content-main h3::text').extract()
            datePublished = response.css('#content-header .date meta[itemprop="datePublished"]::attr(content)').extract_first()
            dateModified = response.css('#content-header .date meta[itemprop="dateModified"]::attr(content)').extract_first()
            imgCaption = response.css('#content-aside div.description p ::text').extract_first()
            category = response.css('#navigation #navLine1 li.active a::text').extract_first()
            subcategory = response.css('#navigation #navLine1 li.active li.active a::text').extract_first()

            # get contents
            article = []
            for paragraph in response.css('#content-main p'):
                article.append(''.join(paragraph.css("::text").extract()))

            #fix date
            datePublished = datePublished.replace('MESZ', '+02:00').replace('MEZ', '+01:00')

            fullarticle["headline"] = headline
            fullarticle["lead"] = subheadline
            fullarticle["content"] = article
            fullarticle["date"] = datePublished
            fullarticle["content-headers"] = articleHeaders
            fullarticle["image-caption"] = imgCaption
            fullarticle["url"] = response.url
            fullarticle["category"] = category
            fullarticle["subcategory"] = subcategory

            json.dump(fullarticle, f)
            yield fullarticle
        self.log('Saved file %s' % filename)