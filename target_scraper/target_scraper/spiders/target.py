import re
import json
import scrapy
import logging
from scrapy import Request
from urllib.parse import urlencode


class TargetSpider(scrapy.Spider):
    name = "target"
    allowed_domains = ["www.target.com"]

    api_slug = 'https://redsky.target.com/redsky_aggregations/v1/web/pdp_client_v1?'

    headers = {
        'authority': 'redsky.target.com',
        'accept': 'application/json',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'origin': 'https://www.target.com',
        'referer': '',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }

    params = {
        'key': '9f36aeafbe60771e321a7cc95a78140772ab3e96',
        'tcin': '',
        'is_bot': 'false',
        'store_id': '2485',
        'pricing_store_id': '2485',
        'has_pricing_store_id': 'true',
        'has_financing_options': 'true',
        'visitor_id': '0188297C979F02019FFCC0097A975B28',
        'has_size_context': 'true',
        'latitude': '9.960',
        'longitude': '76.250',
        'zip': '68200',
        'state': 'KL',
        'skip_personalized': 'true',
        'channel': 'WEB',
        'page': '',
    }

    def __init__(self, *args, **kwargs):
        super(TargetSpider, self).__init__(*args, **kwargs)
        self.url = kwargs.get("url")
        # scrapy crawl target -a url=https://www.target.com/p/baby-trend-expedition-race-tec-jogger-travel-system-8211-ultra-gray/-/A-79344798

        product_id = self.url.split("?")[0].split("/")[-1].split("&")[0].split("#")[0]
        self.params['page'] = '/p/'+product_id
        self.params['tcin'] = product_id.split('-')[-1]
        self.headers['referer'] = self.url

    def start_requests(self):
        api = self.api_slug+urlencode(self.params)
        yield Request(
            url=api,
            callback=self.parse,
            headers=self.headers,
            dont_filter=True,
        )

    def parse(self, response):
        """Data Extraction"""
        json_data = json.loads(response.text)['data']
        product_data = json_data.get('product',{})

        if product_data:
            title = product_data.get("item",{}).get("product_description",{}).get("title","")
            tcin = product_data.get('tcin',"")
            upc = product_data.get('item',{}).get('primary_barcode',"")
            price_amount = product_data.get('price',{}).get('current_retail',None)
            description = product_data.get("item",{}).get("product_description",{}).get("downstream_description","")
            bullets_raw_list = product_data.get("item",{}).get("product_description",{}).get("soft_bullets",{}).get("bullets",[])
            features_raw_list = product_data.get("item",{}).get("product_description",{}).get("bullet_descriptions")

            try:
                if not upc:
                    if product_data.get('children',[]):
                        upc = product_data.get('children',[])[0].get('item').get('primary_barcode')
            except:
                logging.info('UPC not found...')
                upc = ''

            # Data Cleaning
            description = description.replace('<br />','')
            bullets = ' '.join(bullets_raw_list)
            features_list = []
            for features_values in features_raw_list:
                features_value_list = features_values.split(':')
                feature_key = (features_value_list[0].strip('<B>')).strip()
                feature_value = (features_value_list[1].strip('</B>')).strip()
                features_list.append({feature_key:feature_value})

            # Final Data
            output_data = {
                "url": self.url,
                "product_title": title,
                "tcin": str(tcin), 
                "upc": str(upc), 
                "price_amount": price_amount,
                "currency": "USD",
                "description": description, 
                "specs": None,
                "ingredients": [], 
                "bullets": bullets, 
                "features": features_list
            }

            print(output_data)

            # Write JSON data to the file
            file_path = "finalData.txt"
            with open(file_path, 'w') as file:
                json.dump(output_data, file, indent=4)

            logging.info (f"JSON data has been written to {file_path}")



