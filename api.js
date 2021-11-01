// npm install google-play-scraper
// node api.js
var gplay = require('google-play-scraper');

gplay.developer({
    devId: "Qiiwi Games AB",
    fullDetail: true
}).then(function (developer) {
    for (const [_, data] of Object.entries(developer)) {
        console.log(data.appId);
    }
}).catch(function (e) {
    console.log('There was an error fetching the reviews');
});
