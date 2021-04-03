// SocketIO
// ---------------------
// SocketIO leverages WebSockets, which are more efficient for "long polling" cases like this.
// HTTP is not meant for keeping open a connection; WebSockets are! WebSockets are a separate
// implementation over TCP that can be used for "long lived" connections. So unlike HTTP,
// WebSockets are great for patiently waiting for the backend server to kick some data back
// to the client without bombarding it with HTTP requests.

// https://www.fullstackpython.com/websockets.html

function poll_status(item) {
    // Connect to the Socket.IO server.
    // The connection URL has the following format, relative to the current page:
    //     http[s]://<domain>:<port>[/<namespace>]
    const socket = io({rememberTransport: false, transport: 'websocket'});
    // connect to backend and send over the item
    socket.on('connect', function() {
        socket.emit('poll_status', item);
    });

    // listen for a status update from the server
    socket.on('status', function(data) {
        $('#data').text('Complete');
    });
}