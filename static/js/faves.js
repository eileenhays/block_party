"use strict";


$( ".remove" ).click(function(evt) {
	evt.preventDefault();

	var evt_id = $(this).attr('data-evt_id');
	var removeEvt = {evt_id: evt_id};

	$.post("/remove-event", removeEvt)
	.done(function(msg) {
		alert( msg + " was removed from favorites" );
	});
	// Remove event div
	$( "#evt-" + evt_id ).remove();	
});

// Allow for sorting by date (ascending and descending order)
// $( ".date-sort" ).click(function(evt) {
// 	evt.preventDefault();

// 	$.post("/date-sort", function(data) {
// 		//data will be sorted and the page updates without refreshing
// 	});

// });