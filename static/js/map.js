"use strict";

var map;
var centerSF = {lat: 37.7749, lng: -122.4194}; 
var markers = [];
var event_address = '';


function initAutocomplete() {
  // Instantiates map 
  map = new google.maps.Map(document.getElementById('map'), {
    center: centerSF,
    zoom: 12,
    mapTypeId: 'roadmap'
  });

  var input = document.getElementById('pac-input');

  // Create search box and link it to the UI element.
  var searchBox = new google.maps.places.SearchBox(input);
 
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

  // Bias the SearchBox results towards current map's viewport.
  map.addListener('bounds_changed', function() {
    searchBox.setBounds(map.getBounds());
  });

  // Setup primary marker and searches for events with markers
  setPrimaryMarker(map, searchBox, markers); 

  // Sets evt listener on "Update Homebase" button to change 
  // to latest search
  updateHomebase();

  // Checks if there is address already in session to autoload
  $.get("/homebase-in-session")
      .done(function(address) {
            console.log("returned_address " + address);
            if (address !== 'None') {
              input.value = address;
            }
      });
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
    
    // console.log(places);

    // Instantiate boundaries for the map 
    var bounds = new google.maps.LatLngBounds();
    window.bounds = bounds
    
    places.forEach(function(place) {
      if (!place.geometry) {
        console.log("Returned place contains no geometry");
        return;
      }

      var primaryIcon = {
        url: "/static/images/logos_markers/turqoise_marker.svg",
        size: new google.maps.Size(71, 71), 
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34), 
        scaledSize: new google.maps.Size(40, 40) //25,25
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

  // console.log(primaryLocation);

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
    console.log("Place:" + place); //erase afterward

    // Skips over the place if position empty
    if (jQuery.isEmptyObject(place.position) || place.position.lat == 0 && place.position.lng == 0) {
      continue;
    } 
    
    if (jQuery.isEmptyObject(place.description)) {
      var contentString = "";
    } 
    else {
      var shortEventDescript = place.description.slice(0, 281); 
      contentString = '<div id="windowContent">' + 
                      '<h4><a href="' + place.url + '" target="_blank">' + place.name + '</a></h4>' +
                      '<strong>Group: </strong>' + place.group + '<br>' +
                      '<p><strong>' + place.datetime + '</strong></p>' + 
                      '<p>' + shortEventDescript + '...</p>' + 
                      '<button class="fave btn btn-default" data-src_evt_id="' + place.src_evt_id + '"' +
                                            'data-datetime="' + place.datetime + '"' +
                                            'data-name="' + place.name + '"' + 
                                            'data-url="' + place.url + '"' + 
                                            'data-group="' + place.group + '"' + 
                                            'data-lat="' + place.position.lat + '"' +
                                            'data-lng="' + place.position.lng + '"' +  
                                            'data-address="' + place.address + '"' +
                                            'data-cat="' + place.category + '"' +  
                                            'data-src_id="mtup">' +                                                                               
                                            'add to favorites</button>'+
                      '</div>';    
    // console.log(contentString);
    }
    // src_evt_id
    // Instantiates info window for place
    var placeInfowindow = new google.maps.InfoWindow({
      maxWidth: 200
    });

    var eventIcon = {
        url: "/static/images/logos_markers/coral_marker.svg",
        size: new google.maps.Size(71, 71), 
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34), 
        scaledSize: new google.maps.Size(45, 45) 
      };

    console.log(place.position);
    var eventMarker = new google.maps.Marker({
      map: map,
      title: place.name,
      icon: eventIcon,
      position: place.position,
      infowindow: contentString
    });

    // Add marker to map
    markers.push(eventMarker);

    // console.log(place.position);

    // Add event listener to marker to open info window
    eventMarker.addListener('click', function(evt) {
      placeInfowindow.setContent(this.infowindow);
      placeInfowindow.open( map, this )
      // var address = reverseGeocode(place.position.lat, place.position.lng);
      // Saves the event details to variables when favorite button clicked
      $('.fave').click(function(evt){
        evt.preventDefault();

        var lat = $(this).attr('data-lat');
        var lng = $(this).attr('data-lng');
        var eventInfo = {
          src_evt_id: $(this).attr('data-src_evt_id'),
          datetime: $(this).attr('data-datetime'),
          name: $(this).attr('data-name'),
          url: $(this).attr('data-url'),
          group_name: $(this).attr('data-group'),
          lat: lat,
          lng: lng,
          // address: address,
          address: $(this).attr('data-address'),
          category: $(this).attr('data-cat'), 
          src_id: $(this).attr('data-src_id'), 
        };

        // AJAX call to server to search local events with provided address
        $.post("/add-fave", eventInfo)
          .done(function(msg) {
            alert(msg + " was successfully added to favorites!");
          });
      });
    });  
    // Expand map boundaries to include new event marker
    bounds.extend(place.position);    

    // Fit map to extended new boundary 
    map.fitBounds(bounds); 
  }

  // Adds the list of these events on the page
  listEventsOnPage(eventPlaces);

}

function clearOldMarkers(markers) {
  // Clear out the old event markers.
  markers.forEach(function(marker) {
    marker.setMap(null);
  });
  markers = [];
}

function listEventsOnPage(eventPlaces) {
  // Full list of events on the bottom of the map
  var eventList = document.getElementById('evt-list');
  // console.log("events!" + eventList);
  var contentString = '';
  
  for (var i = 0; i < eventPlaces.length; i++) {
    var place = eventPlaces[i]; 
    // console.log(place);
    var evtString = '<h4><a href="' + place.url + '" target="_blank">' + place.name + '</a></h4>' +
                        '<strong>Group: </strong>' + place.group + '<br>' +
                        '<strong>' + place.datetime + '</strong><br>' + 
                        '<button class="fave btn btn-default" data-src_evt_id="' + place.src_evt_id + '"' +
                                            'data-datetime="' + place.datetime + '"' +
                                            'data-name="' + place.name + '"' + 
                                            'data-url="' + place.url + '"' + 
                                            'data-group="' + place.group + '"' + 
                                            'data-lat="' + place.position.lat + '"' +
                                            'data-lng="' + place.position.lng + '"' +  
                                            'data-address="' + place.address + '"' +
                                            'data-cat="' + place.category + '"' +  
                                            'data-src_id="mtup">' +                                                                               
                                            'add to favorites</button>'+ 
                        '<p class="evt-description">' + place.description + '</p>' + '<br><br>';

    contentString += evtString;
  }

  eventList.innerHTML = contentString;
}

function reverseGeocode(lat, lng) {
  var latlng = lat + ',' + lng;
  var address = $.ajax({url: 'https://maps.googleapis.com/maps/api/geocode/json?latlng=' + latlng,
          success: function(result) {
          var formatted_address = result['results'][0]['formatted_address'];
          address += formatted_address;
          console.log('in here!' + address)
          return formatted_address;
          },
          async: false
  });

  console.log("This is an address obj " + address);
  // debugger;
  console.log("This is an address " + address.responseJSON.results[0])
  return address.responseJSON.results[0].formatted_address;
}

function updateHomebase() {
  // Updates the user's home address to current session
  $('#update-home').click(function(evt){    

    $.post("/update-homebase", function(new_addy) {
      $("#homebase-addy").html(new_addy);
    });
  });
}
