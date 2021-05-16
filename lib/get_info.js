// get_info.js
'use strict';

var Nightmare = require('nightmare');
var args = process.argv.slice(2);
var sku = args[0]
var url = 'https://www.amazon.com/dp/'+sku
var debug = args[1] || false
var nightmare = Nightmare({ show: debug })

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