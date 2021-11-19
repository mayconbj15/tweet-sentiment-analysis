var cities = {}

var loaded = false

var quantOfTweetsInTrain = 10

window.onload = async function () {
    await LoadEvents().then(() => console.log("then"));
    await GetTrendsAvaliable().then(() => {
        document.getElementById('cities-spinner').className = 'd-none spinner-border';
        document.getElementById('cities-trending').className = 'row ';
    });

    LoadBrazilTrendings();
}

async function LoadEvents() {
    console.log('Loading events')
    var dropdowns = document.getElementsByClassName('dropdown-item')
    for (var i = 0; i < dropdowns.length; i++) {
        dropdowns[i].addEventListener("click", function (event) {
            LoadTrendingTable(event.target.textContent)
        }, false);
    }

    return true;
}

async function LoadBrazilTrendings() {
    console.log("LoadBrazilTrendings")
    var city = "Brazil";
    var tweetsOfTrends = GetTweetsOfTrends(city, 3);

    RenderCityTrendTable(city, tweetsOfTrends, "trend-table-brazil");
}

//Api module
async function GetTrendsAvaliable() {
    console.log('GetTrendsAvaliable')

    var settings = {
        "url": "http://localhost:5000/trends/avaliable",
        "method": "GET",
        "timeout": 0,
        "async": false
    };

    $.ajax(settings).done(function (response) {
        response.forEach(element => {
            cities[element["name"]] = element["woeid"]
        });
    });

    console.log(cities);
    loaded = true;
}

//Trending Topic Tables
function LoadTrendingTable(city) {
    var tweetsOfTrends = GetTweetsOfTrends(city, 3);

    RenderCityTrendTable(city, tweetsOfTrends, "trend-table", "trending-title");
}

function GetTweetsOfTrends(city, quant) {
    console.log(`city: ${city}`)
    var trends = GetTrendsOfCity(city, quant);
    var tweetsOfTrends = GetTweetsOfTrendsFromApi(trends, quantOfTweetsInTrain);
    var tweetsOfTrends = GetTweetsSentiments(tweetsOfTrends);

    return tweetsOfTrends;
}

function GetTweetsOfTrendsFromApi(trends, quant) {
    console.log('GetTweetsOfTrendsFromApi')
    var tweetsOfTrends = {};
    trends.forEach(element => {
        var tweetsList = []
        for (var i = 0; i < quantOfTweetsInTrain; i += 100) {
            var tweets = GetTweetsByQuery(element["query"], 100);
            tweetsList = tweetsList.concat(tweets["data"])
        }

        tweetsOfTrends[element["name"]] = { "data": tweetsList, "sentiment": null, "tweet_volume": element["tweet_volume"] };

    });
    Object.keys(tweetsOfTrends).forEach(k => tweetsOfTrends[k]["data"] = tweetsOfTrends[k]["data"].filter(t => t["lang"] == "pt"));

    return tweetsOfTrends;
}

function GetTrendsOfCity(cityName, quant) {
    console.log('GetTrendsOfCity')
    var cityId = cities[cityName]
    var trends = GetTrendsById(cityId);
    trends.sort(function (a, b) {
        return b["tweet_volume"] - a["tweet_volume"]
    })

    console.log('log: trends');
    console.log(trends);
    return trends.slice(0, quant);
}

function GetTrendsById(cityId, quantTrend) {
    console.log('GetTrendsAvaliable')

    var settings = {
        "url": "http://localhost:5000/trendsbyid/" + cityId,
        "method": "GET",
        "timeout": 0,
        "async": false
    };

    var trends = []
    $.ajax(settings).done(function (response) {
        response[0]["trends"].forEach(element => {
            trends.push(element)
        });
    });

    return trends.filter((t) => t["tweet_volume"] != null);
}

function GetTweetsSentiments(tweetsOfTrends) {
    console.log('GetTweetsSentiments')
    Object.keys(tweetsOfTrends).forEach(k => {
        tweets = []
        tweetsOfTrends[k]["data"].forEach(t => tweets.push(t["text"]))
        if (tweets.length > 0) {
            var settings = {
                "url": `http://localhost:5001/tweets/sentiments?Trend=${k}`,
                "method": "POST",
                "timeout": 0,
                "async": false,
                "headers": {
                    "Content-Type": "text/plain"
                },
                "data": JSON.stringify({
                    "data": tweets
                }),
            };

            var tweetsSentiments = {};
            $.ajax(settings).done(function (response) {
                console.log(response);
                console.log('response');
                tweetsSentiments = response;
            });

            var positive = 0;
            var negative = 0;
            var neutral = 0;
            tweetsSentiments["data"].forEach(element => {
                if (element["sentiment"] == 0) {
                    negative++;
                } else if (element["sentiment"] == 1) {
                    positive++;
                } else {
                    neutral++;
                }
            });

            //Regra para saber o sentimento do topico
            if (positive > negative && positive > neutral)
                tweetsOfTrends[k]["sentiment"] = 1
            else if (negative > positive && negative > neutral)
                tweetsOfTrends[k]["sentiment"] = 0
            else if (neutral > positive && neutral > negative)
                tweetsOfTrends[k]["sentiment"] = 2

            tweetsSentiments["group"] = SortDictionary(tweetsSentiments["group"])
            console.log(`Api response sentiments. Trend ${k}`)
            console.log(tweetsSentiments)
        }
    });


    return tweetsOfTrends;
}

function RenderCityTrendTable(city, tweetsOfTrends, id, titleId) {
    if (titleId != undefined) {
        var trendTitle = document.getElementById(titleId);
        if (trendTitle != undefined) {
            trendTitle.innerHTML = `<h3>Trending topics de ${city}</h3>`;
        }
    }

    var trendTable = document.getElementById(id);
    var html = `
        <table class="table table-striped table-dark center id="${id}"">
        <thead>
            <tr>
                <th scope="col">#</th>
                <th scope="col">Topico</th>
                <th scope="col">Nº de tweets</th>
                <th scope="col">Sentimento</th>
            </tr>
        </thead>
        <tbody>
    `;
    var i = 0;
    Object.keys(tweetsOfTrends).forEach(k => {
        i++;
        html += `
        <tr>
            <th scope="row">${i}</th>
            <td>${k}</td>
            <td>${tweetsOfTrends[k]["tweet_volume"]}</td>
            <td>${GetSentimentLabel(tweetsOfTrends[k]["sentiment"])}</td>
        </tr>
        `;
    })

    html += ` 
        </tbody>
    </table>`;

    trendTable.innerHTML = html;
    console.log(html);
}

function GetSentimentLabel(sentimentCode) {
    if (sentimentCode == "1") {
        return "Positivo";
    } else if (sentimentCode == "0") {
        return "Negativo";
    } else {
        return "Neutro";
    }
}

function GetTweetsByQuery(query, quant) {
    var settings = {
        "url": `http://localhost:5000/tweets/search/recent?max_results=${quant}&query=${query}&tweet.fields=lang`,
        "method": "GET",
        "timeout": 0,
        "async": false
    };

    var tweets = {}
    $.ajax(settings).done(function (response) {
        tweets = response;
    });

    return tweets;
}

function SortDictionary(obj) {
    items = Object.keys(obj).map(function (key) {
        return [key, obj[key]];
    });
    items.sort(function (first, second) {
        return second[1] - first[1];
    });
    sorted_obj = {}
    $.each(items, function (k, v) {
        use_key = v[0]
        use_value = v[1]
        sorted_obj[use_key] = use_value
    })
    return (sorted_obj)
}


