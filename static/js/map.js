"use strict";

var map;
var centerSF = {lat: 37.7749, lng: -122.4194}; 
var markers = [];


function initAutocomplete() {
  // Instantiates map 
  map = new google.maps.Map(document.getElementById('map'), {
    center: centerSF,
    zoom: 12,
    mapTypeId: 'roadmap'
  });

  // Create search box and link it to the UI element.
  var input = document.getElementById('pac-input');
  var searchBox = new google.maps.places.SearchBox(input);
  
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

  // Bias the SearchBox results towards current map's viewport.
  map.addListener('bounds_changed', function() {
    searchBox.setBounds(map.getBounds());
  });

  // Setup primary marker and searches for events with markers
  setPrimaryMarker(map, searchBox, markers); //Have the searchBox listener here**** 
}

function setPrimaryMarker(map, searchBox, markers) {
  // Adds an event listener that autocompletes in searchBox, and retrieves
  // more details for that place.  

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
     
    // Searches for events and adds markers 
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

  // Exit out of function if no search results
  if (eventPlaces.length == 0) {
    return;
  }

  // Loop through each event in the eventPlaces array

  for (var i = 0; i < eventPlaces.length; i++) {

    var place = eventPlaces[i]; 
    var placeInfowindow = new google.maps.InfoWindow({
      content: 'Test content',
    });

    var eventMarker = new google.maps.Marker({
      map: map,
      title: place.name,
      position: place.position,
      infowindow: placeInfowindow,
    });

    console.log(eventMarker);
    markers.push(eventMarker);

    // console.log(markers);

    eventMarker.addListener('click', function() {
      hideAllInfoWindows(map, placeInfowindow);
      placeInfowindow.open(map, this); 
    });

    // Expand map boundaries to include event markers
    bounds.extend(place.position);    

    // Fit map to extended new boundary 
    map.fitBounds(bounds); 
  }

  listEventsOnPage(eventPlaces);

}

function hideAllInfoWindows(map, placeInfowindow) {
  markers.forEach(function(marker) {
    placeInfowindow.close(map, marker);
  });
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

// function addInfowindow(map, place) {
//   var contentString = '<div id="windowContent">' + 
//                       '<h3>' + place.name + '</h3>' +
//                       '<p>' + place.time + '</p>' + 
//                       '<p><a href="' + place.url + '">' + place.url + '</a></p>' + 
//                       '</div>';

//   new google.maps.InfoWindow({
//     content: contentString,
//     num: i
//   });

//   marker.addListener('click', function() {
//   infowindow.open(map, marker);
//   });

// }



// function saveEvent(place) {
//   $.get("/saved-event", )
// }


