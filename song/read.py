from lxml import html
import requests
from .models import Songs, Words, WordsOfSongs

page = requests.get('https://en.wikipedia.org/wiki/Hayim_Nahman_Bialik')
tree = html.fromstring(page.content)

content = tree.xpath('//h1[@class="firstHeading"]/text()')

name= tree.xpath('//div[@class="mw-parser-output"]/p/text()')


