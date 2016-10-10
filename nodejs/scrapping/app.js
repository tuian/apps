var express = require("express");
var request = require("request");
var fs = require("fs");

var app = express();
var port = "8101";

// Example 1 - connecting to Google.com

// var url = "http://www.google.com";

// request(url,function(err, resp, body){

// 	if(err){
// 		console.log(err);
// 	}else{
// 		console.log(body);
// 	}
// });


// Example 2 - connecting and downloading Google.com

var url = "http://www.google.com";
var destination = fs.createWriteStream("./downloads/google2.html");

request(url).pipe(destination);


// Example 3 - connecting and downloading Google.com and watch for events

var url = "http://www.googl3e.com";
var destination = fs.createWriteStream("./downloads/google3.html");

request(url,function(err,resp, body){
	b = body
})
.pipe(destination)
.on('finish',function(){
console.log("All done")
})
.on('error',function(err){
console.log("Error:"+err)
});


// create a express server:

app.listen(port,function(response){

	console.log("Listening on port: "+port);
	console.log("Listening on port: "+response);
	
});