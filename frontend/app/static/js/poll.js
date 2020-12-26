
function poll_status(item) {
    // Connect to the Socket.IO server.
    // The connection URL has the following format, relative to the current page:
    //     http[s]://<domain>:<port>[/<namespace>]
    var socket = io();

    // connect to and send over the item
    socket.on('connect', function() {
        socket.emit('poll-item-status', item);
    });

    socket.on('status', function(data) {
        console.log('received status:', data);
        $('#data').text('Complete');
    });
}