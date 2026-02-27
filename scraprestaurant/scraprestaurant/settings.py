# Scrapy settings for scraprestaurant project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "scraprestaurant"

SPIDER_MODULES = ["scraprestaurant.spiders"]
NEWSPIDER_MODULE = "scraprestaurant.spiders"

ADDONS = {}


SCRAPEOPS_API_KEY = '936520c0-f41f-4496-b392-bd95d4cc8865' 
SCRAPEOPS_FAKE_BROWSER_HEADER_ENABLED = True
SCRAPEOPS_FAKE_USER_AGENT_ENABLED = True
SCRAPEOPS_NUM_RESULTS = 100


SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT = 'https://headers.scrapeops.io/v1/user-agents'
SCRAPEOPS_FAKE_BROWSER_HEADER_ENDPOINT = 'https://headers.scrapeops.io/v1/browser-headers'

DOWNLOADER_MIDDLEWARES = {
    'scraprestaurant.middlewares.ScrapeOpsFakeUserAgentMiddleware': 400,        # Runs first
    'scraprestaurant.middlewares.ScrapeOpsFakeBrowserHeaderAgentMiddleware': 410,  # Runs second
    'scraprestaurant.middlewares.ScrapeProxyMiddleware': 420,  # Runs third
}

DOWNLOADER_MIDDLEWARES.update({
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None, # Prevents data waste on circular redirects
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 590, # Keep this ON (Gzip saves data)
})

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
    'Accept-Language': 'en',
}


# Obey robots.txt rules
CONCURRENT_REQUESTS_PER_DOMAIN = 1
ROBOTSTXT_OBEY = False


# INSTEAD OF USING DOWNLOAD_DELAY AUTOTHROTTLE IS A BEST OPTION 
# DOWNLOAD_DELAY = 3

# Don't waste time on dead free proxies
RETRY_TIMES = 5  # Try up to 10 different proxies before giving up
DOWNLOAD_TIMEOUT = 40

# 3. Disable images to save data
# Add this if you haven't already to prevent downloading bulky media
MEDIA_ALLOW_REDIRECTS = False

METAREFRESH_ENABLED = False

# Only allow these types of data
# This prevents downloading of .jpg, .png, .gif, .mp4, etc.
def should_abort_request(request):
    if any(ext in request.url.lower() for ext in ['.jpg', '.png', '.gif', '.css', '.woff', '.js']):
        return True
    return False


# Autothrottle is a "smart" system that speeds up when the website is fast and slows down if the website starts showing signs of blocking you.
# 1. Enable the AutoThrottle extension
AUTOTHROTTLE_ENABLED = True
# 2. The initial download delay (starts at 5 seconds)
AUTOTHROTTLE_START_DELAY = 5
# 3. The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# 4. The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# 5. Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = True

# Disable cookies (enabled by default)
COOKIES_ENABLED = False


# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "scraprestaurant.middlewares.ScraprestaurantSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "scraprestaurant.middlewares.ScraprestaurantDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "scraprestaurant.pipelines.ScraprestaurantPipeline": 300,
#}


# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
FEED_EXPORT_ENCODING = "utf-8"
