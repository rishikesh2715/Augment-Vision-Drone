
define([

], function (

) {

    function ButtonPlugin() {

        var button = "button";

        function ButtonView(domain) {
            var container = null;
            this.container = container;

            var label = domain.label || 'Label not defined';

            var command = domain.command || 'console.log("No command!")';

            var historyServer = domain.historyServer;

            function makeButton() {
                var button = document.createElement("div");
                //adaptable siehe ptrogress bar
                button.style.width = "100%";
                button.style.height = "100%";
                button.width;
                button.style.position = "relative";

                var btn = document.createElement("button");
                btn.innerHTML = label;
                btn.classList.add("c-button");
                btn.style.width = "100%";
                btn.style.height = "100%";
                btn.style.fontSize = "14px";
                //btn.style.color =  '#aaaaaa'
                btn.onclick = function () {
                //console.log('fresh meat!')
                    const Http = new XMLHttpRequest();
                    const url = 'http://' + 'localhost' + ':' + '16969' + historyServer + '/command/:' + command;
                    Http.open("POST", url, true);
                    Http.send();
                    Http.onreadystatechange = (e) => {
                        console.log(Http.responseText);
                    };
                };

                button.appendChild(btn);

                // var para = document.createElement("P");               // Create a <p> element
                // para.innerText = "This is a paragraph";               // Insert text
                // button.appendChild(para);

                //console.log("Hi!")

                return {
                    content: button,
                    setLabel: function (text) {
                        title.innerText = text;
                    }
                };

            }

            //makeButton()

            this.show = function (dom) {

                var button = makeButton();
                dom.appendChild(button.content);

            };

            this.destroy = function () {
            // Remove dom
                if (container) {
                    container.remove();
                }

            };

            return this;
        }

        return function install(openmct) {

            openmct.types.addType(button, {
                name: 'Button',
                description: 'Sends custom message to a UDP-Port',
                cssClass: "icon-minus",
                creatable: true,
                initialize: function (domain) {
                    domain.composition = [];
                },
                form: [
                    {
                        "key": "label",
                        "name": "Button Label",
                        "control": "textfield",
                        "cssClass": "l-input-lg"
                    },
                    {
                        "key": "command",
                        "name": "Command",
                        "control": "textfield",
                        "cssClass": "l-input-lg"
                    },
                    {
                        "key": "historyServer",
                        "name": "URL of the history server",
                        "control": "textfield",
                        "cssClass": "l-input-lg"
                    }
                ]
            });

            openmct.objectViews.addProvider({
                key: button,
                name: "Custom Button",
                canView: function (domain) {
                    return domain.type === button;
                },
                view: function (domain) {
                    return new ButtonView(domain);
                },
                canEdit: function (domain) {
                    return false;
                },
                priority: function () {
                    return 1;
                }
            });

            console.log("Button plugin installed");
        };
    }

    return ButtonPlugin;
});
