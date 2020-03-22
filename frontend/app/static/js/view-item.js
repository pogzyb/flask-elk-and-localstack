
function poll_status(term) {
    var socket = io();
    socket.on('connect', function() {
        socket.emit('view-page', term);
    });

    socket.on('status', function(data) {
        console.log('Got this status: ', data);
        $('#data').text('DONE');
    });
}