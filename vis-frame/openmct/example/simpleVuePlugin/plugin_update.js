
define(['vue'], //, './Gauge.vue'], //'gauge',

    function (Vue) { //,  GaugeComponent) { //Gauge,

        function SimpleVuePlugin() {
            return function install(openmct) {

                openmct.types.addType('view.JQ', {
                    name: 'JQwidget',
                    cssClass: "icon-box-round-corners",
                    description: 'Provides a sizable map for a object with latitude, longitude and heading',
                    creatable: true,
                    initialize: function (domain) {
                        domain.composition = [];
                    }
                });
                openmct.objectViews.addProvider({
                    name: "view.JQ",
                    key: "JQ",
                    cssClass: "icon-box",
                    canView: function (d) {
                        return d.type === 'view.JQ';
                    },
                    view: function (domain) {
                        var vm;
                        var gaugetemplate = require('./Gauge.vue'); //or HelloWorld or ToDoApp

                        return {
                            show: function (dom) {

                                container = document.createElement("div");
                                container.style.width = "100%";

                                var composition = domain.composition || [];
                                subscriptions = [];
                                subscriptions.length = composition.length;

                                dom.appendChild(container);

                                vm = new Vue(gaugetemplate.default);
                                //vm.coordinates = [11.286146,48.082427];
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

                                            if (typeof (value) === "number" && String(id.key).includes("lon")) {
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
