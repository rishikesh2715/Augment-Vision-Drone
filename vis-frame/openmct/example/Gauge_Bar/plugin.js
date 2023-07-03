
define(['./Gauge.js', './Latency.js','./Progress.js', './Fuel.js' // './Progress_vertical.js',  './Fuel.js'

], function (
    GaugeView,
    LatencyView,
    ProgressBarView,
    //ProgressBarViewVertical,
    FuelBarView
    
) {

    function Gauge() {
        var progress_type = "view.progress-bar";
        //var progress_type_vertival = "view.progress-bar-vertical";
        var fuel_type = "view.fuel-bar";
        var latency_type = "view.latency";
        var gauge_type = "view.gauge";


        return function install(openmct) {
            
            openmct.types.addType(progress_type, {
                name: 'Progress Bar',
                description: 'Progress bars indicates a value visually on a horizontal bar',
                cssClass: "icon-minus",
                creatable: true,
                initialize: function (domain) {
                    domain.composition = [];
                },
                form: [
                    {
                        "key": "value.min",
                        "name": "Min Value",
                        "control": "textfield",
                        "cssClass": "l-input-lg"
                    },
                    {
                        "key": "value.max",
                        "name": "Max Value",
                        "control": "textfield",
                        "cssClass": "l-input-lg"
                    }
                ]
            });
            openmct.objectViews.addProvider({
                key: progress_type,
                name: "Progress Bar View",
                canView: function (domain) {
                    return domain.type === progress_type;
                },
                view: function (domain) {
                    return new ProgressBarView(domain);
                },
                canEdit: function (domain) {
                    return true;
                },
                priority: function () {
                    return 1;
                }
            });

            // openmct.types.addType(progress_type_vertival, {
            //     name: 'Progress Bar Vertical',
            //     description: 'Progress bars indicate visually what percentage of a resource is used on a vertical bar',
            //     cssClass: "icon-minus",
            //     creatable: true,
            //     initialize: function (domain) {
            //         domain.composition = [];
            //     },
            //     form: [
            //         {
            //             "key": "value.min",
            //             "name": "Min Value",
            //             "control": "textfield",
            //             "cssClass": "l-input-lg"
            //         },
            //         {
            //             "key": "value.max",
            //             "name": "Max Value",
            //             "control": "textfield",
            //             "cssClass": "l-input-lg"
            //         }
            //     ]
            // });


            // openmct.objectViews.addProvider({
            //     key: progress_type_vertival,
            //     name: "Progress Bar View vertical",
            //     canView: function (domain) {
            //         return domain.type === progress_type_vertival;
            //     },
            //     view: function (domain) {
            //         return new ProgressBarViewVertical(domain);
            //     },
            //     canEdit: function (domain) {
            //         return false;
            //     },
            //     priority: function () {
            //         return 1;
            //     }
            // });

            openmct.types.addType(fuel_type, {
                name: 'Fuel Bar',
                description: 'Fuel bars indicates in percentage (between max an min value given) how much Fuel is left on a horizontal bar',
                cssClass: "icon-minus",
                creatable: true,
                initialize: function (domain) {
                    domain.composition = [];
                },
                form: [
                    {
                        "key": "value.min",
                        "name": "Min Value",
                        "control": "textfield",
                        "cssClass": "l-input-lg"
                    },
                    {
                        "key": "value.max",
                        "name": "Max Value",
                        "control": "textfield",
                        "cssClass": "l-input-lg"
                    }
                ]
            });
            openmct.objectViews.addProvider({
                key: fuel_type,
                name: "Fuel Bar View",
                canView: function (domain) {
                    return domain.type === fuel_type;
                },
                view: function (domain) {
                    return new FuelBarView(domain);
                },
                canEdit: function (domain) {
                    return true;
                },
                priority: function () {
                    return 1;
                }
            });

            openmct.types.addType(latency_type, {
                name: 'Latency',
                description: 'Gauges indicates a value visually circular dial',
                cssClass: "icon-timer",
                creatable: true,
                initialize: function (domain) {
                    domain.composition = [];
                },
                form: [
                    {
                        "key": "value.min",
                        "name": "Min Value",
                        "control": "textfield",
                        "cssClass": "l-input-lg"
                    },
                    {
                        "key": "value.max",
                        "name": "Max Value",
                        "control": "textfield",
                        "cssClass": "l-input-lg"
                    },
                    {
                        "key": "value.size",
                        "name": "Size (optional, standard is 80)",
                        "control": "textfield",
                        "cssClass": "l-input-lg"
                    }
                ]
            });

            openmct.objectViews.addProvider({
                key: latency_type,
                name: "Latency Gauge",
                canView: function (domain) {
                    return domain.type === latency_type;
                },
                view: function (domain) {
                    return new LatencyView(domain);
                },
                canEdit: function (domain) {
                    return true;
                },
                priority: function () {
                    return 1;
                }
            });

            openmct.types.addType(gauge_type, {
                name: 'Gauge',
                description: 'Gauges indicate visually what percentage of a resource is used on a circular dial',
                cssClass: "icon-timer",
                creatable: true,
                initialize: function (domain) {
                    domain.composition = [];
                },
                form: [
                    {
                        "key": "value.min",
                        "name": "Min Value",
                        "control": "textfield",
                        "cssClass": "l-input-lg"
                    },
                    {
                        "key": "value.max",
                        "name": "Max Value",
                        "control": "textfield",
                        "cssClass": "l-input-lg"
                    },
                    {
                        "key": "value.size",
                        "name": "Size (optional, standard is 80)",
                        "control": "textfield",
                        "cssClass": "l-input-lg"
                    }
                ]
            });

            openmct.objectViews.addProvider({
                key: gauge_type,
                name: "Gauge View",
                canView: function (domain) {
                    return domain.type === gauge_type;
                },
                view: function (domain) {
                    return new GaugeView(domain);
                },
                canEdit: function (domain) {
                    return true;
                },
                priority: function () {
                    return 1;
                }
            });

            console.log("gauge/bar/fuel plugin installed");
        };
    }

    return Gauge;
});
