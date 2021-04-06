# amazon-product-page-info
Get info about SKUs from csv file

Hit the amazon page of a SKU, look for div id="availability" as well as "tabular-buybox-text"

next step => load a csv of all SKUs and append the information at runtime

## first time?
`python3 -m venv env`
`chmod +x ./setup_env.sh`
`npm install`

## load the tools (python and node.js)
`. setup_env.sh`