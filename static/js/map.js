var map;
var defaultLocation = {lat: 37.7749, lng: -122.4194}; 
var markers = [];


// Add a search box for map that uses Autocomplete. Uses Places library. 

function initAutocomplete() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: defaultLocation,
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
  setPrimaryMarker(map, searchBox); //How to reset with a new address?**** 

}

function setPrimaryMarker(map, searchBox) {
  // Listen for the event fired when the user selects a prediction and retrieve
  // more details for that place. Autocomplete object. 
  searchBox.addListener('places_changed', function() {
    var places = searchBox.getPlaces();
    
    if (places.length == 0) {
      return;
    }
    else if (places.length > 1) {
      return console.log("Please search for one address"); //have it flash a message***
    }

    clearOldMarkers(markers);
    
    console.log(places);

    var bounds = new google.maps.LatLngBounds();
    window.bounds = bounds
    
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


function searchWithPrimaryLocation(places) {
  // User input primary location to search for local events.

  var primaryLocation = {};

  primaryLocation["name"] = places[0].name;
  primaryLocation["lat"] = places[0].geometry.location.lat();
  primaryLocation["lng"] = places[0].geometry.location.lng();            

  console.log(primaryLocation);

  // AJAX call to server to search local events with provided address
  $.get("/search-events", 
        primaryLocation, 
        function(result) {
          setEventMarkers(result, map)
        },
        function(error) {
          console.log(error);
        });
 }

function setEventMarkers(data, map) {
  // Event places data from server
  var eventPlaces = Object.values(data);
  console.log(eventPlaces);

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

    // Expand map boundaries to include event markers
    bounds.extend(place.position)
    // addInfoWindow(marker, map)    
  });

  // Fit map to extended new boundary 
  map.fitBounds(bounds);
}

function clearOldMarkers(markers) {
    // Clear out the old event markers.
    markers.forEach(function(marker) {
      markers.setMap(null);
    });
    markers = [];
}

function addInfoWindow(marker, map) {
  var contentString = 'div id="windowContent"' + 
                      '<h1>Event</h1><br>' +
                      '<p>This is where event info goes.</p>' + 
                      '</div>';
    // '<div id="content">'+
    // '<div id="siteNotice">'+
    // '</div>'+
    // '<h1 id="firstHeading" class="firstHeading">Uluru</h1>'+
    // '<div id="bodyContent">'+
    // '<p><b>Uluru</b>, also referred to as <b>Ayers Rock</b>, is a large ' +
    // 'sandstone rock formation in the southern part of the '+
    // 'Northern Territory, central Australia. It lies 335&#160;km (208&#160;mi) '+
    // 'south west of the nearest large town, Alice Springs; 450&#160;km '+
    // '(280&#160;mi) by road. Kata Tjuta and Uluru are the two major '+
    // 'features of the Uluru - Kata Tjuta National Park. Uluru is '+
    // 'sacred to the Pitjantjatjara and Yankunytjatjara, the '+
    // 'Aboriginal people of the area. It has many springs, waterholes, '+
    // 'rock caves and ancient paintings. Uluru is listed as a World '+
    // 'Heritage Site.</p>'+
    // '<p>Attribution: Uluru, <a href="https://en.wikipedia.org/w/index.php?title=Uluru&oldid=297882194">'+
    // 'https://en.wikipedia.org/w/index.php?title=Uluru</a> '+
    // '(last visited June 22, 2009).</p>'+
    // '</div>'+
    // '</div>';

  var i = 0; //need to increment this

  var infowindow = new google.maps.InfoWindow({
    content: contentString,
    num: i
  });

  // var marker = new google.maps.Marker({
  // position: uluru,
  // map: map,
  // title: 'Uluru (Ayers Rock)'
  // });

  marker.addListener('click', function() {
  infowindow.open(map, marker);
  });
}
