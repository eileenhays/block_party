var map;
var defaultLocation = {lat: 37.7893921, lng: -122.4099426}; 


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

    setPrimaryMarker(map, searchBox);
    
  // Listen for the event fired when the user selects a prediction and retrieve
  // more details for that place. Autocomplete object. 

}

function setPrimaryMarker(map, searchBox) {
  var markers = [];

  searchBox.addListener('places_changed', function() {
    var places = searchBox.getPlaces();
    
    if (places.length == 0) {
      return;
    }
    else if (places.length > 1) {
      return console.log("Please search for one address");
    }

    // Clear out the old event markers.
    markers.forEach(function(marker) {
      markers.setMap(null);
    });
    markers = [];
    
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


function clearAndSetMarkers(data, map) {
  console.log(data);
  // // Clear out the old event markers.
  // eventPlaces.forEach(function(marker) {
  //   eventPlaces.setMap(null);
  // });
  // eventPlaces = [];
  var eventPlaces = [];

  // For each place, get the icon, name and location.
  // bounds biases toward results in the area specified; 
  // strictBounds completely restrict results to area specified

  eventPlaces.push(data);
  // window.eventPlaces = eventPlaces; //creates eventPlaces global variable

  eventPlaces.forEach(function(place) {
    console.log(place);
    // var eventIcon = {
    //   url: "http://maps.google.com/mapfiles/marker.png",
    //   size: new google.maps.Size(71, 71),
    //   origin: new google.maps.Point(0, 0),
    //   anchor: new google.maps.Point(17, 34),
    //   scaledSize: new google.maps.Size(25, 25),
    // };

    // Create a marker for each place.
    eventPlaces.push(new google.maps.Marker({
      map: map,
      // icon: eventIcon,
      title: place.name,
      position: place.position
    }));
  });
}

function searchWithPrimaryLocation(places) {
  // User input primary location to search for local events.

  var obj = {};

  obj["name"] = places[0].name
  obj["lat"] = places[0].geometry.location.lat();
  obj["lng"] = places[0].geometry.location.lng();            

  console.log(obj);

  $.get("/search-events", obj, 
    function(result) {
      clearAndSetMarkers(result, map);
    }, function(error) {
      console.log(error);
    }
  );
    //callback from the result and error
}












