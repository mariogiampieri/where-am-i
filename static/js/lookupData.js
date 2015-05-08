var coordsDiv = $("#coordinates");
var leafMap = $("#map-container");

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(getCensusBlock);
    } else {
        coordsDiv.html("Geolocation is not supported by this browser.");
    }
}

function getCensusBlock(position){
	var lat = position.coords.latitude;
	var lon = position.coords.longitude;
    coordsDiv.html("Latitude: " + lat + "<br>Longitude: " + lon);
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

var map = L.map(leafMap).setView([51.505, -0.09], 13); //figure out how put user location onto map- remember, L.map() originally contained "map". figure out how to put marker on map in index.html

// keep getting cors errors with this, tried setting jQuery.support.cors = true;, specifying ajax datatype to 'jsonp',
// and '&jsonp=getBlockData' to the end of the census api request will follow tutorial at http://www.html5rocks.com/en/tutorials/cors/
function getBlockData(data, textStatus, jqHXR) {
 	var fips = data["Results"]["block"][0]["FIPS"]; //need to split json response into parts to plug in parts to census api (state, county, etc, etc, block)
 	var state = fips.slice(0,1);
    var county = fips.slice(2,4);
    var ctract = fips.slice(5,10);
    var cblock = fips.slice(11,15);
 	$.ajax({
 		url: "http://api.census.gov/data/2010/sf1?get=P0010001&for=block:" + cblock + "&in=state:" + state + "+county:" + county + "+tract:" + ctract + "&key=c578327f5fb8e40e00fa608cdd7230781a8d2e00", // + "&jsonp=censusResponse", //<-- &jsonp=function_name(name of next function?)"//plug in the fips lookup url here
        dataType: 'jsonp', //try above query string at the state, county, censustract levels to make absolutely sure the string is correct. try in browser and then in application.
        jsonp: 'jsonp',
        cache: false,
        //jsonpCallback: 'censusResponse',
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

////the makings of a datatable
//$(document).ready(function() {
//    $('#responseTable').DataTable( {
//        "ajax": "data.json"
//    });
//})