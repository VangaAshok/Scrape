import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nodero.settings')
django.setup()

import json
from scrape_app.models import Product, ProductImage
from datetime import datetime
from django.utils import timezone

# Define the path to your JSON file on the D-drive
file_path = "C:/Users/anil/Desktop/Django API/Scraper/Scrapy/men_products.json"

def load_json_data_db(file_path):

    with open(file_path, 'r', encoding='utf-8') as f: 
            data = json.load(f)
            print(data)
#     print(len(data))

    for item in data:
            
        product = Product.objects.create(
        category=item['category'],
        name=item['name'],
        price=item['price'],
        product_url=item['product_url'],
        description=item['description'],
        )

        for image_url in item['image_url']:
                
                ProductImage.objects.create(
                        product=product,
                        image_url=image_url
                )

        
load_json_data_db(file_path)