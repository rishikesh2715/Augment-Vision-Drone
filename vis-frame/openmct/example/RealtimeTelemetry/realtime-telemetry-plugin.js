/**
 * Basic Realtime telemetry plugin using websockets.
 */

define([

], function (

) {

    function RealtimeTelemetryPlugin(desired_domain_object_type, serverURL, IP) {
        return function (openmct) {
            //var desired_domain_object_type = 'TFLEX.telemetry';
            var port = 16969;
            var socket = new WebSocket('ws://' + IP + ':' + port + serverURL);
            var listeners = {};

            // This is the WebSockets function that gets called to push data updates from the real-time server to the real-time client
            // (see realtime-server.js/notifySubscribers())
            socket.onmessage = function (event) {
                point = JSON.parse(event.data);
                // console.log("realtime-telemetry-plugin.js: received new data for channel " + point.id + ": time = " + point.timestamp + " value = " + point.value);
                if (listeners[point.id]) {
                    listeners[point.id].forEach(function (l) {
                        l(point);
                    });
                }
                // if (listener[point.id]) {
                //     listener[point.id](point);
                // }
            };

            // var provider = {
            // supportsSubscribe: function (domainObject) {
            // return domainObject.type === desired_domain_object_type;
            // },
            // subscribe: function (domainObject, callback) {
            // listener[domainObject.identifier.key] = callback;
            // socket.send('subscribe ' + domainObject.identifier.key);
            // return function unsubscribe() {
            // delete listener[domainObject.identifier.key];
            // socket.send('unsubscribe ' + domainObject.identifier.key);
            // };
            // }
            // };
            var provider = {
                supportsSubscribe: function (domainObject) {
                    return domainObject.type === desired_domain_object_type;
                },
                subscribe: function (domainObject, callback, options) {
                    if (!listeners[domainObject.identifier.key]) {
                        listeners[domainObject.identifier.key] = [];
                    }

                    if (!listeners[domainObject.identifier.key].length) {
                        socket.send('subscribe ' + domainObject.identifier.key);
                    }

                    listeners[domainObject.identifier.key].push(callback);

                    return function () {
                        listeners[domainObject.identifier.key] =
                            listeners[domainObject.identifier.key].filter(function (c) {
                                return c !== callback;
                            });

                        if (!listeners[domainObject.identifier.key].length) {
                            socket.send('unsubscribe ' + domainObject.identifier.key);
                        }
                    };
                }
            };

            openmct.telemetry.addProvider(provider);
        };
    }

    return RealtimeTelemetryPlugin;
});
