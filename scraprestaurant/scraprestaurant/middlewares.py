# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random
import requests
from scrapy import signals
from urllib.parse import urlencode
from random import randint
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ScraprestaurantSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    async def process_start(self, start):
        # Called with an async iterator over the spider start() method or the
        # matching method of an earlier spider middleware.
        async for item_or_request in start:
            yield item_or_request

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class ScraprestaurantDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)



class ScrapeOpsFakeUserAgentMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.scrapeops_api_key = settings.get('SCRAPEOPS_API_KEY')
        self.scrapeops_endpoint = settings.get('SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT', 'http://headers.scrapeops.io/v1/user-agents?') 
        self.scrapeops_fake_user_agents_active = settings.get('SCRAPEOPS_FAKE_USER_AGENT_ENABLED', False)
        self.scrapeops_num_results = settings.get('SCRAPEOPS_NUM_RESULTS')
        self.headers_list = []
        self._get_user_agents_list()
        self._scrapeops_fake_user_agents_enabled()


    def _get_user_agents_list(self):
        payload = {'api_key': self.scrapeops_api_key}
        if self.scrapeops_num_results is not None:
            payload['num_results'] = self.scrapeops_num_results
        response = requests.get(self.scrapeops_endpoint, params=urlencode(payload))
        json_response = response.json()
        self.user_agents_list = json_response.get('result', [])


    def _get_random_user_agent(self):
        random_index = randint(0, len(self.user_agents_list) - 1)
        return self.user_agents_list[random_index]

    def _scrapeops_fake_user_agents_enabled(self):
        if self.scrapeops_api_key is None or self.scrapeops_api_key == '' or self.scrapeops_fake_user_agents_active == False:
            self.scrapeops_fake_user_agents_active = False
        else:
            self.scrapeops_fake_user_agents_active = True

    def process_request(self, request, spider):        
        random_user_agent = self._get_random_user_agent()
        request.headers['User-Agent'] = random_user_agent

        print("************ NEW USER AGENT ATTACHED *******")  # 🔥 CHANGED: clearer message
        print(request.headers['User-Agent'])




class ScrapeOpsFakeBrowserHeaderAgentMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.scrapeops_api_key = settings.get('SCRAPEOPS_API_KEY')
        self.scrapeops_endpoint = settings.get('SCRAPEOPS_FAKE_BROWSER_HEADER_ENDPOINT', 'http://headers.scrapeops.io/v1/browser-headers') 
        self.scrapeops_fake_browser_headers_active = settings.get('SCRAPEOPS_FAKE_BROWSER_HEADER_ENABLED', True)
        self.scrapeops_num_results = settings.get('SCRAPEOPS_NUM_RESULTS')
        self.headers_list = []
        self._get_headers_list()
        self._scrapeops_fake_browser_headers_enabled()

    def _get_headers_list(self):
        payload = {'api_key': self.scrapeops_api_key}
        if self.scrapeops_num_results is not None:
            payload['num_results'] = self.scrapeops_num_results
        response = requests.get(self.scrapeops_endpoint, params=urlencode(payload))
        json_response = response.json()
        self.headers_list = json_response.get('result', [])

    def _get_random_browser_header(self):
        random_index = randint(0, len(self.headers_list) - 1)
        return self.headers_list[random_index]

    def _scrapeops_fake_browser_headers_enabled(self):
        if self.scrapeops_api_key is None or self.scrapeops_api_key == '' or self.scrapeops_fake_browser_headers_active == False:
            self.scrapeops_fake_browser_headers_active = False
        else:
            self.scrapeops_fake_browser_headers_active = True
    
    def process_request(self, request, spider):        
            random_browser_header = self._get_random_browser_header()

            # Use .get() to prevent KeyErrors
            request.headers['accept-language'] = random_browser_header.get('accept-language')
            request.headers['sec-fetch-user'] = random_browser_header.get('sec-fetch-user') 
            request.headers['sec-fetch-mod'] = random_browser_header.get('sec-fetch-mod') 
            request.headers['sec-fetch-site'] = random_browser_header.get('sec-fetch-site') 
            request.headers['sec-ch-ua-platform'] = random_browser_header.get('sec-ch-ua-platform') 
            request.headers['sec-ch-ua-mobile'] = random_browser_header.get('sec-ch-ua-mobile') 
            request.headers['sec-ch-ua'] = random_browser_header.get('sec-ch-ua') 
            request.headers['accept'] = random_browser_header.get('accept') 
            # 🔥 REMOVED: request.headers['user-agent'] = random_browser_header.get('user-agent') 
            request.headers['upgrade-insecure-requests'] = random_browser_header.get('upgrade-insecure-requests')

            print("************ NEW BROWSER HEADERS ATTACHED *******")  # 🔥 CHANGED: clearer message
            print(dict(request.headers))
            # 🔥 REMOVED: print(request.headers['user-agent'])


# class ScrapeProxyMiddleware:
#     def __init__(self):
#         try:
#             with open("valid_proxies.txt", "r") as f:
#                 self.proxies = f.read().splitlines()
#         except FileNotFoundError:
#             self.proxies = []

#     def process_request(self, request, spider):
#         if self.proxies:
#             # 1. First, pick the random proxy and save it to a variable named 'proxy'
#             proxy = random.choice(self.proxies)
#             # 2. Attach it to the request
#             request.meta['proxy'] = proxy
#             # 3. Now you can log it because 'proxy' is defined!
#             spider.log(f"--- 🌐 PROXY ROTATED TO: {proxy} ---")


# THIS IS FOR RESIDENTIAL API HANDLE 100MB FREE BANDTHWIDTH
class ScrapeProxyMiddleware:
    def process_request(self, request, spider):
        # Your specific ScrapeOps Residential Gateway
        proxy_address = "http://scrapeops:6fb77214-3a92-4d9c-b397-e44775146cff@residential-proxy.scrapeops.io:8181"
        # Attach the gateway to the request
        request.meta['proxy'] = proxy_address
        # Log it so you know it's working
        spider.log(f"--- 🏠 USING RESIDENTIAL PROXY GATEWAY ---")