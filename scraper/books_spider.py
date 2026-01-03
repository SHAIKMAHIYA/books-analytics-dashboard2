import scrapy

class BooksSpider(scrapy.Spider):
    name = "books"
    start_urls = ["https://books.toscrape.com/"]

    custom_settings = {
        "FEEDS": {
            "../data/books.csv": {
                "format": "csv",
                "overwrite": True
            }
        }
    }

    def parse(self, response):
        for book in response.css("article.product_pod"):
            yield {
                "title": book.css("h3 a::attr(title)").get(),
                "price": float(book.css("p.price_color::text").get()[1:]),
                "availability": book.css(
                    "p.instock.availability::text"
                ).getall()[-1].strip()
            }

        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
