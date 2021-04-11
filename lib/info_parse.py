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



cnt = 0
err = 0

# Create the output csv file and create headers
f = open('./output/amazon_stuff.csv', 'w+')
f.write('"sku", "availability","sold by", "ship by"\n')

sku_retry = []

with open('./input/sku_list.csv', newline='') as csvfile:
	# Open the CSV file and read it to obtain all the SKUs
	sku_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	
	# Load the progressBar
	pbar = tqdm.tqdm(sku_reader, desc="Reviewing SKUs", unit="SKU", unit_scale=True)
	# Process each SKUs
	for row in pbar:
		try:
			result = execute_js('lib/get_info.js '+' '.join(row))
		except:
			print('could not scrape')
		if result:
		    # JavaScript is successfully executed
		    # Open file and parse
			with open('./data/page.html', 'rb') as file:
			    soup = BeautifulSoup(file,"html.parser")

			# initialize
			sku = ' '.join(row)
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

			
				f.write('"' + sku + '", "' + avail + '", "' + sold_by + '"' +',"' + ship_by + '"\n')
				cnt =+1
			except:
				# in some cases there is no seller available and there is only a buybox to show all options => we'll process that separately
				# let's check to see if there is that buybox option there if so we consider the product not available
				try:
					avail = soup.find_all("	", id="buybox-see-all-buying-choices".split())[0].text.strip().replace('\n','')
					sold_by = 'N/A'
					ship_by = 'N/A'
					
					f.write('"' + sku + '", "' + avail + '", "' + sold_by + '"' +',"' + ship_by + '"\n')
					cnt =+1
				except:
					# in some cases only second hand products are available
					try:
						all_options = soup.find_all("div", id="usedbuyBox".split())
						avail = "Used - "+soup.find_all("div", id="availability".split())[0].text.strip().replace('\n','')
						sold_by = soup.find_all("a", id="sellerProfileTriggerId".split())[0].text.strip().replace('\n','')
						ship_by = 'N/A'
						
						f.write('"' + sku + '", "' + avail + '", "' + sold_by + '"' +',"' + ship_by + '"\n')
						cnt =+1
					except:
						# in some rare cases, products are completely out of stock
						try: 
							all_options = soup.find_all("div", id="outOfStock".split())
							avail = 'Out of Stock'
							sold_by = 'N/A'
							ship_by = 'N/A'
							
							f.write('"' + sku + '", "' + avail + '", "' + sold_by + '"' +',"' + ship_by + '"\n')
							cnt =+1
						except:
							print("error with parsing info for SKU " + sku)
							sku_retry.append(str(sku).strip())
							err =+1
		else:
		    # JavaScript is failed
		    print("something went wrong scraping SKU "+row)
		    err =+1

print("summary: ")
print("Processed SKUs: " + str(cnt))
print("Processed SKUs that returned errors: " + str(err))

print(r"""
 ________  ________  ________   _______           ________      ___    ___      ________  ___  ________  ___  ___  ________  ___  ________  ___  ___     
|\   ___ \|\   __  \|\   ___  \|\  ___ \         |\   __  \    |\  \  /  /|    |\   __  \|\  \|\   __  \|\  \|\  \|\   __  \|\  \|\   __  \|\  \|\  \    
\ \  \_|\ \ \  \|\  \ \  \\ \  \ \   __/|        \ \  \|\ /_   \ \  \/  / /    \ \  \|\  \ \  \ \  \|\  \ \  \\\  \ \  \|\  \ \  \ \  \|\  \ \  \\\  \   
 \ \  \ \\ \ \  \\\  \ \  \\ \  \ \  \_|/__       \ \   __  \   \ \    / /      \ \   ____\ \  \ \  \\\  \ \  \\\  \ \   ____\ \  \ \  \\\  \ \  \\\  \  
  \ \  \_\\ \ \  \\\  \ \  \\ \  \ \  \_|\ \       \ \  \|\  \   \/  /  /        \ \  \___|\ \  \ \  \\\  \ \  \\\  \ \  \___|\ \  \ \  \\\  \ \  \\\  \ 
   \ \_______\ \_______\ \__\\ \__\ \_______\       \ \_______\__/  / /           \ \__\    \ \__\ \_______\ \_______\ \__\    \ \__\ \_______\ \_______\
    \|_______|\|_______|\|__| \|__|\|_______|        \|_______|\___/ /             \|__|     \|__|\|_______|\|_______|\|__|     \|__|\|_______|\|_______|
                                                              \|___|/                                                                                    
                """)