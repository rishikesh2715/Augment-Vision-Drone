// telemetry source object for the Horyzn project
// not up-to-date but (to the best of my knowledge) also not used anymore
// up to date e.g. DG800.js

const dgram = require('dgram');
const server = dgram.createSocket('udp4');

server.bind(50013);

function Horyzn() {
    this.state = {

        "ATT.roll" : 0,
        "ATT.pitch" : 0,
        "ATT.yaw" : 0,
        "NAV.roll" : 0,
        "NAV.pitch" : 0,
        "Ground.course" : 0,
        "GPS.alt" : 0,
        "GPS.satcount" : 0,
        "Airspeed.calc" : 0,
        "Airspeed.tar" : 0,
        "Groundspeed.calc" : 0,
        "Wind.dir" : 0,
        "Wind.vel" : 0,
        "ACC.X" : 0,
        "ACC.Y" : 0,
        "ACC.Z" : 0,
	    "Mag.X" : 0,
	    "Mag.Y" : 0,
	    "Mag.Z" : 0,
        "Batt.V" : 0,
        "Lidar.alt" : 0,
        "Turn.radius" : 0,
        "Climb.rate" : 0,
        "Turn.rate" : 0,
        "Dist.traveled" : 0,

        "Time.stamp": Date.now()

    };
    this.history = {};
    this.listeners = [];
    this.data = new Array();
    Object.keys(this.state).forEach(function (k) {
        this.history[k] = [];
    }, this);

    setInterval(function () {
        this.generateTelemetry();
    }.bind(this), 100);



    console.log("Horyzn Initialized!");

    server.on('message', (msg, rinfo) => {
        this.data = `${msg}`.split(',');

        //console.log(`server got: ${msg} from ${rinfo.address}:${rinfo.port}`)
        //console.log(`server got: ${this.data[8]} from ${rinfo.address}:${rinfo.port}`)

        this.state["ATT.roll"] = this.data[0];          
        this.state["ATT.pitch"] = this.data[1];         
        this.state["ATT.yaw"] = this.data[2];           
        this.state["NAV.roll"] = this.data[3];          
        this.state["NAV.pitch"] = this.data[4];         
        this.state["Ground.course"] = this.data[5];     
        this.state["GPS.alt"] = this.data[6];                   
        this.state["GPS.satcount"] = this.data[7];      
        this.state["Airspeed.calc"] = this.data[8];     
        this.state["Airspeed.tar"] = this.data[9];     
        this.state["Groundspeed.calc"] = this.data[10]; 
        this.state["Wind.dir"] = this.data[11];         
        this.state["Wind.vel"] = this.data[12];         
        this.state["ACC.X"] = this.data[13]/100;        
        this.state["ACC.Y"] = this.data[14]/100;        
        this.state["ACC.Z"] = this.data[15]/100;        
        this.state["Mag.X"] = this.data[16];            
        this.state["Mag.Y"] = this.data[17];            
        this.state["Mag.Z"] = this.data[18];            
	    this.state["Batt.V"] = this.data[19];           
	    this.state["Lidar.alt"] = this.data[20];        
        this.state["Turn.radius"] = this.data[21];      
        this.state["Climb.rate"] = this.data[22];       
        this.state["Turn.rate"] = this.data[23];
        this.state["Dist.traveled"] = this.data[24];

    });

};



/**
 * Takes a measurement of spacecraft state, stores in history, and notifies
 * listeners.
 */
Horyzn.prototype.generateTelemetry = function () {
    var timestamp = Date.now();
    Object.keys(this.state).forEach(function (id) {
        var state = { timestamp: timestamp, value: this.state[id], id: id};
        this.notify(state);
        console.log(state);
        try{
            this.history[id].push(state);
            }
            catch (e) {
                console.log(e)
            }
        //this.state["comms.sent"] += JSON.stringify(state).length;
    }, this);
};

Horyzn.prototype.notify = function (point) {
    this.listeners.forEach(function (l) {
        l(point);
    });
};

Horyzn.prototype.listen = function (listener) {
    this.listeners.push(listener);
    return function () {
        this.listeners = this.listeners.filter(function (l) {
            return l !== listener;
        });
    }.bind(this);
};

module.exports = function () {
    return new Horyzn()
};
