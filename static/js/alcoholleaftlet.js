// Creating map object
var map = L.map("map", {
    center: [38.897621, -77.036573],
    zoom: 8
});

// Adding tile layer to the map
var lightmap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 18,
    id: "mapbox.streets",
    accessToken: "pk.eyJ1IjoiY3lwb2xvIiwiYSI6ImNqdzQ4aTkxMjB2Nzc0NHBjM2E2YTZqeGoifQ.QQqO36MCcG6cjQHtLWwEhw"
}).addTo(map);



var markers = L.markerClusterGroup();
var markerList = [];
var controlSearch = new L.Control.Search({
    position: 'topright',
    layer: markers,
    initial: false,
    zoom: 18,
    marker: false
});


$.ajax({
    url: '/stats/alcohol',
    success: function (map_data_1) {
        for (var i = 0; i < map_data_1.length; i++) {
            var title_1 = "alcohol";
            var selfIcon = L.divIcon({
                className: 'my-div-icon',
                iconSize: [50, 50],
            });
            var marker = L.marker(new L.LatLng(map_data_1[i].lat, map_data_1[i].lon), {
                title: title_1,
                icon: selfIcon
            }).setBouncingOptions({
                bounceHeight: 20,
                exclusive: true
            }).on('click', function () {
                this.bounce(3);
            }).addTo(markers);

            var content = title_1 + "</br>" + "Latitude:" + map_data_1[i].Latitude + "</br>" + "Longitude:" + map_data_1[i].Longitude;
            marker.bindPopup(content, {
                maxWidth: 600
            });

            markers.addLayer(marker);
            markerList.push(marker);

        }
    }
});