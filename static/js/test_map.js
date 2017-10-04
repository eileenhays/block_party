var map;
var defLocation = {lat: 37.7893921, lng: -122.4099426}; 
// var eventList = $.get('/data/score', function(data){
//     $('#my_score').html(data['score']);
// });

// Instantiate map
// function initMap() {
//   map = new google.maps.Map(document.getElementById('map'), {
//     center: defLocation,
//     zoom: 13,
//   });

//   // Create a marker for address
//   var marker = new google.maps.Marker({
//     position: defLocation,
//     map: map
//   });
// }

// Add a search box for map that uses Autocomplete. Uses Places library. 

function initAutocomplete() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: defLocation,
    zoom: 13,
    mapTypeId: 'roadmap'
  });

  // Create the search box and link it to the UI element.
  var input = document.getElementById('pac-input');
  var searchBox = new google.maps.places.SearchBox(input);
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

  // Bias the SearchBox results towards current map's viewport.
  map.addListener('bounds_changed', function() {
    searchBox.setBounds(map.getBounds());
  });

  var markers = [];
  // Listen for the event fired when the user selects a prediction and retrieve
  // more details for that place. Autocomplete object. 
  searchBox.addListener('places_changed', function() {
    var places = searchBox.getPlaces();
    console.log(places);
    window.places = places;

    if (places.length == 0) {
      return;
    }

    $.get('/search-events', clearAndSetNewMarkers); 

  }
  
  function clearAndSetNewMarkers() {
    // Clear out the old markers.
    markers.forEach(function(marker) {
      marker.setMap(null);
    });
    markers = [];

    // For each place, get the icon, name and location.
    // bounds biases toward results in the area specified; 
    // strictBounds completely restrict results to area specified

    var bounds = new google.maps.LatLngBounds();
    places.forEach(function(place) {
      if (!place.geometry) {
        console.log("Returned place contains no geometry");
        return;
      }
      var icon = {
        url: place.icon,
        size: new google.maps.Size(71, 71),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34),
        scaledSize: new google.maps.Size(25, 25)
      };

      // Create a marker for each place.
      markers.push(new google.maps.Marker({
        map: map,
        icon: icon,
        title: place.name,
        position: place.geometry.location
      }));

      if (place.geometry.viewport) {
        // Only geocodes have viewport.
        bounds.union(place.geometry.viewport);
      } else {
        bounds.extend(place.geometry.location);
      }
    });
    map.fitBounds(bounds);
  }  

  // showEventLocations(eventList);
}

// function showEventLocations(eventList) {
//   myMarkers = []
//   for event in eventList {
//     newMarker = myMarkers.push(new google.maps.Market({
//       map: map,
//       icon: icon,
//       title: event.name,
//       position: {event.latitude, event.longitude}
//     }));
//   };
// }












