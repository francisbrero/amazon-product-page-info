# amazon-product-page-info
Get info about SKUs from csv file

Hit the amazon page of a SKU, look for div id="availability" as well as "tabular-buybox-text"

next step => load a csv of all SKUs and append the information at runtime

## first time?
`python3 -m venv env`

`chmod +x ./setup_env.sh`

`npm install`

## load the tools (python and node.js) and start virtuel env
`python3 -m venv "./env"`

`source "./env/bin/activate"`

`sh setup_env.sh`

## Update the list of SKUs to monitor
in input>sku_list.csv add the SKUs to listen to

## Run it!!!!
`python lib/info_parse.py`

You will now have an output csv with the desired goods

## Stop virtual env
`deactivate` 

## Debug
### test 
`node lib/get_info.js B006GQHRU8`

## Context
This leverages nightmare.js which was developed by Segment as a scraper on top of electron

Possible improvements
- store website in memory rather than writing on disk
- multi-thread
- This could be made into a Lambda to scale and be managed more easily