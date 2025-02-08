from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class CrawlingSpider(CrawlSpider):
  name = "mycrawler"
  allowed_domains = ["coursera.org"]
  start_urls = [f"https://www.coursera.org/courses?page=2&sortBy=BEST_MATCH"]

  rules = (  
    Rule(LinkExtractor(allow='/courses'), callback='parse_course', follow=False),  
    )  

  def parse_course(self, response):
    yield {
      "title": response.css("li.cds-9 h3.cds-CommonCard-title::text").get(),
      "partner": response.css("li.cds-9 p.cds-ProductCard-partnerNames::text").get(),
      "skills": response.css("li.cds-9 div.cds-ProductCard-body p.css-vac8rf::text").get().replace("Skills you'll gain", ""),
      "ratings": response.css("li.cds-9 div.cds-ProductCard-footer div.cds-CommonCard-ratings div[aria-label=Rating] span.css-6ecy9b::text").get(),
      "reviews": response.css("li.cds-9 div.cds-ProductCard-footer div.cds-CommonCard-ratings div.css-vac8rf::text").get(),
      "type_and_duration": response.css("li.cds-9 div.cds-CommonCard-metadata p.css-vac8rf::text").get(),
      "course_thumbnail": response.css("li.cds-9 div.cds-CommonCard-previewImage img::attr(src)").get(),
      "link": response.urljoin(response.css("li.cds-9 a.cds-CommonCard-titleLink::attr(href)").get()),
    }
