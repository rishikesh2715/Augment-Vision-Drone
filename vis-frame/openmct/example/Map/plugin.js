
define(['vue'], //, './Gauge.vue'], //'gauge',

    function (Vue) { //,  GaugeComponent) { //Gauge,

        function SimpleVuePlugin() {
            return function install(openmct) {

                openmct.types.addType('view.map', {
                    name: 'Map',
                    cssClass: "icon-box-round-corners",
                    description: 'Provides a sizable map for a object with latitude, longitude and heading',
                    creatable: true,
                    initialize: function (domain) {
                        domain.composition = [];
                    },
                    form: [
                        {
                            "key": "init.lat",
                            "name": "Latitude Center of Map",
                            "control": "textfield",
                            "cssClass": "l-input-lg"
                        },
                        {
                            "key": "init.lng",
                            "name": "Longitude Center of Map",
                            "control": "textfield",
                            "cssClass": "l-input-lg"
                        }
                    ]
                });
                openmct.objectViews.addProvider({
                    name: "view.map",
                    key: "map",
                    cssClass: "icon-box",
                    canView: function (d) {
                        return d.type === 'view.map';
                    },
                    view: function (domain) {
                        var vm;
                        var gaugetemplate = require('./map.vue'); //or HelloWorld or ToDoApp

                        return {
                            show: function (dom) {

                                container = document.createElement("div");
                                container.style.width = "100%";

                                var composition = domain.composition || [];
                                subscriptions = [];
                                subscriptions.length = composition.length;

                                dom.appendChild(container);

                                vm = new Vue(gaugetemplate.default);
                                var init_lat = domain["init.lat"] || 48.082427;
                                if (typeof (init_lat) === "string") {
                                    init_lat = parseFloat(init_lat);
                                };
                                
                                var init_lng = domain["init.lng"] || 11.286146;
                                if (typeof (init_lng) === "string") {
                                    init_lng = parseFloat(init_lng);
                                };
                                vm.coordinates = [init_lng,init_lat];
                                //vm.coordinates[0] = 11.286146;
                                //vm.rotatePlane = "";

                                composition.forEach((id, index) => {
                                    // var gauge = makeGauge(id.key);
                                    // console.log(index)
                                    // container.appendChild(gauge.content);

                                    openmct.objects.get(id).then(function (cDomain) {
                                        var allTelemetry = [];
                                        if (cDomain.telemetry && cDomain.telemetry.values) {
                                            allTelemetry = cDomain.telemetry.values.filter((value) => value.format === "float");
                                        }

                                        var first = (allTelemetry.length > 0) ? allTelemetry[0] : null;

                                        subscriptions[index] = openmct.telemetry.subscribe(cDomain, function (data) {
                                            if (!first) {
                                                return;
                                            }

                                            var value = data[first.source || first.key];
                                            //console.log(String(id.key).includes("gps"))
                                            if (typeof (value) === "string") {
                                                value = parseFloat(value);
                                            }

                                            if (typeof (value) === "number" && String(id.key).includes("lat")) {
                                                vm.lat = value;
                                                
                                                //console.log(value)

                                            }

                                            if (typeof (value) === "number" && String(id.key).includes("lng")) {
                                                vm.lon = value;
                                                
                                                //console.log(value)
                                            }

                                            if (typeof (value) === "number" && String(id.key).includes("heading")) {
                                                vm.rotatePlane = value;
                                            }
                                        });
                                    });
                                });

                                dom.appendChild(vm.$mount().$el);
                            },
                            destroy: function (domain) {
                                vm.$destroy();
                            }
                        };
                    }
                });

            };

        }

        return SimpleVuePlugin;

    });
