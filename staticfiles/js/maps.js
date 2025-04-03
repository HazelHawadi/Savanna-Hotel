async function initMap() {
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement, PinElement } = await google.maps.importLibrary("marker");

  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 12,
    center: { lat: 52.2712, lng: -9.6909 }, // Tralee Town Centre
    mapId: "DEMO_MAP_ID",
  });

  var labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

  var locations = [
    { lat: 40.785091, lng: -73.968285 },
    { lat: 41.084045, lng: -73.874245 },
    { lat: 40.754932, lng: -73.984016 },
  ];

  const markers = locations.map((position, i) => {
    const label = labels[i % labels.length];
    const pinGlyph = new google.maps.marker.PinElement({
      glyph: label,
      glyphColor: "white",
    });

    const marker = new google.maps.marker.AdvancedMarkerElement({
      position,
      content: pinGlyph.element,
    });

    // Open info window when marker is clicked
    marker.addListener("click", () => {
      const infoWindow = new google.maps.InfoWindow({
        content: `Coordinates: ${position.lat}, ${position.lng}`,
      });
      infoWindow.open(map, marker);
    });

    return marker;
  });

  new markerClusterer.MarkerClusterer({ markers, map });
}

initMap();
