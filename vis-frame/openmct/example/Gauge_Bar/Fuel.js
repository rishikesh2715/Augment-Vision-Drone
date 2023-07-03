define([

], function (

) {

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

        var tblBody = document.createElement("tblBody");

        var row = document.createElement("tr");
        row.style.width = "100%";
        var head = document.createElement("td");
        head.innerText = name;
        head.style.fontsize = "14px";
        head.style.color = "#34B6F7";
        head.style.width = "1%"
        head.style.verticalAlign = "middle"
        row.appendChild(head);

        var row2 = document.createElement("tr");
        row2.style.width = "100%";

        var valuebox = document.createElement("td");
        valuebox.id = "Value";
        valuebox.innerText = 0;
        valuebox.style.fontSize = "20px";
        //valuebox.style.color = "#E0E0E0";
        valuebox.style.width = "1%"
        //valuebox.style.fontWeight = "bold"
        valuebox.style.textAlign = "center"
        valuebox.style.verticalAlign = "middle"
        row2.appendChild(valuebox);

        var box = document.createElement("td");
        row2.appendChild(box);

        var bar = createFuelBar();
        box.appendChild(bar.content);

        tblBody.appendChild(row)
        tblBody.appendChild(row2)

        return {
            content: tblBody,
            progress: bar,
            setLabel: function (text) {
                head.innerText = text;
            },
            setValue(value) {
                
                valuebox.innerText = (100 - (Math.round( (getPercentOf(value)+ Number.EPSILON) * 100) / 100)*100).toString() + '%'
                
            }
        };
    }

    function createFuelBar() {
        var bar = document.createElement("div");
        bar.style.width = "100%";
        bar.style.height = "30px";
        bar.classList.add("plot-display-area");

        var percentage = document.createElement("progress");
        percentage.style.width = "0%";
        percentage.style.height = "100%";
        percentage.style.padding = "0";        
        bar.appendChild(percentage);

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
                //percentage.innerText = Math.round(float) + "%";
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
            var row = createRow(domain.name);
            container.appendChild(row.content);

            openmct.objects.get(id).then(function (cDomain) {
                var allTelemetry = [];
                if (cDomain.telemetry && cDomain.telemetry.values) {
                    allTelemetry = cDomain.telemetry.values.filter((value) => value.format === "float"|| value.format === "integer");
                }

                var first = (allTelemetry.length > 0) ? allTelemetry[0] : null;

                subscriptions[index] = openmct.telemetry.subscribe(cDomain, function (data) {
                    if (!first) {
                        return;
                    }

                    row.progress.setNormalizedPercent(getPercentOf(data[first.source || first.key]));

                    var value = data[first.source || first.key];
                    if (typeof (value) === "string") {
                        value = parseFloat(value);
                    }

                    if (typeof (value) === "number") {
                        row.setValue(value);
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

return FuelBarView

});