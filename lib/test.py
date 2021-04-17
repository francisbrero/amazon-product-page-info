try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

try:
	from Naked.toolshed.shell import execute_js, muterun_js
except ImportError:
	print("could not load Naked")

try:
	import csv
except ImportError:
	print("could not load CSV")

try:
	import tqdm
except ImportError:
	print("could not load TQDM")

try:
	from asyncio_throttle import Throttler
except ImportError:
	print("could not load async")

sku = 'B006GQHRU8'

def parse_sku(sku: str):
	try:
		result = execute_js('lib/get_info.js '+' '+sku)
		with open('./data/page.html', 'rb') as file:
			soup = BeautifulSoup(file,"html.parser")
			avail = ''
			try:
				avail = soup.find_all("div", id="availability".split())[0].text.strip().replace('\n','')
				print(avail)
				# return avail
			except:
				print('somethign went wrong')
	except:
		print('could not scrape SKU ' + sku)		

parse_sku(sku)