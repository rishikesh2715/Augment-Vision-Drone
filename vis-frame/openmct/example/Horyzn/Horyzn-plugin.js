
define([

], function (

) {

    function HoryznPlugin() {

        function gethoryznDictionary() {
            return fetch('/example/Horyzn/Horyzndictionary.json').then(function (response) {
                return response.json();
            });

        }

        // An object provider builds Domain Objects
        var Horyzn_objectProvider = {
            get: function (identifier) {
                return gethoryznDictionary().then(function (dictionary) {
                    //console.log("Horyzn-dictionary-plugin.js: identifier.key = " + identifier.key);
                    if (identifier.key === 'Horyzn') {
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
                            type: 'Horyzn.telemetry',
                            telemetry: {
                                values: measurement.values
                            },
                            location: 'Horyzn.taxonomy:Horyzn'
                        };
                    }
                });
            }
        };

        // The composition of a domain object is the list of objects it contains, as shown (for example) in the tree for browsing.
        // Can be used to populate a hierarchy under a custom root-level object based on the contents of a telemetry dictionary.
        // "appliesTo"  returns a boolean value indicating whether this composition provider applies to the given object
        // "load" returns an array of Identifier objects (like the channels this telemetry stream offers)
        var Horyzn_compositionProvider = {
            appliesTo: function (domainObject) {
                return domainObject.identifier.namespace === 'Horyzn.taxonomy'
                    && domainObject.type === 'folder';
            },
            load: function (domainObject) {
                return gethoryznDictionary()
                    .then(function (dictionary) {
                        return dictionary.measurements.map(function (m) {
                            return {
                                namespace: 'Horyzn.taxonomy',
                                key: m.key
                            };
                        });
                    });
            }
        };

        return function install(openmct) {
            // The addRoot function takes an "object identifier" as an argument
            openmct.objects.addRoot({
                namespace: 'Horyzn.taxonomy',
                key: 'Horyzn'
            });

            openmct.objects.addProvider('Horyzn.taxonomy', Horyzn_objectProvider);

            openmct.composition.addProvider(Horyzn_compositionProvider);

            openmct.types.addType('Horyzn.telemetry', {
                name: 'Horyzn Telemetry Point',
                description: 'Telemetry of Horyzn',
                cssClass: 'icon-telemetry'
            });
        };
    }

    return HoryznPlugin;
});
