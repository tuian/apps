var express = require("express");
var request = require("request");
var fs = require("fs");
var cheerio = require("cheerio");

var app = express();
var port = "8101";


// Download the specific elements from a job listing page

//var url = "http://www.google.com";
var url = "http://au.indeed.com/viewjob?jk=b0da89142f841b0e"
var destination = fs.createWriteStream("./downloads/joblisting.html");

request(url,function(err,resp, body){
	//console.log(body);
	var $ = cheerio.load(body);
	
	var companyName1 = $('.company');
	companyName_text1 = companyName1.text();
	console.log(companyName_text1)

	$('.company').filter(function(){

	 var companyName2 = $(this);
	 companyName_text2 = companyName2.text();
	
	
	})
	
	console.log(companyName_text2)

})


// create a express server:

app.listen(port);
console.log("Listening on port: "+port);
	
	
//*[@id="job-content"]/tbody/tr/td[1]/div/span[1]