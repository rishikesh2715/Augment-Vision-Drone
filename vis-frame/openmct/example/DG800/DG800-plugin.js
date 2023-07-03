
define([
    "./DG800LimitProvider",
], function (
    DG800LimitProvider
) {

    function DG800Plugin() {

        function getDG800Dictionary() {
            return fetch('/example/DG800/DG800dictionary.json').then(function (response) {
                return response.json();
            });

        }

        // An object provider builds Domain Objects
        var DG800_objectProvider = {
            get: function (identifier) {
                return getDG800Dictionary().then(function (dictionary) {
                    //console.log("DG800-dictionary-plugin.js: identifier.key = " + identifier.key);
                    if (identifier.key === 'DG800') {
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
                            type: 'DG800.telemetry',
                            telemetry: {
                                values: measurement.values
                            },
                            location: 'DG800.taxonomy:DG800'
                        };
                    }
                });
            }
        };

        // The composition of a domain object is the list of objects it contains, as shown (for example) in the tree for browsing.
        // Can be used to populate a hierarchy under a custom root-level object based on the contents of a telemetry dictionary.
        // "appliesTo"  returns a boolean value indicating whether this composition provider applies to the given object
        // "load" returns an array of Identifier objects (like the channels this telemetry stream offers)
        var DG800_compositionProvider = {
            appliesTo: function (domainObject) {
                return domainObject.identifier.namespace === 'DG800.taxonomy'
                    && domainObject.type === 'folder';
            },
            load: function (domainObject) {
                return getDG800Dictionary()
                    .then(function (dictionary) {
                        return dictionary.measurements.map(function (m) {
                            return {
                                namespace: 'DG800.taxonomy',
                                key: m.key
                            };
                        });
                    });
            }
        };

        return function install(openmct) {
            // The addRoot function takes an "object identifier" as an argument
            openmct.objects.addRoot({
                namespace: 'DG800.taxonomy',
                key: 'DG800'
            });

            openmct.objects.addProvider('DG800.taxonomy', DG800_objectProvider);

            openmct.composition.addProvider(DG800_compositionProvider);

            openmct.types.addType('DG800.telemetry', {
                name: 'DG800 Telemetry Point',
                description: 'Telemetry of DG800',
                cssClass: 'icon-telemetry'
            });

            openmct.telemetry.addProvider(new DG800LimitProvider());
        };
    }

    return DG800Plugin;
});
