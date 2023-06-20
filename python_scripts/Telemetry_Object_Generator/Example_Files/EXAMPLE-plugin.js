
define([
    //"./EXAMPLELimitProvider_Test",
], function (
    //EXAMPLELimitProvider
) {

    function EXAMPLEPlugin() {

        function getEXAMPLEDictionary() {
            return fetch('/example/EXAMPLE/EXAMPLEdictionary.json').then(function (response) {
                return response.json();
            });

        }

        // An object provider builds Domain Objects
        var EXAMPLE_objectProvider = {
            get: function (identifier) {
                return getEXAMPLEDictionary().then(function (dictionary) {
                    //console.log("EXAMPLE-dictionary-plugin.js: identifier.key = " + identifier.key);
                    if (identifier.key === 'EXAMPLE') {
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
                            type: 'EXAMPLE.telemetry',
                            telemetry: {
                                values: measurement.values
                            },
                            location: 'EXAMPLE.taxonomy:EXAMPLE'
                        };
                    }
                });
            }
        };

        // The composition of a domain object is the list of objects it contains, as shown (for example) in the tree for browsing.
        // Can be used to populate a hierarchy under a custom root-level object based on the contents of a telemetry dictionary.
        // "appliesTo"  returns a boolean value indicating whether this composition provider applies to the given object
        // "load" returns an array of Identifier objects (like the channels this telemetry stream offers)
        var EXAMPLE_compositionProvider = {
            appliesTo: function (domainObject) {
                return domainObject.identifier.namespace === 'EXAMPLE.taxonomy'
                    && domainObject.type === 'folder';
            },
            load: function (domainObject) {
                return getEXAMPLEDictionary()
                    .then(function (dictionary) {
                        return dictionary.measurements.map(function (m) {
                            return {
                                namespace: 'EXAMPLE.taxonomy',
                                key: m.key
                            };
                        });
                    });
            }
        };

        return function install(openmct) {
            // The addRoot function takes an "object identifier" as an argument
            openmct.objects.addRoot({
                namespace: 'EXAMPLE.taxonomy',
                key: 'EXAMPLE'
            });

            openmct.objects.addProvider('EXAMPLE.taxonomy', EXAMPLE_objectProvider);

            openmct.composition.addProvider(EXAMPLE_compositionProvider);

            //openmct.telemetry.addProvider(new EXAMPLELimitProvider());

            openmct.types.addType('EXAMPLE.telemetry', {
                name: 'EXAMPLE Telemetry Point',
                description: 'Telemetry of EXAMPLE',
                cssClass: 'icon-telemetry'
            });
        };
    }

    return EXAMPLEPlugin;
});
