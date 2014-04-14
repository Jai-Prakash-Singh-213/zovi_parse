# Scrapy settings for zovi project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'zovi'

SPIDER_MODULES = ['zovi.spiders']
NEWSPIDER_MODULE = 'zovi.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'zovi (+http://www.yourdomain.com)'

WEBSERVICE_ENABLED = False
TELNETCONSOLE_ENABLED  = False


DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    'zovi.proxymiddle.ProxyMiddleware': 100,
}
