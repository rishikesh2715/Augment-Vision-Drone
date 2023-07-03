
define([

], function (

) {

    function FLEXOPPlugin() {

        function getTFLEXDictionary() {
            return fetch('/example/FLEXOP/TFLEXdictionary.json').then(function (response) {
                return response.json();
            });

        }

        // An object provider builds Domain Objects
        var FLEXOP_objectProvider = {
            get: function (identifier) {
                return getTFLEXDictionary().then(function (dictionary) {
                    //console.log("FLEXOP-dictionary-plugin.js: identifier.key = " + identifier.key);
                    if (identifier.key === 'TFLEX') {
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
                            type: 'TFLEX.telemetry',
                            telemetry: {
                                values: measurement.values
                            },
                            location: 'FLEXOP.taxonomy:TFLEX'
                        };
                    }
                });
            }
        };

        // The composition of a domain object is the list of objects it contains, as shown (for example) in the tree for browsing.
        // Can be used to populate a hierarchy under a custom root-level object based on the contents of a telemetry dictionary.
        // "appliesTo"  returns a boolean value indicating whether this composition provider applies to the given object
        // "load" returns an array of Identifier objects (like the channels this telemetry stream offers)
        var FLEXOP_compositionProvider = {
            appliesTo: function (domainObject) {
                return domainObject.identifier.namespace === 'FLEXOP.taxonomy'
                    && domainObject.type === 'folder';
            },
            load: function (domainObject) {
                return getTFLEXDictionary()
                    .then(function (dictionary) {
                        return dictionary.measurements.map(function (m) {
                            return {
                                namespace: 'FLEXOP.taxonomy',
                                key: m.key
                            };
                        });
                    });
            }
        };

        return function install(openmct) {
            // The addRoot function takes an "object identifier" as an argument
            openmct.objects.addRoot({
                namespace: 'FLEXOP.taxonomy',
                key: 'TFLEX'
            });

            openmct.objects.addProvider('FLEXOP.taxonomy', FLEXOP_objectProvider);

            openmct.composition.addProvider(FLEXOP_compositionProvider);

            openmct.types.addType('TFLEX.telemetry', {
                name: 'TFLEX Telemetry Point',
                description: 'Telemetry of TFLEX',
                cssClass: 'icon-telemetry'
            });
        };
    }

    return FLEXOPPlugin;
});
