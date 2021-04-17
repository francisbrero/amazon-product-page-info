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
	import asyncio
	from asyncio_throttle import Throttler
except ImportError:
	print("could not load async")


cnt = 0
err = 0

async def write_result(result, writer):
	print(result)
	try:
		writer.writerow(result)
	except:
		print("failed to write")

async def parse_sku(sku: str, writer):
	print('looking into ' + sku)
	try:
		result = execute_js('lib/get_info.js '+' ' + sku)
	    # JavaScript is successfully executed
	    # Open file and parse
		with open('./data/page.html', 'rb') as file:
			soup = BeautifulSoup(file,"html.parser")

		avail = ''
		sold_by = ''
		ship_by = ''
		all_options = ''

		try:
			avail = soup.find_all("div", id="availability".split())[0].text.strip().replace('\n','')

			sold_buy_box = soup.find_all("span", id="tabular-buybox-truncate-0".split())[0]
			sold_by = sold_buy_box.find("span", class_="tabular-buybox-text").text.strip()

			ship_by_box = soup.find_all("span", id="tabular-buybox-truncate-1".split())[0]
			ship_by = ship_by_box.find("span", class_="tabular-buybox-text").text.strip()

			new_row = [sku.strip(), avail, sold_by, ship_by]
			await write_result(new_row, writer)			
			# f.write('"' + sku + '", "' + avail + '", "' + sold_by + '"' +',"' + ship_by + '"\n')
			cnt =+1
		except:
			# in some cases there is no seller available and there is only a buybox to show all options => we'll process that separately
			# let's check to see if there is that buybox option there if so we consider the product not available
			try:
				avail = soup.find_all("	", id="buybox-see-all-buying-choices".split())[0].text.strip().replace('\n','')
				sold_by = 'N/A'
				ship_by = 'N/A'
				
				await write_result(avail, writer)
				# f.write('"' + sku + '", "' + avail + '", "' + sold_by + '"' +',"' + ship_by + '"\n')
				cnt =+1
			except:
				# in some cases only second hand products are available
				try:
					all_options = soup.find_all("div", id="usedbuyBox".split())
					avail = "Used - "+soup.find_all("div", id="availability".split())[0].text.strip().replace('\n','')
					sold_by = soup.find_all("a", id="sellerProfileTriggerId".split())[0].text.strip().replace('\n','')
					ship_by = 'N/A'
					
					new_row = [sku.strip(), avail, sold_by, ship_by]
					await write_result(new_row, writer)	
					# f.write('"' + sku + '", "' + avail + '", "' + sold_by + '"' +',"' + ship_by + '"\n')
					cnt =+1
				except:
					# in some rare cases, products are completely out of stock
					try: 
						all_options = soup.find_all("div", id="outOfStock".split())
						avail = 'Out of Stock'
						sold_by = 'N/A'
						ship_by = 'N/A'
						
						new_row = [sku.strip(), avail, sold_by, ship_by]
						await write_result(new_row, writer)	
						# f.write('"' + sku + '", "' + avail + '", "' + sold_by + '"' +',"' + ship_by + '"\n')
						cnt =+1
					except:
						print("error with parsing info for SKU " + sku)
						err =+1
	except:
		print('could not scrape SKU ' + sku)


async def main():
	with open('./input/sku_list.csv', newline='') as csv_in, open("./output/amazon_stuff.csv", 'w+') as csv_out:
		writer = csv.writer(csv_out, delimiter=',')
		amazon_info = [parse_sku(row, writer) for row in csv_in]
		await asyncio.gather(*amazon_info)
		print('!--- finished processing')


# Run the loop asynchronously
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
