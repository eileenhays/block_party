"use strict";

var map;
var centerSF = {lat: 37.7749, lng: -122.4194}; 


// Add a search box for map that uses Autocomplete. Uses Places library. 

function initAutocomplete() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: centerSF,
    zoom: 12,
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

  // Sets up primary marker and searches for events with markers
  setPrimaryMarker(map, searchBox); //Have the searchBox listener here**** 
}

function setPrimaryMarker(map, searchBox) {
  // Listen for the event fired when the user selects a prediction and retrieve
  // more details for that place. Autocomplete object. 
  var markers = [];
  window.markers = markers; 

  searchBox.addListener('places_changed', function() {
    var places = searchBox.getPlaces();
    
    if (places.length == 0) {
      console.log("That location does not exist") //flash msg
      return;
    }
    else if (places.length > 1) {
      console.log("Requires a single address to search"); //flash msg
      return;
    }

    clearOldMarkers(markers); //I think this only needs to live here if searchBox changes 
    
    console.log(places);

    var bounds = new google.maps.LatLngBounds();
    window.bounds = bounds
    
    places.forEach(function(place) {
      if (!place.geometry) {
        console.log("Returned place contains no geometry");
        return;
      }

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


function searchWithPrimaryLocation(places) {
  // User input primary location to search for local events.

  var obj = {};

  obj["name"] = places[0].name;
  obj["lat"] = places[0].geometry.location.lat();
  obj["lng"] = places[0].geometry.location.lng();            

  console.log(obj);

  // AJAX call to server to search local events with provided address
  $.ajax({url: "/search-events", 
          data: obj, 
          success: function(result) {
            setEventMarkers(result, map);
          },
          error: function(error) {
            console.log(error);
          }});
 }


function setEventMarkers(data, map) {
  // Event places data from server
  var eventPlaces = Object.values(data);
  window.eventPlaces = eventPlaces;

  // No search results will exit out of function
  if (eventPlaces.length == 0) {
    return;
  }

  // Loop through each event in the eventPlaces array
  eventPlaces.forEach(function(place) {
    console.log(place.position);

    if (!place.position) {
      console.log("Returned event place contains no geometry");
      return;
    }

    // Create a marker for each event place.
    var eventMarker = new google.maps.Marker({
                      map: map,
                      title: place.name,
                      position: place.position
                      });

    // Add marker to map 
    markers.push(eventMarker);

    console.log(markers);

    // Where I would add an event listener for my marker info windows
    addInfowindow(markers, map)
    // Expand map boundaries to include event markers
    bounds.extend(place.position)
    // addInfoWindow(marker, map)    
  });

  // Fit map to extended new boundary 
  map.fitBounds(bounds);

  listEventsOnPage(eventPlaces);

}

function clearOldMarkers(markers) {
    // Clear out the old event markers.
    markers.forEach(function(marker) {
      markers.setMap(null);
    });
    markers = [];
}

function listEventsOnPage(eventPlaces) {
  var eventList = document.getElementById('events_list');

  var contentText = JSON.stringify(eventPlaces);

  eventList.innerHTML = contentText;
}

function addInfowindow(markers, map) {
  var contentString = '<div id="windowContent">' + 
                      '<h3>Event</h3>' +
                      '<p>This is where event info goes.</p>' + 
                      '</div>';

  var i = 0; //need to increment this

  markers.forEach(function(marker) {
    var infowindow = new google.maps.InfoWindow({
      content: contentString,
      num: i
    });

    marker.addListener('click', function() {
    infowindow.open(map, marker);
    });
  });

}

// function saveEvent(place) {
//   $.get("/saved-event", )
// }


