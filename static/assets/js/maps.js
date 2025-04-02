function initMap() {
  var map = new google.maps.Map(document.getElementById("map"), {
    zoom: 12,
    center: {
      lat: 52.2712,
      lng: -9.6909,
    },
  });

  var labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

  var locations = [
    { lat: 52.2712, lng: -9.6909 }, // Tralee Town Centre
  ];

  // Create markers for each location
  var markers = locations.map(function (location, i) {
    return new google.maps.Marker({
      position: location,
      label: labels[i % labels.length],
    });
  });

  // Cluster the markers on the map
  var markerCluster = new MarkerClusterer(map, markers, {
    imagePath:
      "https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m",
  });
}
