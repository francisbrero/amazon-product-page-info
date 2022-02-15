exports.handler = async (event) => {
    var sku = process.argv[2];
    var url = 'https://www.amazon.com/dp/'+sku
    const browserObject = require('./browser');



    let browserInstance = browserObject.startBrowser();
    let browser;
    try{
        browser = await browserInstance;
    }
    catch(err){
        console.log(err);
    };
    let page = await browser.newPage();

    await page.goto(url);
    // make sure the page is loaded
    await page.waitForSelector('#nav-main')
    // take a screenshot for debugging purposes
    // await page.screenshot({ path: './debug/1_screen_load.png' });
    
    // Scrape the page for the information
    let dataObj = {};

    // get availability information
    try{
        await page.$eval('#availability', function(availability) {
            return availability.innerText;
            }).then(function(result) {
                dataObj['availability'] = result;
                // console.log("availability: " + result);
        });
    }
    catch(err){
        dataObj['availability'] = "unable to determine availability";
        // console.log("not able to get availability, sad... " + err);
    };

    // get sold_by information
    try{
        await page.$eval('#sellerProfileTriggerId', function(seller_by_box) {
            return seller_by_box.innerText;
        }).then(function(result) {
            dataObj['sold_by'] = result;
            // console.log("seller: "+result);
        });
    }
    catch(err){
        dataObj['sold_by'] = "N/A";
        // console.log("not able to get sold_by, sad... " + err);
    };

    // get ship_by information
    try{
        await page.$eval('#tabular-buybox > div.tabular-buybox-container > div:nth-child(2) > div > span', function(ship_by) {
            return ship_by.innerText;
        }).then(function(result) {
            dataObj['ship_by'] = result;
            console.log("ship by: "+result);
        });
    }
    catch(err){
        dataObj['ship_by'] = "N/A";
        // console.log("not able to get ship_by, sad... " + err);
    };

    console.log(dataObj);

    // close the browser
    await browser.close();
    console.log('I am done')

    const response = {
        statusCode: 200,
        body: dataObj,
    };
    return response;
};
