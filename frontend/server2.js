const express = require('express')
const app = express()
const port = 3000

app.get('/', (req, res) => {
    console.log('teste')
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
        res.send('Hello World!')
    });


})

app.listen(port, () => {
    console.log(`Example app listening at http://localhost:${port}`)
})