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

  // var input;
  // // if localStorage has something saved in savedLocation {
  // //   then, use the location as an input for the search box
  // // }
  // //Check if there is already a saved location saved in the HTML5 storage 
  // if ('savedLocation' in localStorage) {
  //   input = localStorage['savedLocation'];
  // }
  // else {
  // // Create search box and link it to the UI element.
  //   input = document.getElementById('pac-input');
  // }

  // Create search box and link it to the UI element.
  var input = document.getElementById('pac-input');
  
  var searchBox = new google.maps.places.SearchBox(input);
  
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

  // Bias the SearchBox results towards current map's viewport.
  map.addListener('bounds_changed', function() {
    searchBox.setBounds(map.getBounds());
  });

  // Setup primary marker and searches for events with markers
  setPrimaryMarker(map, searchBox, markers);  
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

    clearOldMarkers(markers); 
    
    console.log(places);

    // Instantiate boundaries for the map 
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

  var primaryLocation = {};

  primaryLocation["name"] = places[0].name;
  primaryLocation["address"] = places[0].formatted_address;
  primaryLocation["lat"] = places[0].geometry.location.lat();
  primaryLocation["lng"] = places[0].geometry.location.lng();            

  console.log(primaryLocation);

  // Save the location to a local storage session (persists in browser)
  // localStorage.setItem('savedLocation', places[0].formatted_address);
  // console.log("saved session:" + localStorage.savedLocation);

  //AJAX call to server to save session with provided address
  // $.ajax({url: "/"})

  // AJAX call to server to search local events with provided address
  $.ajax({url: "/search-events", 
          data: primaryLocation, 
          success: function(result) {
            setEventMarkers(result, map);
          },
          error: function(error) {
            console.log(error);
          }
        });
 }

function setEventMarkers(data, map) {
  // Event places data from server
  var eventPlaces = Object.values(data);
  console.log(eventPlaces); 

  // Exit out of function if no search results
  if (eventPlaces.length == 0) {
    return;
  }

  // Add a marker and info window to each event place
  for (var i = 0; i < eventPlaces.length; i++) {
    var place = eventPlaces[i]; 
    console.log(place.position);
    // var shortEventDescript = (function(place) {
    //       if len(place.description) > 280 {
    //         return place.description.slice(0, 281) + '...'; 
    //       }
    //       else {
    //         return place.description;
    //       } 
    //     })();

    // Skips over the place if it does not have position
    if (jQuery.isEmptyObject(place.position) || place.position == {"lat":0, "lng":0}) {
      continue;
    } 

    var shortEventDescript = place.description.slice(0, 281); 
    var contentString = '<div id="windowContent">' + 
                        '<h3><a href=' + place.url + 'target="_blank">' + place.name + '</a></h3>' +
                        '<p><strong>' + place.time + '</strong></p>' + 
                        '<p>' + shortEventDescript + '...</p>' + 
                        '</div>';    
    // console.log(contentString);

    // Instantiates info window for place
    var placeInfowindow = new google.maps.InfoWindow({
      maxWidth: 200
    });
    var eventMarker = new google.maps.Marker({
      map: map,
      title: place.name,
      position: place.position,
      infowindow: contentString
    });

    // Add marker to map
    markers.push(eventMarker);

    eventMarker.addListener('click', function(evt) {
      placeInfowindow.setContent(this.infowindow);
      placeInfowindow.open( map, this )

      // hideAllInfoWindows(map, this.infowindow);
      // placeInfowindow.open(map, this); 
    });

    // Expand map boundaries to include new event marker
    bounds.extend(place.position);    

    // Fit map to extended new boundary 
    map.fitBounds(bounds); 
  }

  // Adds the list of these events on the page
  listEventsOnPage(eventPlaces);

}

function hideAllInfoWindows(map, placeInfowindow) {
  // Closes info windows when user clicks elsewhere
  markers.forEach(function(marker) {
    placeInfowindow.close(map, marker);
  });
}

function clearOldMarkers(markers) {
  // Clear out the old event markers.
  markers.forEach(function(marker) {
    marker.setMap(null);
  });
  markers = [];
}

function listEventsOnPage(eventPlaces) {
  // Full list of events on the side of the map
  var eventList = document.getElementById('events_list');

  var contentText = JSON.stringify(eventPlaces);

  eventList.innerHTML = contentText;
}

// function isEmpty(obj) {
//   for (var prop in obj) {
//     if (obj.hasOwnProperty(prop))
//       return false;
//     return true;
//   }
// }



