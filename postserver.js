var fs = require('fs');
var http = require('http');
var url = require('url');
var querystring = require('querystring');
var Twit = require('twit');
var utf = require('utf8');
var path= require('path');

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
                count: 300
            }, function (err, data) {
                if (err) {
                    console.log("err" + err);
                } else {
                    for (var index in data.statuses) {
                        
                                var tweet = data.statuses[index];
                                console.log(tweet.text + "hhhhh");
                                // var datetime=formatDateTime(tweet.created_at);
                                //if(tweet.place.name != null && tweet.coordinates.coordinates != null)
                                    //tweetList.push({'id': tweet.id_str,'userId': tweet.user.id, 'name': tweet.user.name, 'text': tweet.text, 'retweet_count': tweet.retweet_count, 'place': tweet.place.name, "coordinates": tweet.coordinates.coordinates});
                                //else
                                     tweetList.push({'id': tweet.id_str,'userId': tweet.user.id, 'name': tweet.user.name, 'text': tweet.text, 'retweet_count': tweet.retweet_count});
                                //storeIntoDb(tweet.id_str, tweet.user.id, tweet.user.name, datetime, utf.encode(tweet.text), retweet_count);
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