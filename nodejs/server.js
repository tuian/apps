var http = require("http");

console.log("Starting the server...")

http.createServer(function(request, response) {
console.log(request)
response.writeHead(200, {"Content-Type": "text/plain"});
response.write("Hello World");
response.end();

}).listen(8888);
