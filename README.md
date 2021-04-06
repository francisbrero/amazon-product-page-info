# amazon-product-page-info
Get info about SKUs from csv file

Hit the amazon page of a SKU, look for div id="availability" as well as "tabular-buybox-text"

next step => load a csv of all SKUs and append the information at runtime

## first time?
`python3 -m venv env`
`chmod +x ./setup_env.sh`
`npm install`

## load the tools (python and node.js) and start virtuel env
`sh setup_env.sh`

## Stop virtual env
`deactivate` 

test 
`node lib/get_info.js B006GQHRU8`