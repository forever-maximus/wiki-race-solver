
window.onload = function() {
    var searchButton = document.getElementById("search-button");
    searchButton.addEventListener("click", sendSearchRequest, false);

    //var socket = io.connect('http://' + document.domain + ':' + location.port);
    var socket = io.connect({transports: ['websocket']});

    socket.on('connect', function() {
        socket.emit('client connected', {data: 'New client connected!'});
    });

    socket.on('search response', function(data){
        console.log(data);
    });

    function sendSearchRequest() {
        console.log("search button clicked!");
        socket.emit('search request', {data: 'requesting search'});
    }
};

