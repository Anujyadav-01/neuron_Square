import scrapy
from ..items import NeuronItem


class NeuronSpider(scrapy.Spider):
    name = 'primer'
    page_number = 2
    start_urls = [
        'https://www.midsouthshooterssupply.com/dept/reloading/primers?currentpage=1'
    ]

    def parse(self, response, **kwargs):
        items = NeuronItem()
        html_code = response.css("div.product-container")

        for code in html_code:
            price = code.css(".price span::text").extract()
            title = code.css("a.catalog-item-name::text").extract()
            product_id = code.css("span.product-id::text").extract()
            stock = code.css("span.out-of-stock::text").extract()
            manufacturer = code.css("a.catalog-item-brand::text").extract()
            # rating = code.css("section.pr-review-snippet-container").extract()
            # description = code.css("div.product-description::text").extract()
            # delivery_info = code.css("").extract()

            items['Price'] = price
            items['Title'] = title
            items['Product_id'] = product_id
            items['Stock'] = stock
            items['Manufacturer'] = manufacturer

            yield items

        next_page = 'https://www.midsouthshooterssupply.com/dept/reloading/primers?currentpage=' + str(
            NeuronSpider.page_number) + ''
        if NeuronSpider.page_number < 3:
            NeuronSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)