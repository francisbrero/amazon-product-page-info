// scraper.js
'use strict';

var Nightmare = require('nightmare');
new Nightmare()
  .goto('https://www.amazon.com/dp/B006GQHRU8')
  .wait(500)
  .html('./data/page.html', 'HTMLComplete')
  .screenshot('./debug/1_screen_load.png')
  .run(function(err, nightmare) {
    if (err) {
      console.log(err);
    }
    process.exit()
  });