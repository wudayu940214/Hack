var fs = require('fs');
var http = require('http');
var url = require('url');
var querystring = require('querystring');
var Twit = require('twit');
var utf = require('utf8');
var path= require('path');
var regex = /(?:[\u2700-\u27bf]|(?:\ud83c[\udde6-\uddff]){2}|[\ud800-\udbff][\udc00-\udfff]|[\u0023-\u0039]\ufe0f?\u20e3|\u3299|\u3297|\u303d|\u3030|\u24c2|\ud83c[\udd70-\udd71]|\ud83c[\udd7e-\udd7f]|\ud83c\udd8e|\ud83c[\udd91-\udd9a]|\ud83c[\udde6-\uddff]|\ud83c[\ude01-\ude02]|\ud83c\ude1a|\ud83c\ude2f|\ud83c[\ude32-\ude3a]|\ud83c[\ude50-\ude51]|\u203c|\u2049|[\u25aa-\u25ab]|\u25b6|\u25c0|[\u25fb-\u25fe]|\u00a9|\u00ae|\u2122|\u2139|\ud83c\udc04|[\u2600-\u26FF]|\u2b05|\u2b06|\u2b07|\u2b1b|\u2b1c|\u2b50|\u2b55|\u231a|\u231b|\u2328|\u23cf|[\u23e9-\u23f3]|[\u23f8-\u23fa]|\ud83c\udccf|\u2934|\u2935|[\u2190-\u21ff])/g;
// Configure the twitter
var client = new Twit({
    consumer_key: '9MXIxRBS9mmQrdJ2VUjFI193G',
    consumer_secret: 'JP1PpFb1G6JKuinjGAx0MSSuEgpe3Z4MEt9Khi6oU1JDRbkdcx',
    access_token: '838522627207671808-rrdHvVYZRKpY44S38nn6gn5Smli1CI2',
    access_token_secret: 'URONc6AZmphJcGuJyJR5yiLV9cdsgMPHLKpDOFmmBCHJ5'
});


var server = http.createServer(function (request, response) {
    if (request.method == 'POST') {
        var body = '';
        var tweetList=[];
        var resultList = [];
        var databaseList =[];
        var tweetText = '';
        var count = 1;
        request.on('data', function (data) {
            body += data;
            // if body >  1e6 === 1 * Math.pow(10, 6) ~~~ 1MB
            // flood attack or faulty client
            // (code 413: request entity too large), kill request
            if (body.length > 1e6) {
                response.writeHead(413,
                    {'Content-Type': 'text/plain'}).end();
                request.connection.destroy();
            }
        });
        request.on('end', function () {
            var POST = querystring.parse(body);
            console.log(POST);
            response.writeHead(200, {"Content-Type": "text/plain"});
            console.log(POST.keyword);

            client.get('search/tweets', {
                q: POST.keyword,
                count: 300,
                lang: "en"
            }, function (err, data) {
                if (err) {
                    console.log("err" + err);
                } else {
                    for (var index in data.statuses) {
                        
                                var tweet = data.statuses[index];
                                
                                // var datetime=formatDateTime(tweet.created_at);
                                //if(tweet.place.name != null && tweet.coordinates.coordinates != null)
                                    //tweetList.push({'id': tweet.id_str,'userId': tweet.user.id, 'name': tweet.user.name, 'text': tweet.text, 'retweet_count': tweet.retweet_count, 'place': tweet.place.name, "coordinates": tweet.coordinates.coordinates});
                                //else
                                tweetText = tweet.text.replace(regex, '');
                                console.log(tweetText + " " + count);
                                tweetList.push({'id': tweet.id_str,'userId': tweet.user.id, 'name': tweet.user.name, 'text': tweetText, 'retweet_count': tweet.retweet_count});
                                //storeIntoDb(tweet.id_str, tweet.user.id, tweet.user.name, datetime, utf.encode(tweet.text), retweet_count);
                                count ++;
                    }
                    resultList.push({'tweetList':tweetList});
                    //response.write(JSON.stringify(resultList));
                    // response.end();
                    fs.writeFile("twit.txt", JSON.stringify(resultList), function(err, data){
                    });
                    response.end('Hello ' + POST.keyword +  JSON.stringify(resultList) + '\n');
                }
            });
        });
    }
});
// Listen on port 3000, IP defaults to 127.0.0.1 (localhost)
server.listen(3000);