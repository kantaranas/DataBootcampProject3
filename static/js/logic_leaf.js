// Creating map object
var myMap = L.map("map", {
  center: [40.731003, -74.065888],
  zoom: 11
});

// Adding tile layer to the map
L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.streets",
  accessToken: API_KEY
}).addTo(myMap);


d3.queue()
.defer(
  d3.json,("/metadata/chart/01/alcohol").(function(obj) {
      var markers = obj.data.map(function(response) {
          return L.marker([response.lat, response.lon]);
  })

  // Loop through data
  for (var i = 0; i < 100; i++) {

      // Add a new marker to the cluster group and bind a pop-up
      markers.addLayer(L.marker([response.lat, response.response])
        .bindPopup(response.state));
    }

  // Add our marker cluster layer to the map
  myMap.addLayer(markers);

})
renderData()