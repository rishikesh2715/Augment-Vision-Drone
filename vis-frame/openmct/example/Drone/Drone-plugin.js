
define([
    //"./DroneLimitProvider_Test",
], function (
    //DroneLimitProvider
) {

    function DronePlugin() {

        function getDroneDictionary() {
            return fetch('/example/Drone/Dronedictionary.json').then(function (response) {
                return response.json();
            });

        }

        // An object provider builds Domain Objects
        var Drone_objectProvider = {
            get: function (identifier) {
                return getDroneDictionary().then(function (dictionary) {
                    //console.log("Drone-dictionary-plugin.js: identifier.key = " + identifier.key);
                    if (identifier.key === 'Drone') {
                        return {
                            identifier: identifier,
                            name: dictionary.name,
                            type: 'folder',
                            location: 'ROOT'
                        };
                    } else {
                        var measurement = dictionary.measurements.filter(function (m) {
                            return m.key === identifier.key;
                        })[0];

                        return {
                            identifier: identifier,
                            name: measurement.name,
                            type: 'Drone.telemetry',
                            telemetry: {
                                values: measurement.values
                            },
                            location: 'Drone.taxonomy:Drone'
                        };
                    }
                });
            }
        };

        // The composition of a domain object is the list of objects it contains, as shown (for example) in the tree for browsing.
        // Can be used to populate a hierarchy under a custom root-level object based on the contents of a telemetry dictionary.
        // "appliesTo"  returns a boolean value indicating whether this composition provider applies to the given object
        // "load" returns an array of Identifier objects (like the channels this telemetry stream offers)
        var Drone_compositionProvider = {
            appliesTo: function (domainObject) {
                return domainObject.identifier.namespace === 'Drone.taxonomy'
                    && domainObject.type === 'folder';
            },
            load: function (domainObject) {
                return getDroneDictionary()
                    .then(function (dictionary) {
                        return dictionary.measurements.map(function (m) {
                            return {
                                namespace: 'Drone.taxonomy',
                                key: m.key
                            };
                        });
                    });
            }
        };

        return function install(openmct) {
            // The addRoot function takes an "object identifier" as an argument
            openmct.objects.addRoot({
                namespace: 'Drone.taxonomy',
                key: 'Drone'
            });

            openmct.objects.addProvider('Drone.taxonomy', Drone_objectProvider);

            openmct.composition.addProvider(Drone_compositionProvider);

            //openmct.telemetry.addProvider(new DroneLimitProvider());

            openmct.types.addType('Drone.telemetry', {
                name: 'Drone Telemetry Point',
                description: 'Telemetry of Drone',
                cssClass: 'icon-telemetry'
            });
        };
    }

    return DronePlugin;
});
