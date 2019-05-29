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



$.ajax({
    url: '/stats/personal_injury',
    success: function (map_data_2) {
        for (var i = 0; i < map_data_2.length; i++) {
            var title_2 = "personal_injury";
            var selfIcon = L.divIcon({
                className: 'my-div-icon',
                iconSize: [50, 50],
            });
            var marker = L.marker(new L.LatLng(map_data_2[i].lat, map_data_2[i].lon), {
                title: title_2,
                icon: selfIcon
            }).setBouncingOptions({
                bounceHeight: 20,
                exclusive: true
            }).on('click', function () {
                this.bounce(3);
            }).addTo(markers);

            var content = title_2 + "</br>" + "Latitude:" + map_data_2[i].Latitude + "</br>" + "Longitude:" + map_data_2[i].Longitude;
            marker.bindPopup(content, {
                maxWidth: 600
            });

            markers.addLayer(marker);
            markerList.push(marker);

        }
    }
});


$.ajax({
    url: '/stats/property_damage',
    success: function (map_data_3) {
        for (var i = 0; i < map_data_3.length; i++) {
            var title_3 = "property_damage";
            var selfIcon = L.divIcon({
                className: 'my-div-icon',
                iconSize: [50, 50],
            });
            var marker = L.marker(new L.LatLng(map_data_3[i].lat, map_data_3[i].lon), {
                title: title_3,
                icon: selfIcon
            }).setBouncingOptions({
                bounceHeight: 20,
                exclusive: true
            }).on('click', function () {
                this.bounce(3);
            }).addTo(markers);

            var content = title_3 + "</br>" + "Latitude:" + map_data_3[i].Latitude + "</br>" + "Longitude:" + map_data_3[i].Longitude;
            marker.bindPopup(content, {
                maxWidth: 600
            });

            markers.addLayer(marker);
            markerList.push(marker);

        }


        $.ajax({
            url: '/stats/belts',
            success: function (map_data_5) {
                for (var i = 0; i < map_data_5.length; i++) {
                    var title_5 = "personal_injury";
                    var selfIcon = L.divIcon({
                        className: 'my-div-icon',
                        iconSize: [50, 50],
                    });
                    var marker = L.marker(new L.LatLng(map_data_5[i].lat, map_data_5[i].lon), {
                        title: title_5,
                        icon: selfIcon
                    }).setBouncingOptions({
                        bounceHeight: 20,
                        exclusive: true
                    }).on('click', function () {
                        this.bounce(3);
                    }).addTo(markers);

                    var content = title_5 + "</br>" + "Latitude:" + map_data_5[i].Latitude + "</br>" + "Longitude:" + map_data_5[i].Longitude;
                    marker.bindPopup(content, {
                        maxWidth: 600
                    });

                    markers.addLayer(marker);
                    markerList.push(marker);

                }
            }
        });


        controlSearch.on('search:locationfound', function (e) {
            if (e.layer._popup) {
                var index = markerList.map(function (e) {
                    return e.options.title;
                }).indexOf(e.text);
                var m = markerList[index];
                markers.zoomToShowLayer(m, function () {
                    m.openPopup();
                    m.bounce(3);
                });
            }
        });
        map.addControl(controlSearch);
        map.addLayer(markers);
        //Mini map
        lc = L.control.locate({
            position: 'topright',
            strings: {
                title: "Show me where I am, yo!",
                popup: "I am here"
            },
            drawCircle: true,
            showPopup: true
        }).addTo(map);

        // Zoom position
        L.control.zoom({
            position: 'topright'
        }).addTo(map);
    }
});
