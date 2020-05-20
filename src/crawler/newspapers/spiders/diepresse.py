import scrapy
import json
from datetime import datetime

class DiePresseSpider(scrapy.Spider):
    name = "diepresse"

    def start_requests(self):
        sessionid = 'B26113953C9B79B0F702178BA7CEA602.13' #load page and check jsessionid cookie

        url = 'https://diepresse.com/user/search.do;jsessionid=' + sessionid + \
                  '?resultsPage=0&resetForm=0&searchText=&action=search&autor=0&autorname=&zeitpunkt=1'+ \
                  '&dayOnly=8&monthOnly=5&yearOnly=2018' + \
                  '&dayFrom=1&monthFrom=4&yearFrom=2018' + \
                  '&dayTo=30&monthTo=4&yearTo=2018' + \
                  '&ress=1&ress=2&ress=3&ress=4&ress=5&ress=6&ress=7&ress=8&ress=9&ress=10&ress=11&ress=13&ress=14&ress=15'

        yield scrapy.Request(url=url, callback=self.parse_archive, cookies={'JSESSIONID' : sessionid})

    def parse_archive(self, response):
        links = response.css('li.searchresults__item a::attr(href)').extract()
        dates = response.css('li.searchresults__item .searchresults__timestamp::text').extract()

        for link, date in zip(links, dates):
            print (link, date)
            urlbase = 'https://diepresse.com'
            url = urlbase + link
            yield scrapy.Request(url=url, callback=self.parse_article)

        next_page = response.css('ol.nav.pagination li.pagination__last a::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse_archive
            )

    def parse_article(self, response):
        page = response.url.split("/")[-2]
        filename = 'tmp/diepresse-%s.json' % page

        with open(filename, 'w') as f:
            fullarticle = {}
            headline = response.css('h1.article__headline::text').extract_first()
            subheadline = response.css('p.article__lead::text').extract_first()
            articleHeaders = response.css('#content-body h2::text').extract()
            datePublished = response.css('.article__main .article__timestamp::text').extract_first()
            imgCaption = response.css('.article__figure .article__media-caption ::text').extract_first()
            breadcrumbs = response.css("nav.show-on-big-screen .breadcrumbs__menu .breadcrumbs__item a::text").extract()

            if len(breadcrumbs) > 1:
                category = breadcrumbs[1]
            else:
                category = None
            if len(breadcrumbs) > 2:
                subcategory = breadcrumbs[2]
            else:
                subcategory = None


            # get contents
            article = []
            for paragraph in response.css('#content-body p'):
                article.append(''.join(paragraph.css("::text").extract()))

            #fix date format
            datePublished = datetime.strptime(datePublished.strip(),'%d.%m.%Y um %H:%M').astimezone().isoformat()

            fullarticle["headline"] = headline
            fullarticle["lead"] = subheadline
            fullarticle["content"] = article
            fullarticle["date"] = datePublished
            fullarticle["content-headers"] = articleHeaders
            fullarticle["image-caption"] = imgCaption
            fullarticle["url"] = response.url
            fullarticle["category"] = category
            fullarticle["subcategory"] = subcategory

            #json.dump(fullarticle, f)
            yield fullarticle
        self.log('Saved file %s' % filename)