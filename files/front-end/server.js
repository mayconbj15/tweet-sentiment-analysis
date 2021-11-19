var http = require('http'); // 1 - Import Node.js core module
const { stringify } = require('querystring');
const url = require('url');


var server = http.createServer(function (req, res) {   // 2 - creating server
    var request = require('request');

    //handle incomming requests here..
    if (req.url == '/trends/avaliable') { //check the URL of the current request
        res.setHeader('Access-Control-Allow-Origin', '*');
        console.log('/trends/avaliable');
        var options = {
            'method': 'GET',
            'url': 'https://api.twitter.com/1.1/trends/available.json',
            'headers': {
                'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAKbHNAEAAAAA%2B8gitwwlUp0Vbkfq%2FjtBIY%2FmDho%3DtFFVqf72YFHLITsfHLQRoaz3oriVxuqTJyvNE2firmJCoOhILt',
                'Cookie': 'guest_id=v1%3A161445177275078142; personalization_id="v1_0yiC0TN5IyWVExTm/BFPuw=="'
            }
        };

        request(options, function (error, response) {
            if (error) throw new Error(error);
            //console.log(response.body);

            res.setHeader('Access-Control-Allow-Origin', '*');
            res.writeHead(200, { 'Content-Type': 'application/json' });

            // set response content    
            res.write(response.body);
            res.end();
        });
    } else if (req.url.includes('trendsbyid/')) {
        console.log('trendsbyid/');
        var id = req.url.split('/')[2];

        var options = {
            'method': 'GET',
            'url': 'https://api.twitter.com/1.1/trends/place.json?id=' + id,
            'headers': {
                'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAKbHNAEAAAAA%2B8gitwwlUp0Vbkfq%2FjtBIY%2FmDho%3DtFFVqf72YFHLITsfHLQRoaz3oriVxuqTJyvNE2firmJCoOhILt',
                'Cookie': 'guest_id=v1%3A161445177275078142; personalization_id="v1_0yiC0TN5IyWVExTm/BFPuw=="'
            }
        };
        request(options, function (error, response) {
            if (error) throw new Error(error);
            //console.log(response.body);
            //Set header 
            res.setHeader('Access-Control-Allow-Origin', '*');
            res.writeHead(200, { 'Content-Type': 'application/json' });

            res.write(response.body);

            res.end();
        });
    } else if (req.url.includes("tweets/search/")) {
        const queryObject = url.parse(req.url, true).query;
        console.log(queryObject);
        var queryString = stringify(queryObject);
        console.log(queryString);

        var request = require('request');
        var options = {
            'method': 'GET',
            'url': 'https://api.twitter.com/2/tweets/search/recent?' + queryString,
            'headers': {
                'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAKbHNAEAAAAA%2B8gitwwlUp0Vbkfq%2FjtBIY%2FmDho%3DtFFVqf72YFHLITsfHLQRoaz3oriVxuqTJyvNE2firmJCoOhILt',
                'Cookie': 'guest_id=v1%3A163268461359551176; personalization_id="v1_vMlVuQFW5L5zKKQrt4yPsw=="'
            }
        };
        request(options, function (error, response) {
            if (error) throw new Error(error);
            res.setHeader('Access-Control-Allow-Origin', '*');
            res.writeHead(200, { 'Content-Type': 'application/json' });

            res.write(response.body);

            res.end();
        });

    }
});

server.listen(5000); //3 - listen for any incoming requests

console.log('Node.js web server at port 5000 is running..')


