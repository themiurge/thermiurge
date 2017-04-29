var http = require("http");
var url = require("url");
var util = require("util");

function getOutsideTemperature() {
    return Math.random() * 12.0 + 8.0;
}

function getRoomTemperature() {
    return Math.random() * 5.0 + 17.0;
}

http.createServer(function (request, response) {

    // Retrieve request type
    var reqType = url.parse(request.url).pathname.substr(1);
    var t = 0.0;
    
    // Retrieve requested temperature
    switch (reqType) {
        case "in":
            t = getRoomTemperature();
            break;
        case "out":
            t = getOutsideTemperature();
            break;
    }

    // Write response and send
    response.writeHead(200, {'Content-Type': 'text/plain'});
    response.write(util.format("%j", t));
    response.end();
    

}).listen(8081);

console.log('Server running at http://127.0.0.1:8081/');
