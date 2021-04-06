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

# Load the progressBar

with open('./input/sku_list.csv', newline='') as csvfile:
	# Open the CSV file and read it to obtain all the SKUs
	sku_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')

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

			try:
				avail = soup.find_all("div", id="availability".split())[0].text.strip()

				sold_buy_box = soup.find_all("span", id="tabular-buybox-truncate-0".split())[0]
				sold_by = sold_buy_box.find("span", class_="tabular-buybox-text").text.strip()

				ship_by_box = soup.find_all("span", id="tabular-buybox-truncate-1".split())[0]
				ship_by = ship_by_box.find("span", class_="tabular-buybox-text").text.strip()

			
				f.write('"' + sku + '", "' + avail + '", "' + sold_by + '"' +',"' + ship_by + '"\n')
				cnt =+1
			except:
				print("error with SKU " + sku)
				err =+1

		else:
		    # JavaScript is failed
		    print("something went wrong with row "+row)
	
print("and we're done!")