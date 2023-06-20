/*
Copyright 2017 Erigo Technologies LLC
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

/**
 * Real-time server, run on server side; pushes real-time updates to subscribed
 * channels over WebSockets.
 *
 * This is a modified version of the original realtime-server.js from
 * openmct-tutorial; this version can serve multiple telemetry sources at
 * different ports.
 */

var WebSocketServer = require('ws').Server;

function RealtimeServer(telemetrySource, port) {
    this.telemetrySource = telemetrySource;
    this.server = new WebSocketServer({ port: port });
    this.server.on('connection', this.handleConnection.bind(this));
    console.log('Realtime server started at ws://localhost:' + port);
};

RealtimeServer.prototype.handleConnection = function (ws) {
    var unlisten = this.telemetrySource.listen(notifySubscribers);
        subscribed = {}, // Active subscriptions for this connection
        handlers = { // Handlers for specific requests
            subscribe: function (id) {
                subscribed[id] = true;
            },
            unsubscribe: function (id) {
                delete subscribed[id];
            }
        };

    // this function is called as a result of spacecraft.js/notify() or cloudturbine.js/notify() being called
    // push out data (via WebSocket) to the client-side subscribers (see realtime-telemetry-plugin.js/socket.onmessage)
    function notifySubscribers(point) {
        if (subscribed[point.id]) {
        	// console.log('realtime-server.js: push data to subscribed channel ' + point.id + ': time = ' + point.timestamp + ' value = ' + point.value);
            ws.send(JSON.stringify(point));
        }
    }

    // Listen for requests of subscribers
    ws.on('message', function (message) {
        var parts = message.split(' '),
            handler = handlers[parts[0]];
        if (handler) {
            handler.apply(handlers, parts.slice(1));
        }
    });

    // Stop sending telemetry updates for this connection when closed
    ws.on('close', unlisten);
};



module.exports = RealtimeServer;
