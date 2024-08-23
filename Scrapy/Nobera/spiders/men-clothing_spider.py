import scrapy

class NoberoSpider(scrapy.Spider):
    name = "nobero"
    start_urls = ['https://nobero.com/pages/men']
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }


    def parse(self, response):
        # Define the subcategories you want to scrape
        subcategories = {
            'oversized_tshirts': 'https://nobero.com/collections/men-oversized-t-shirts',
            'tshirts': 'https://nobero.com/collections/pick-printed-t-shirts',
            'joggers': 'https://nobero.com/collections/fashion-joggers-men',
            'coords': 'https://nobero.com/collections/best-selling-co-ord-sets',
            'plus_size_tshirts': 'https://nobero.com/collections/plus-size-t-shirts',
            'shorts': 'https://nobero.com/collections/mens-shorts-collection'
        }
        
        # Loop through each subcategory
        for category_name, url in subcategories.items():
            yield scrapy.Request(url=url, callback=self.parse_subcategory, meta={'category_name': category_name})


    def parse_subcategory(self, response):
        category_name = response.meta['category_name']
    # On the subcategory page, extract each item's URL and follow it
        product_links = response.css('a.product_link::attr(href)').getall()

        for link in product_links:
            absolute_url = response.urljoin(link)
            yield scrapy.Request(url=absolute_url, callback=self.parse_product, meta={'category_name': category_name})


    def parse_product(self, response):
        image_urls = response.css('img.h-full::attr(src)').getall()
        image_urls = ['https:' + url if url.startswith('//') else url for url in image_urls]
        image_urls = list(set(image_urls))

        # Extract product details from the product page
        yield {
            'category': response.meta['category_name'],
            'name': response.css('h1.capitalize::text').get().strip(),
            'price': response.css('h2.text-xl spanclass::text').get().strip(),
            'image_url': image_urls,
            'product_url': response.url,
            'description': response.css('div#description_content').get(),
            
        }


