/**
 * Created by Mario on 5/3/15.
 */

var coordsDiv = $("#coordinates");

var getLocation = function() {
    if (navigator.geolocation) { navigator.geolocation.getCurrentPosition(getCensusBlock); 
    } else {
    coordsDiv.html("Geolocation is not supported by this browser.") 
    }
}

var getCensusBlock = function(position) {
    var lat = position.coords.latitude;
    var lon = position.coords.longitude;
    coordsDiv.html("Latitude:" + lat + "<br>Longitude:" + lon);

    //get FIPS code for block
    $.ajax({
        url: "http://www.broadbandmap.gov/broadbandmap/census/block?latitude=" + lat + "&longitude=" + lon + "&format=jsonp",
        dataType: "jsonp",
        success: getBlockData,
        error: function(jqHXR, textStatus, errorThrown) {
            console.log("Error loading data for block:" + textStatus + errorThrown)
        }
    })
}

var getBlockData = function(data, textStatus, jqHXR) {
    var fips = data["Results"]["block"][0]["FIPS"];
    var state = fips.slice(0,1);
    var county = fips.slice(2,4);
     var ctract = fips.slice(5,10); 
    var cblock = fips.slice(11,15);
    $.ajax({
        url: "http://api.census.gov/data/2010/sf1?get=P0010001,P0030001&for=block:" + cblock + "&in=state:" + state + "+county:" + county + "+tract:" + ctract + "&key=c578327f5fb8e40e00fa608cdd7230781a8d2e00",
        data: data,
        dataType: 'jsonp',
        success: function() {
            console.log("Success")
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.log("Error returning census data: " + errorThrown)
        }
    })
}

var buildTable = function(getBlockData) {
    var pop = data["Results"] //build this out to include the field position of the population data
    //copy the above var x = data[] position for other relevant returned data, from the tables specified
    $(document).ready(function) {
        $('#responseTable').dataTable({
            "ajax": "data.json"
        })
    }
}