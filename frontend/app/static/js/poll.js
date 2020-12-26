
function poll_status(item) {
    // Connect to the Socket.IO server.
    // The connection URL has the following format, relative to the current page:
    //     http[s]://<domain>:<port>[/<namespace>]
    var socket = io('http://' + document.domain + ':' + location.port);

    // connect to backend and send over the item
    socket.on('connect', function() {
        socket.emit('poll_status', item);
    });

    // listen for a status update from the server
    socket.on('status', function(data) {
        $('#data').text('Complete');
    });
}