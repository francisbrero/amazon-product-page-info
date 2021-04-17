// get_info.js
'use strict';

var Nightmare = require('nightmare');
var nightmare = Nightmare({ show: false })
var args = process.argv.slice(2);
var sku = args[0]
var url = 'https://www.amazon.com/dp/'+sku

nightmare
  .goto(url)
  .wait('#nav-main')
  .html('./data/page.html', 'HTMLOnly')
  .run(function(err, nightmare) {
    if (err) {
      console.log(err);
    }
    process.exit()
  });