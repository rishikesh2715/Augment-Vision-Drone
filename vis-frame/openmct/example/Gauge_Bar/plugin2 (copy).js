
define([

], function (

) {

    function Gauge() {
        var progress_type = "view.progress-bar";
        var fuel_type = "view.fuel-bar";
        var latency_type = "view.latency";
        var gauge_type = "view.gauge";

        function ProgressBarView(domain) {
            var container = null;

            var subscriptions = null;

            var min = domain["value.min"] || 0;
            if (typeof (min) === "string") {
                min = parseFloat(min);
            }

            var max = domain["value.max"] || 1;
            if (typeof (max) === "string") {
                max = parseFloat(max);
            }

            function getPercentOf(value) {
                return (value - min) / (max - min);
            }

            function createRow(name) {
                var row = document.createElement("tr");
                row.style.width = "100%";
                var head = document.createElement("td");
                head.innerText = name;
                head.style.fontsize = "14px";
                head.style.color = "#34B6F7";
                row.appendChild(head);

                var box = document.createElement("td");
                box.colSpan = "2";
                row.appendChild(box);

                var bar = createProgressBar();
                box.appendChild(bar.content);

                return {
                    content: row,
                    progress: bar,
                    setLabel: function (text) {
                        head.innerText = text;
                    }
                };
            }

            function createProgressBar() {
                var bar = document.createElement("div");
                bar.style.width = "100%";
                bar.style.height = "30px";
                bar.classList.add("plot-display-area");

                var percentage = document.createElement("div");
                bar.appendChild(percentage);
                percentage.classList.add("c-button");
                //percentage.classList.add("c-button--major");
                percentage.style.background = "#E0E0E0";
                percentage.style.fontsize = "14px";
                percentage.style.color = "#000000";
                percentage.style.width = "0%";
                percentage.style.height = "100%";
                percentage.style.padding = "0";

                return {
                    content: bar,
                    setPercent(float) {
                        var width = float;
                        if (width > 100) {
                            width = 100;
                        } else if (width < 0) {
                            width = 0;
                        }

                        percentage.style.width = width + "%";
                        percentage.innerText = Math.round(float) + "%";
                    },
                    setNormalizedPercent(float) {
                        if (!float) {
                            float = 0;
                        }

                        this.setPercent(float * 100);
                    }
                };
            }

            this.show = function (dom) {
                container = document.createElement("table");
                container.style.width = "100%";

                var composition = domain.composition || [];
                subscriptions = [];
                subscriptions.length = composition.length;
                dom.appendChild(container);

                composition.forEach((id, index) => {
                    var row = createRow(id.key);
                    container.appendChild(row.content);

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

                            row.progress.setNormalizedPercent(getPercentOf(data[first.source || first.key]));
                        });
                    });
                });
            };

            this.destroy = function () {
            // Remove dom
                if (container) {
                    container.remove();
                }

                // Unsubscribe
                if (subscriptions != null) {
                    for (var i = 0; i < subscriptions.length; i++) {
                        if (subscriptions[i]) {
                            subscriptions[i]();
                        }
                    }

                    subscriptions = null;
                }
            };

            return this;
        }

        function FuelBarView(domain) {
            var container = null;

            var subscriptions = null;

            var min = domain["value.min"] || 0;
            if (typeof (min) === "string") {
                min = parseFloat(min);
            }

            var max = domain["value.max"] || 1;
            if (typeof (max) === "string") {
                max = parseFloat(max);
            }

            function getPercentOf(value) {
                return (value - min) / (max - min);
            }

            function createRow(name) {
                var row = document.createElement("tr");
                row.style.width = "100%";
                var head = document.createElement("td");
                head.innerText = name;
                row.appendChild(head);

                var box = document.createElement("td");
                row.appendChild(box);

                var bar = createFuelBar();
                box.appendChild(bar.content);

                return {
                    content: row,
                    progress: bar,
                    setLabel: function (text) {
                        head.innerText = text;
                    }
                };
            }

            function createFuelBar() {
                var bar = document.createElement("div");
                bar.style.width = "100%";
                bar.style.height = "30px";
                bar.classList.add("plot-display-area");

                var percentage = document.createElement("div");
                bar.appendChild(percentage);
                percentage.classList.add("c-button");
                percentage.classList.add("c-button--major");
                percentage.style.width = "0%";
                percentage.style.height = "100%";
                percentage.style.padding = "0";

                return {
                    content: bar,
                    setPercent(float) {
                        var width = float;
                        if (width > 100) {
                            width = 0;
                        } else if (width < 0) {
                            width = 100;
                        }

                        percentage.style.width = width + "%";
                        percentage.innerText = Math.round(float) + "%";
                    },
                    setNormalizedPercent(float) {
                        if (!float) {
                            float = 100;
                        }

                        this.setPercent(100 - float * 100);
                    }
                };
            }

            this.show = function (dom) {
                container = document.createElement("table");
                container.style.width = "100%";

                var composition = domain.composition || [];
                subscriptions = [];
                subscriptions.length = composition.length;
                dom.appendChild(container);

                composition.forEach((id, index) => {
                    var row = createRow(id.key);
                    container.appendChild(row.content);

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

                            row.progress.setNormalizedPercent(getPercentOf(data[first.source || first.key]));
                        });
                    });
                });
            };

            this.destroy = function () {
            // Remove dom
                if (container) {
                    container.remove();
                }

                // Unsubscribe
                if (subscriptions != null) {
                    for (var i = 0; i < subscriptions.length; i++) {
                        if (subscriptions[i]) {
                            subscriptions[i]();
                        }
                    }

                    subscriptions = null;
                }
            };

            return this;
        }

        function LatencyView(domain) {
            var container = null;
            this.container = container;
            var counter = 0;
            var latency = 0;

            var min_value = domain["value.min"] || 0;
            if (typeof (min_value) === "string") {
                min_value = parseFloat(min_value);
            }

            var max_value = domain["value.max"] || 1;
            if (typeof (max_value) === "string") {
                max_value = parseFloat(max_value);
            }

            function getPercentOf(value) {
                return (value - min_value) / (max_value - min_value);
            }

            function makeGauge(name) {

                var gauge = document.createElement("div");
                gauge.style.display = "inline-block";
                gauge.style.position = "relative";

                var canvas = document.createElement("canvas");
                var radius = 80;
                var outerLineThickness = 15;
                var innerLineThickness = 6;
                canvas.width = 2 * radius + 2 * outerLineThickness;
                canvas.height = radius + 2 * outerLineThickness;
                var centre = {
                    x: canvas.width / 2,
                    y: canvas.height - outerLineThickness
                };
                var context = canvas.getContext("2d");
                gauge.appendChild(canvas);

                function redraw(percent) {
                // Setup
                    context.lineCap = "round";
                    context.font = '24px verdana';
                    context.textAlign = 'center';
                    context.textBaseline = 'middle';
                    context.fillStyle = "gray";
                    context.clearRect(0, 0, canvas.width, canvas.height);

                    // Draw full outline
                    context.beginPath();
                    context.arc(centre.x, centre.y, radius, Math.PI, 0, false),
                    context.strokeStyle = 'lightgray';
                    context.lineWidth = outerLineThickness;
                    context.stroke();

                    // Draw fill percentage
                    if (percent > 0) {
                        context.beginPath();
                        context.arc(centre.x, centre.y, radius, Math.PI, (-Math.PI) * (1 - percent), false),
                        context.strokeStyle = 'red';
                        context.lineWidth = innerLineThickness;
                        context.stroke();
                    }
                }

                redraw(0);

                // Draw text
                var row = document.createElement("tr");

                var min = document.createElement("td");
                min.innerText = min_value;
                min.style.textAlign = "left";
                row.appendChild(min);

                var title = document.createElement("td");
                title.innerText = name;
                title.style.textAlign = "center";
                title.style.color = "#34B6F7";
                row.appendChild(title);

                var max = document.createElement("td");
                max.innerText = max_value;
                max.style.textAlign = "right";
                row.appendChild(max);

                var bottom = document.createElement("table");
                bottom.appendChild(row);
                gauge.appendChild(bottom);

                var valuebox = document.createElement("div");
                valuebox.innerText = 0;
                valuebox.style.paddingTop = radius + "px";
                valuebox.style.verticalAlign = "bottom";
                valuebox.style.font = '24px verdana';
                valuebox.style.textAlign = "center";
                valuebox.style.position = "absolute";
                valuebox.style.left = 0;
                valuebox.style.right = 0;
                valuebox.style.top = 0;
                valuebox.style.bottom = 0;
                gauge.appendChild(valuebox);

                return {
                    content: gauge,
                    setLabel: function (text) {
                        title.innerText = text;
                    },
                    setValue(value) {
                        latency = latency + Date.now() - value;
                        if (counter === 10) {
                            latency = latency / 10;
                            //difference between timestamp and printing time
                            // console.log(`date: ${Date.now()}`)
                            // console.log(`value: ${value}`)
                            console.log(`latency: ${latency}`);
                            valuebox.innerText = Math.round((latency + Number.EPSILON) * 100) / 100;

                            var percentage = getPercentOf(latency);
                            if (percentage < 0) {
                                percentage = 0;
                            } else if (percentage > 1) {
                                percentage = 1;
                            }

                            redraw(percentage);

                            counter = 0;
                            latency = 0;
                        }

                        counter = counter + 1;
                        console.log(counter);
                    }
                };
            }

            var subscriptions = null;

            this.show = function (dom) {
                container = document.createElement("div");
                var composition = domain.composition || [];
                subscriptions = [];
                subscriptions.length = composition.length;
                dom.appendChild(container);

                composition.forEach((id, index) => {
                    var gauge = makeGauge(id.key);
                    //console.log(index)
                    container.appendChild(gauge.content);

                    openmct.objects.get(id).then(function (cDomain) {
                        var allTelemetry = [];
                        if (cDomain.telemetry && cDomain.telemetry.values) {
                            allTelemetry = cDomain.telemetry.values.filter((value) => value.format === "float");
                            console.log(cDomain.telemetry.values.filter((utc) => utc.format === "utc"));
                        }

                        var first = (allTelemetry.length > 0) ? allTelemetry[0] : null;

                        subscriptions[index] = openmct.telemetry.subscribe(cDomain, function (data) {
                            if (!first) {
                                return;
                            }

                            var value = data[first.source || first.key];
                            if (typeof (value) === "string") {
                                value = parseFloat(value);
                            }

                            if (typeof (value) === "number") {
                            //value = (Date.now() - value);
                                gauge.setValue(value);
                            }
                        });
                    });
                });
            };

            this.destroy = function () {
            // Remove dom
                if (container) {
                    container.remove();
                }

                // Unsubscribe
                if (subscriptions != null) {
                    for (var i = 0; i < subscriptions.length; i++) {
                        if (subscriptions[i]) {
                            subscriptions[i]();
                        }
                    }

                    subscriptions = null;
                }
            };

            return this;
        }

        function GaugeView(domain) {
            var container = null;
            this.container = container;

            var min_value = domain["value.min"] || 0;
            if (typeof (min_value) === "string") {
                min_value = parseFloat(min_value);
            }

            var max_value = domain["value.max"] || 1;
            if (typeof (max_value) === "string") {
                max_value = parseFloat(max_value);
            }

            function getPercentOf(value) {
                return (value - min_value) / (max_value - min_value);
            }

            function makeGauge(name) {
                var gauge = document.createElement("div");
                gauge.style.display = "inline-block";
                gauge.style.position = "relative";

                var canvas = document.createElement("canvas");
                var radius = 80;
                var outerLineThickness = 15;
                var innerLineThickness = 6;
                canvas.width = 2 * radius + 2 * outerLineThickness;
                canvas.height = radius + 2 * outerLineThickness;
                var centre = {
                    x: canvas.width / 2,
                    y: canvas.height - outerLineThickness
                };
                var context = canvas.getContext("2d");
                gauge.appendChild(canvas);

                function redraw(percent) {
                // Setup
                    context.lineCap = "round";
                    context.font = '24px verdana';
                    context.textAlign = 'center';
                    context.textBaseline = 'middle';
                    context.fillStyle = "#010101";
                    context.clearRect(0, 0, canvas.width, canvas.height);

                    // Draw full outline
                    context.beginPath();
                    context.arc(centre.x, centre.y, radius, Math.PI, 0, false),
                    context.strokeStyle = '#202020';
                    context.lineWidth = outerLineThickness;
                    context.stroke();

                    // Draw fill percentage
                    if (percent > 0) {
                        context.beginPath();
                        context.arc(centre.x, centre.y, radius, Math.PI, (-Math.PI) * (1 - percent), false),
                        context.strokeStyle = 'white';
                        context.lineWidth = innerLineThickness;
                        context.stroke();
                    }
                }

                redraw(0);

                // Draw text
                var row = document.createElement("tr");

                var min = document.createElement("td");
                min.innerText = min_value;
                min.style.textAlign = "left";
                row.appendChild(min);

                var title = document.createElement("td");
                title.innerText = name;
                title.style.textAlign = "center";
                title.style.color = "#34B6F7";
                row.appendChild(title);

                var max = document.createElement("td");
                max.innerText = max_value;
                max.style.textAlign = "right";
                row.appendChild(max);

                var bottom = document.createElement("table");
                bottom.appendChild(row);
                gauge.appendChild(bottom);

                var valuebox = document.createElement("div");
                valuebox.innerText = 0;
                valuebox.style.paddingTop = radius + "px";
                valuebox.style.verticalAlign = "bottom";
                valuebox.style.font = '24px verdana';
                valuebox.style.textAlign = "center";
                valuebox.style.position = "absolute";
                valuebox.style.left = 0;
                valuebox.style.right = 0;
                valuebox.style.top = 0;
                valuebox.style.bottom = 0;
                gauge.appendChild(valuebox);

                return {
                    content: gauge,
                    setLabel: function (text) {
                        title.innerText = text;
                    },
                    setValue(value) {
                        valuebox.innerText = Math.round((value + Number.EPSILON) * 100) / 100;

                        var percentage = getPercentOf(value);
                        if (percentage < 0) {
                            percentage = 0;
                        } else if (percentage > 1) {
                            percentage = 1;
                        }

                        redraw(percentage);
                    }
                };
            }

            var subscriptions = null;

            this.show = function (dom) {
                container = document.createElement("div");
                var composition = domain.composition || [];
                subscriptions = [];
                subscriptions.length = composition.length;
                dom.appendChild(container);
                //console.log(compostition.)

                composition.forEach((id, index) => {
                    var gauge = makeGauge(id.key);
                    //console.log(id.getName())
                    container.appendChild(gauge.content);

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
                            if (typeof (value) === "string") {
                                value = parseFloat(value);
                            }

                            if (typeof (value) === "number") {
                                gauge.setValue(value);
                            }
                        });
                    });
                });
            };

            this.destroy = function () {
            // Remove dom
                if (container) {
                    container.remove();
                }

                // Unsubscribe
                if (subscriptions != null) {
                    for (var i = 0; i < subscriptions.length; i++) {
                        if (subscriptions[i]) {
                            subscriptions[i]();
                        }
                    }

                    subscriptions = null;
                }
            };

            return this;
        }

        return function install(openmct) {
            openmct.types.addType(progress_type, {
                name: 'Progress Bar',
                description: 'Progress bars indicate visually what percentage of a resource is used on a horizontal bar',
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
                    return false;
                },
                priority: function () {
                    return 1;
                }
            });

            openmct.types.addType(fuel_type, {
                name: 'Fuel Bar',
                description: 'Fuel bars indicate visually what percentage of Fuel is left on a horizontal bar',
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
                    return false;
                },
                priority: function () {
                    return 1;
                }
            });

            openmct.types.addType(latency_type, {
                name: 'Latency',
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
                    return false;
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
                    return false;
                },
                priority: function () {
                    return 1;
                }
            });

            console.log("gauge plugin installed");
        };
    }

    return Gauge;
});
