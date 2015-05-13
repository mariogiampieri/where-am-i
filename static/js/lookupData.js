//var coordsDiv = $("#coordinates"); //not sure that this is necessary
$(document).ready(function() {
    var map = new L.Map("map-container",
                {   center:[40.75, -73.95], //change to users given location
                    zoom: 12
                });
            // Credit where credit is due
    var attribution = 'Map tiles by <a href="http://maps.stamen.com/">Stamen</a>';

            // This allows concurent calls (faster tile loading)
    var subdomains = ['a', 'b', 'c', 'd'];

            // Change this url to use different set of map tiles
    var toner_url = 'http://{s}.tile.stamen.com/toner/{z}/{x}/{y}.png';

            // Let's add the 'terrain' layer
    toner = new L.TileLayer(toner_url, {
        maxZoom: 18,
        attribution: attribution,
        subdomains: subdomains
    });

    // Add it to the map
    map.addLayer(toner);
    L.marker([40.75, -73.95]).addTo(map)
        .bindPopup('This is a popup.');
    $( ".jumbotron" ).click(function() {
        $( ".jumbotron" ).hide( "slow", function() {
        //alert( "Animation complete." );
        });
    });
});

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showLocation);
    } else {
        coordsDiv.html("Geolocation is not supported by this browser.");
    }
}

    function showLocation(position) {
        var lat = position.coords.latitude;
	    var lon = position.coords.longitude;
        //L.marker([lat, lon]).addTo(map);
        $.ajax({
            success: getCensusBlock(position)
        });
    }

    function getCensusBlock(position){
	    var lat = position.coords.latitude;
	    var lon = position.coords.longitude;
	    //getting the FIPS code for the block
	    $.ajax({
		    url: "http://www.broadbandmap.gov/broadbandmap/census/block?latitude=" + lat + "&longitude=" + lon + "&format=jsonp",
		    dataType: 'jsonp',
		    success: getBlockData, //return this to standard success message to verify data is being returned, then worry about accessing fips code for next function
		    error: function (jqXHR, textStatus, errorThrown) {
			    console.log("Error loading data for block:" + "\n" + textStatus + "\n" + errorThrown)
		    }
	    });
    }

    function getBlockData(data, textStatus, jqHXR) {
 	    var fips = data["Results"]["block"][0]["FIPS"];
 	    var state = fips.slice(0,2);
        var county = fips.slice(2,5);
        var ctract = fips.slice(5,11);
        var cblock = fips.slice(11);
 	    $.ajax({
 		    url: "http://api.census.gov/data/2010/sf1?get=P0010001&for=block:" + cblock + "&in=state:" + state + "+county:" + county + "+tract:" + ctract + "&key=c578327f5fb8e40e00fa608cdd7230781a8d2e00",
            dataType: 'jsonp',
            jsonp: 'jsonp',
            cache: true,
 		    success: function(jqHXR, textStatus){
                console.log("Success")
            },
 		    // censusResponse(),
            error: function (jqXHR, textStatus, errorThrown) {
			    console.log("Error returning census data:" + "\n" + textStatus + "\n" + errorThrown)
            }
	    });
    }

    function censusResponse(data, textStatus, jqHXR) {
        var censusData = data;
        console.log("Success")
    }

//to do: link to cartodb.js: http://docs.cartodb.com/cartodb-platform/cartodb-js.html#api-methods
//make a table in the info window for the data to appear in: https://www.datatables.net/
//^^ both of the above already have the necessary links and style in index.html