/* 
* williamson_p3.js
* 
* Author: Noah Williamson
* Last edit: 10/30/2017
* CS316 Project 3
*
* Simple node.js server that listens on a random port number between 
* 2000 and 30000 takes a filename in the URL and then checks
* first to make sure it matches a regex pattern that verifies that the 
* requested URL is only trying to access a jpg image or mp3 audio. If it
* passes this, then the server attempts to read the .jpg or .mp3 file and
* if there is an error then an appropriate error message/status is sent,
* else the file is served to the client. However, 1/3 of the time, an ad is
* served called 'advert.jpg'.
*/

var http = require("http"),
	url = require('url'),
	fs = require('fs');

const STARTPORT = 2000;
const ENDPORT = 30000; // max and min port values

// get a random port number between STARTPORT and ENDPORT
const port = Math.floor( Math.random() * ((ENDPORT + 1) - STARTPORT) ) + STARTPORT;
const hostname = 'iris.cs.uky.edu';

// function to process requests from the user
function serveURL(request, response){
	var xurl = request.url;
	console.log("Requested URL: " + xurl);
	
	// regex pattern
	var pattern = /^\/[a-zA-Z0-9_]+\.(mp3|jpg)$/;
	
	// does URL match regex?
	if(xurl.match(pattern) == null){
		// give error
		response.statusCode = 403;
		response.setHeader('Content-Type', 'text/plain');
		response.end('Invalid file request');
	}
	else{
		giveFile(request, response);
	}

}

// Function to give file either mp3 or jpg or, 33% of the time, an ad
function giveFile(request, response) {
	var xurl = request.url;
	var filename = xurl.substr(1);	// get rid of leading slash
	
	// determine if we need to send an ad
	var ad = 'advert.jpg';
	var max = 4, min = 1;	// generate a number between 1 and 3
	var rand = Math.floor( Math.random() * (max - min) ) + min;
	if (rand == min)	// 1/3 of times give ad
		filename = ad;
			
	fs.readFile(filename, function(error, data){
		if(error){	// give file not found error if necessary
			response.statusCode = 404;
			response.setHeader('Content-Type', 'text/plain');
			response.end('File not found.');
		}
		else{		// else give the file
			response.statusCode = 200;
				
			// set contnet types appropriately
			if(filename.indexOf('.jpg') != -1)
				response.setHeader('Content-Type', 'image/jpeg');
			else
				response.setHeader('Content-Type', 'audio/mpeg3');
			
			response.end(data); 	// send file
		}
	});

	return;
}

// log to console
console.log("Server listening on http://" + hostname + ":" + port);

var server = http.createServer(serveURL); // create server and start listening
server.listen(port, hostname);

