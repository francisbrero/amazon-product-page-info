try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

# Change encoding to avoid silly errors
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Create the output csv file and create headers
f = open('./output/amazon_stuff.csv', 'w+')
f.write('"sku", "avail","sold by", "ship by"\n')

# Open file and parse
with open('./data/page.html', 'rb') as file:
    soup = BeautifulSoup(file,"html.parser")

cnt = 0
err = 0

# initialize
sku = 'blabla'
avail = ''
sold_by = ''
ship_by = ''

avail = soup.find_all("div", id="availability".split())[0].text.strip()
sold_by = soup.find_all("span", id="tabular-buybox-truncate-0".split())[0].text.strip()
ship_by = soup.find_all("span", id="tabular-buybox-truncate-1".split())[0].text.strip()


print(ship_by)