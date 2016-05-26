//var coordsDiv = $("#coordinates"); //not sure that this is necessary

$(document).ready(function() {
    //$('#startButton').on('click', getLocation);

    $('#startButton').click(function() {
        $(".jumbotron").hide("slow", function(){
            $("#mask").hide();
            getLocation();
        })

    });
        //event handlers
    //make jumbotron and opaque mask disappear
    $( ".jumbotron" ).click(function() {
        $( ".jumbotron" ).hide( "slow", function() {
        //alert( "Animation complete." );
        });
    });
    //$("#startButton").click(function() {
    //    $("#mask").hide("slow")
    //});

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
        var acc = position.coords.accuracy
        L.marker([lat, lon]).addTo(map)
            .bindPopup('Your position is: Lat: '+lat +'<br>Lon: ' + lon + '<br>Give or take: '+ acc + ' meters.');
        map.setView(new L.LatLng(lat, lon),17);
        $.ajax({
            success: getWelikiaBlock(position)
        });
    }

    function getWelikiaBlock(position) {
        var lat = position.coords.latitude;
	    var lon = position.coords.longitude;
        $.ajax({
            url: "http://mannahatta2409.org/api/blocks/?lat=" + lat + "&lon=" + lon,
            dataType: 'jsonp',
            success: function(data){
                var blockGeom = data["features"][0]["geometry"];
                var style = {
                    "color": "#ff7800",
                    "weight": 3
                };
                L.geoJson(blockGeom, {
                    style: style
                })
                    .setZIndex(-1)
                    .addTo(map);
                getCensusBlock(position);
                cartoLayers(blockGeom);
            }
        });
    }

    function getCensusBlock(position){
	    var lat = position.coords.latitude;
	    var lon = position.coords.longitude;
	    //getting the FIPS code for the block
	    $.ajax({
		    url: "http://www.broadbandmap.gov/broadbandmap/census/block?latitude=" + lat + "&longitude=" + lon + "&format=jsonp",
		    dataType: 'jsonp',
		    success: getBlockData,
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
 		    url: "http://api.census.gov/data/2010/sf1?get=P0010001,H00010001&for=block:" + cblock + "&in=state:" + state + "+county:" + county + "+tract:" + ctract + "&key=c578327f5fb8e40e00fa608cdd7230781a8d2e00",
            dataType: 'jsonp',
            jsonp: 'jsonp',
            cache: true,
 		    //success: makeTable,
            success: function() {
                console.log("success")
                //makeTable(data);
            },

            error: function (jqXHR, textStatus, errorThrown) {
			    console.log("Error returning census data:" + "\n" + textStatus + "\n" + errorThrown)
            }
	    });
    }

    //dataTable
    //function makeTable(data){
    //    //var dataString = JSON.parse(data, true, ' ');
    //    $('#dataTable').dataTable({
    //        "ajax": function (data, callback, settings){
    //            callback(
    //                JSON.stringify(data)
    //            )
    //        },
    //        "columns": [
    //            {"title": "Population"},
    //            {"title": "# Households"},
    //
    //            {"title": "State"}
    //        ],
    //        "sAjaxDataProp": "data.inner"
    //    });
    //}

    //make map

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
    var toner = new L.TileLayer(toner_url, {
        maxZoom: 18,
        attribution: attribution,
        subdomains: subdomains
    });

    // Add basemap
    map.addLayer(toner);

    //add geoserver tile layer
    contourLayer = new L.tileLayer.wms('http://localhost:8080/geoserver/ows?service=wms', {
        layers: 'cite:allCity_contour_5m',
        format: 'image/png',
        transparent: true,
        version: '1.1.0',
        minZoom: 14,
        maxZoom: 17
    });
    map.addLayer(contourLayer);

    fpLayer = new L.tileLayer.wms('http://localhost:8080/geoserver/ows?service=wms', {
        layers: 'cite:allcity2409vfin_attributed',
        format: 'image/png',
        transparent: true,
        version: '1.1.0',
        minZoom: 15
    });
    map.addLayer(fpLayer);

    //add cartodb data
    function cartoLayers(blockGeom){
        var sql = new cartodb.SQL({user: 'mariogiampieri'});
        cartodb.createLayer(map, 'https://mariogiampieri.cartodb.com/api/v2/viz/38c0a5be-fbe3-11e4-9182-0e9d821ea90d/viz.json')
        .addTo(map)
        .done(function(layer){
                layer.getSubLayer(0).infowindow.set({
                    //offset: [-620,-350]
                });
                console.log(layer.rows);
                })
        }
});


// //make a table in the info window for the data to appear in: https://www.datatables.net/