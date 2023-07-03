define([

], function (

) {

    function FLUTTERPlugin() {

        function getMODEDictionary() {
            return fetch('/example/Flutterometer/FLUTTERdictionary.json').then(function (response) {
                return response.json();
            });

        }

        // An object provider builds Domain Objects
        var FLUTTER_objectProvider = {
            get: function (identifier) {
                return getMODEDictionary().then(function (dictionary) {
                    //console.log("FLUTTER-dictionary-plugin.js: identifier.key = " + identifier.key);
                    if (identifier.key === 'FLUTTER') {
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
                            type: 'FLUTTER.telemetry',
                            telemetry: {
                                values: measurement.values
                            },
                            location: 'FLUTTER.taxonomy:FLUTTER'
                        };
                    }
                });
            }
        };

        // The composition of a domain object is the list of objects it contains, as shown (for example) in the tree for browsing.
        // Can be used to populate a hierarchy under a custom root-level object based on the contents of a telemetry dictionary.
        // "appliesTo"  returns a boolean value indicating whether this composition provider applies to the given object
        // "load" returns an array of Identifier objects (like the channels this telemetry stream offers)
        var FLUTTER_compositionProvider = {
            appliesTo: function (domainObject) {
                return domainObject.identifier.namespace === 'FLUTTER.taxonomy'
               && domainObject.type === 'folder';
            },
            load: function (domainObject) {
                return getMODEDictionary()
                    .then(function (dictionary) {
                        return dictionary.measurements.map(function (m) {
                            return {
                                namespace: 'FLUTTER.taxonomy',
                                key: m.key
                            };
                        });
                    });
            }
        };

        return function install(openmct) {
        // The addRoot function takes an "object identifier" as an argument
            openmct.objects.addRoot({
                namespace: 'FLUTTER.taxonomy',
                key: 'FLUTTER'
            });

            openmct.objects.addProvider('FLUTTER.taxonomy', FLUTTER_objectProvider);

            openmct.composition.addProvider(FLUTTER_compositionProvider);

            openmct.types.addType('FLUTTER.telemetry', {
                name: 'MODE Telemetry Point',
                description: 'Modes to identify flutter',
                cssClass: 'icon-telemetry'
            });
        };

    }

    return FLUTTERPlugin;
});
