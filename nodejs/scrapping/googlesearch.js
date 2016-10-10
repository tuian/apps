var express = require("express");
var request = require("request");
var fs = require("fs");
var cheerio = require("cheerio");

var app = express();
var port = "8101";


// Download the specific elements from a job listing page

//var url = "http://www.google.com";
var url = "http://au.indeed.com/jobs?q=data&l=Parramatta+NSW"

request(url,function(err,resp, body){
	//console.log(body);
	var $ = cheerio.load(body);
	
	//var description = $('#_eEe');
	// # for id, . for class
	// var description = $('.jobtitle turnstileLink'); 
	// description_text = description.text();
	// console.log(description_text)
	console.log("URL: "+url)
	console.log("Search Word: job title\n")

	$('.jobtitle').filter(function(){
	
	 description = $(this);
	 //location = $(".jobtitle .sjcl")
	 description_text = description.text();
	
	console.log(description_text)
	// console.log("Location: ",location.text())

	})
	
	

})


// create a express server:

app.listen(port);
console.log("Listening on port: "+port);
	
	
//*[@id="job-content"]/tbody/tr/td[1]/div/span[1]
//*[@id="gbw"]/div/div/div[1]/div[1]/a