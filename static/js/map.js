var map;
var defaultLocation = {lat: 37.7893921, lng: -122.4099426}; 
var markers = [];


// Add a search box for map that uses Autocomplete. Uses Places library. 

function initAutocomplete() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: defaultLocation,
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

  setPrimaryMarker(map, searchBox); //I want to reset this whenever someone enters the new address

}

function setPrimaryMarker(map, searchBox) {
  // var markers = [];

  // Listen for the event fired when the user selects a prediction and retrieve
  // more details for that place. Autocomplete object. 
  searchBox.addListener('places_changed', function() {
    var places = searchBox.getPlaces();
    
    if (places.length == 0) {
      return;
    }
    else if (places.length > 1) {
      return console.log("Please search for one address"); //have it flash a message
    }

    clearOldMarkers(markers);
    
    console.log(places);
    // window.places = places; //creates places global variable

    var bounds = new google.maps.LatLngBounds();
    
    places.forEach(function(place) {
      if (!place.geometry) {
        console.log("Returned place contains no geometry");
        return;
      }

      // Set primary address
      var primaryIcon = {
        url: "/static/images/star_icon.svg",
        size: new google.maps.Size(71, 71),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34),
        scaledSize: new google.maps.Size(25, 25)
      };

      // Create a marker for the primary address
      markers.push(new google.maps.Marker({
        map: map,
        icon: primaryIcon,
        title: place.name,
        position: place.geometry.location
        })
      );
      
      if (place.geometry.viewport) {
      // Only geocodes have viewport.
        bounds.union(place.geometry.viewport);
      } else {
        bounds.extend(place.geometry.location);
      }
    });

    map.fitBounds(bounds);
     
    searchWithPrimaryLocation(places);

  });
}

// function test(result) {
//   console.log(result);
// }

function searchWithPrimaryLocation(places) {
  // User input primary location to search for local events.

  var primaryLocation = {};

  primaryLocation["name"] = places[0].name;
  primaryLocation["lat"] = places[0].geometry.location.lat();
  primaryLocation["lng"] = places[0].geometry.location.lng();            

  console.log(primaryLocation);


  $.get("/search-events", Object.values(primaryLocation), function(result) {
    clearAndSetMarkers(result, map);
    });
              // function(error) {
              //   console.log(error);
              // },
 }

function clearAndSetMarkers(data, map) {
  var eventPlaces = Object.values(data);
  console.log("This is the eventPlaces object");
  console.log(eventPlaces);

  if (eventPlaces.length == 0) {
    return;
  }

  // For each place, get the icon, name and location.
  var newBounds = new google.maps.LatLngBounds();

  eventPlaces.forEach(function(place) {
    console.log(place.position);

    // if (!place.geometry) {
    //   console.log("Returned event place contains no geometry");
    //   return;
    // }

    // Create a marker for each event place.
    markers.push(new google.maps.Marker({
      map: map,
      title: place.name,
      position: place.position
      })
    );

    console.log(markers);

    // if (place.geometry.viewport) {
    //   newBounds.union(place.geometry.viewport);
    // } else {
    //   newBounds.extend(place.geometry.location);
    // }
  });
  // map.fitBounds(newBounds);
}

function clearOldMarkers(markers) {
      // Clear out the old event markers.
    markers.forEach(function(marker) {
      markers.setMap(null);
    });
    markers = [];
}

