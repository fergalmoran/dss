/** @license

 ----------------------------------------------

 Copyright (c) 2013, Fergal Moran. All rights reserved.
 Code provided under the BSD License:

 */

var socket = new io.Socket({host: 'ext-test.deepsouthsounds.com', resource: 'socket.io', port: '8000', rememberTransport: false});
socket.connect();

socket.on('message', function (obj) {
    if ('buffer' in obj) {
        document.getElementById('form').style.display = 'block';
        document.getElementById('chat').innerHTML = '';

        for (var i in obj.buffer) message(obj.buffer[i]);
    } else message(obj);
});

socket.on('reconnect', function () {
    $('#lines').remove();
    message('System', 'Reconnected to the server');
});

socket.on('reconnecting', function () {
    message('System', 'Attempting to re-connect to the server');
});

socket.on('error', function (e) {
    message('System', e ? e : 'An unknown error occurred');
});

function message (from, msg) {
    console.log(msg);
    $('#lines').append($('<p>').append($('<b>').text(from), msg));
}
