"use strict";

// Goes to login page when button clicked
$('#login').click(function() {
	window.location = "/login";
});

// Logs user out of session
$('#logout').click(function() {
	window.location = "/logout";
});

// Goes to registration page when button clicked
$('#register').click(function() {
	window.location = "/registration";
});

