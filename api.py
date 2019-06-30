# examples/server_simple.py
import asyncio
import aiohttp
from aiohttp import web
import selectorlib
from selectorlib.formatter import Formatter

class Price(Formatter):
    def format(self, text):
        price = text.replace('£','').strip()
        return float(price)

product_page_extractor = selectorlib.Extractor.from_yaml_file('ProductPage_with_Formatter.yml',formatters = [Price])

async def get_product_page(request):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        product_url = request.rel_url.query['product_url']
        data = {'error':'Please provide a URL'}
        if product_url:
            html = await fetch(session, product_url)
            data = product_page_extractor.extract(html)
    return web.json_response(data)

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


app = web.Application()
app.add_routes([web.get('/', get_product_page)])

if __name__ == '__main__':
    web.run_app(app)