"use strict";

//Changes the register/login/logout links when the user status changes

// Goes to login and registration page when button clicked
$('#login').click(function() {
	window.location = "/login";
});

// Changes button to logout if user is logged in and vice versa
//eventually do this with AJAX