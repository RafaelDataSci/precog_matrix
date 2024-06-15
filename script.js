mapboxgl.accessToken = 'MAPBOX_TOKEN';

const map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/streets-v11',
  center: [-79.347015, 43.651070], // Toronto coordinates
  zoom: 12
});

const geocoder = new MapboxGeocoder({
  accessToken: mapboxgl.accessToken,
  mapboxgl: mapboxgl
});

document.getElementById('address').appendChild(geocoder.onAdd(map));

geocoder.on('result', function(e) {
  const lat = e.result.center[1];
  const lon = e.result.center[0];
  document.getElementById('address_latitude').value = lat;
  document.getElementById('address_longitude').value = lon;
});

flatpickr("#address_datetime", {
  enableTime: true,
  dateFormat: "Y-m-d H:i",
});

map.on('click', function(e) {
  const lat = e.lngLat.lat;
  const lon = e.lngLat.lng;
  document.getElementById('address_latitude').value = lat;
  document.getElementById('address_longitude').value = lon;

  // Reverse geocode to get the address
  fetch(`https://api.mapbox.com/geocoding/v5/mapbox.places/${lon},${lat}.json?access_token=${mapboxgl.accessToken}`)
    .then(response => response.json())
    .then(data => {
      const place = data.features[0].place_name;
      document.getElementById('address').innerText = place;
    });
});

$('#crime-form').on('submit', function(event) {
  event.preventDefault();

  const address = $('#address').text().trim();
  const latitude = $('#address_latitude').val();
  const longitude = $('#address_longitude').val();
  const datetime = $('#address_datetime').val();

  $.ajax({
    url: `http://localhost:8000/predict?address=${address}&crime_date=${datetime}`,
    method: 'GET',
    success: function(data) {
      $('#predicted-crimes').text(`Predicted Crimes: ${data.prediction}`);
      $('#crime').removeClass('d-none');
    },
    error: function(error) {
      alert('Error fetching prediction: ' + error.responseJSON.error);
    }
  });
});
