define([

], function (

) {
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

            var size= domain["value.size"] || 80;
            if (typeof (size) === "string") {
                size = parseFloat(size);
            }


            function getPercentOf(value) {
                return (value - min_value) / (max_value - min_value);
            }

            function makeGauge(name) {

                var gauge = document.createElement("div");
                gauge.style.display = "inline-block";
                gauge.style.position = "relative";

                var canvas = document.createElement("canvas");
                var radius = size;
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
                             console.log(`date: ${Date.now()}`)
                             console.log(`value: ${value}`)
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
                            allTelemetry = cDomain.telemetry.values.filter((value) => value.format === "float"|| value.format === "integer");
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

        return LatencyView

});