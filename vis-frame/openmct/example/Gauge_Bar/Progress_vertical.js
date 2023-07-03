define([

], function (

) {

function ProgressBarVerticalView(domain) {
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

        var bar = createProgressBar();        
        box.appendChild(bar.content);
              
        // var ticks = createTicks();
        // bar.content.style.transform = "rotate(-90deg)"
        // box.appendChild(ticks.content);

        tblBody.appendChild(row)
        tblBody.appendChild(row2)

        
        return {
            content: tblBody,
            progress: bar,
            setLabel: function (text) {
                head.innerText = text;
            },
            setValue(value) {
                valuebox.innerText = Math.round((value + Number.EPSILON) * 100) / 100;
                
            }
        };
    }

    function createTicks() {
        var container = document.createElement("div");
        container.style.height = "100%";
        container.style.width = "10px";
        container.style.textAlign = "center"
        container.style.fontSize = "12px";
        container.style.color = "C0C0C0";
        
        var tag1 = document.createElement("div");
        tag1.innerText = min.toString();
        tag1.style.position = "relative";
        tag1.style.float = "top"
        tag1.style.width = "15%";
        tag1.style.textAlign = "top"
        container.appendChild(tag1);
        
        var tag2 =  document.createElement("div");
        tag2.innerText = (min+(max-min)*0.25).toString()
        tag2.style.position = "relative";
        tag2.style.float = "top"
        tag2.style.width = "23%";
        container.appendChild(tag2);

        var tag3 =  document.createElement("div");
        tag3.innerText = (min+(max-min)*0.5).toString()
        tag3.style.position = "relative";
        //tag3.style.left = "50%"
        tag3.style.float = "top"
        tag3.style.width = "23%";
        container.appendChild(tag3);

        var tag4 =  document.createElement("div");
        tag4.innerText = (min+(max-min)*0.75).toString()
        tag4.style.position = "relative";
        //tag4.style.left = "50%"
        tag4.style.float = "top"
        tag4.style.width = "23%";
        container.appendChild(tag4);

        var tag5 =  document.createElement("div");
        tag5.innerText = max.toString();
        tag5.style.position = "relative";
        //tag5.style.left = "100%"
        tag5.style.float = "top"
        tag5.style.width = "15%";
        tag5.style.textAlign = "bottom"
        container.appendChild(tag5);

        return {
            content: container,
        };
    }

    function createProgressBar() {
        var bar = document.createElement("div");
        
        bar.style.width = "100%";
        bar.style.height = "30px";
        bar.style.display = "block";
        bar.style.position = "relative";
        bar.style.transform = "rotate(-90deg)"  
        bar.classList.add("plot-display-area");

        var percentage = document.createElement("progress");
        percentage.style.width = "0%";
        percentage.style.height = "100%";
        percentage.style.padding = "0";
        
        //percentage.style.transform = "rotate(-90deg)"        
        bar.appendChild(percentage);
       
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
                //percentage.innerText = Math.round(float) + "%";
                //percentage.value = float*100
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

return ProgressBarVerticalView

});