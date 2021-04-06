// get_info.js
'use strict';

var Nightmare = require('nightmare');
var args = process.argv.slice(2);
var sku = args[0]
var url = 'https://www.amazon.com/dp/'+sku

new Nightmare()
  .goto(url)
  .wait(10)
  .html('./data/page.html', 'HTMLComplete')
  // .screenshot('./debug/1_screen_load.png')
  .run(function(err, nightmare) {
    if (err) {
      console.log(err);
    }
    // console.log('scraping ' + sku)
    process.exit()
  });