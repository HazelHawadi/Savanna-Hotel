function initMap() {
  console.log("Initializing map...");

  try {
    const map = new google.maps.Map(document.getElementById("map"), {
      zoom: 12,
      center: { lat: 52.2712, lng: -9.6909 }, // Tralee Town Centre
      mapId: "2c53aa66b5ee8784",
    });

    const locations = [
      { lat: 40.785091, lng: -73.968285 },
      { lat: 41.084045, lng: -73.874245 },
      { lat: 40.754932, lng: -73.984016 },
    ];

    const labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

    locations.forEach((position, i) => {
      new google.maps.Marker({
        position,
        map,
        label: labels[i % labels.length],
      });
    });

    console.log("Map loaded successfully!");
  } catch (error) {
    console.error("Error loading Google Maps:", error);
  }
}

window.initMap = initMap;
