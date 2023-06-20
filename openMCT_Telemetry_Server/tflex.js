// telemetry source object for the TFLEX demonstrator

const dgram = require('dgram');
const server = dgram.createSocket('udp4');
const fs = require('fs');


server.bind(50011);

function TFlex() {
// Initialize working parameters and objects

//read the keys from dictionary
        let rawDict = fs.readFileSync('../openmct/example/FLEXOP/TFLEXdictionary.json')
        let dict = JSON.parse(rawDict)
        //console.log(dict.measurements.map(obj => obj.key))

        this.state={};
        (dict.measurements.map(obj => obj.key)).forEach(function (k) {
            this.state[k] = 0;
        }, this);
        //console.log(this.state)    
   
    this.history = {}; //history object
    this.listeners = [];
	this.data = []; // temporar data array
	this.continousLogging = false; //whether continous logging is used
	this.FileTimestamp = '';

	// keys initialized in the history object
	Object.keys(this.state).forEach(function (k) {
        this.history[k] = [];
	}, this);


    setInterval(function () {
        //this.generateTelemetryInterval();
    }.bind(this), 100);



	server.on('message', (msg, rinfo) => {
        //parse the data
		this.data = `${msg}`.split(',');
		
		// Check server message
		//console.log(`server got: ${msg} from ${rinfo.address}:${rinfo.port}`)
        //console.log(`server got: ${this.data[8]} from ${rinfo.address}:${rinfo.port}`)
		
		// Error Flags are set before setting the state in order to make a logic to only print them once when set
		if (this.data[0].search('Flag') !== -1){
			this.ErrorFlags("Flag.RxMux1.Autopilot", "RXMUX 1 Autopilot On!");
			this.ErrorFlags("Flag.RxMux1.SPI", "RXMUX 1 SPI communication fail!");      
			this.ErrorFlags("Flag.RxMux1.ECU_PIN", "RXMUX 1 ECU Pin Connected!");   
			this.ErrorFlags("Flag.RxMux1.ECU_PPM", "RXMUX 1 ECU is commanded to turn on!");    
			this.ErrorFlags("Flag.RxMux1.JETI", "RXMUX 1 Reception from Jeti!");    
			this.ErrorFlags("Flag.RxMux1.GRP", "RXMUX 1 Reception from Graupner!");      
			//this.ErrorFlags("Flag.RxMux1.c_JETI", "ECU RxMux1 c_JETI!");   
			//this.ErrorFlags("Flag.RxMux1.c_GRP", "RxMux 1 c_GRP!");

			this.ErrorFlags("Flag.RxMux2.Autopilot", "RXMUX 2 Autopilot On!");
			this.ErrorFlags("Flag.RxMux2.SPI", "RXMUX 2 SPI communication fail!");      
			this.ErrorFlags("Flag.RxMux2.ECU_PIN", "RXMUX 2 ECU Pin Connected!");   
			this.ErrorFlags("Flag.RxMux2.ECU_PPM", "RXMUX 2 ECU is commanded to turn on!");    
			this.ErrorFlags("Flag.RxMux2.JETI", "RXMUX 2 Reception from Jeti!");    
			this.ErrorFlags("Flag.RxMux2.GRP", "RXMUX 2 Reception from Graupner!");      
			//this.ErrorFlags("Flag.RxMux2.c_JETI", "ECU RxMux2 c_JETI!");   
			//this.ErrorFlags("Flag.RxMux2.c_GRP", "RxMux 2 c_GRP!");
			
			this.ErrorFlags("Flag.RxMux3.Autopilot", "RXMUX 3 Autopilot On!");
			this.ErrorFlags("Flag.RxMux3.SPI", "RXMUX 3 SPI communication fail!");      
			this.ErrorFlags("Flag.RxMux3.ECU_PIN", "RXMUX 3 ECU Pin Connected!");   
			this.ErrorFlags("Flag.RxMux3.ECU_PPM", "RXMUX 3 ECU is commanded to turn on!");    
			this.ErrorFlags("Flag.RxMux3.JETI", "RXMUX 3 Reception from Jeti!");    
			this.ErrorFlags("Flag.RxMux3.GRP", "RXMUX 3 Reception from Graupner!");      
			//this.ErrorFlags("Flag.RxMux1.c_JETI", "ECU RxMux1 c_JETI!");   
			//this.ErrorFlags("Flag.RxMux1.c_GRP", "RxMux 1 c_GRP!");

			this.ErrorFlags("Flag.flightHAT.XsensConfigFault", "Xsens Config Fault!");   //49   
			this.ErrorFlags("Flag.flightHAT.XsensUnexpectedConfigAck", "Xsens Unexpected Config Ack!");  //51
			this.ErrorFlags("Flag.flightHAT.XsensConfigChecksumFault", "Xsens Config Checksum Fault!");  //53
			this.ErrorFlags("Flag.flightHAT.XsensConfigReceiveFault", "Xsens Config Receive Fault!");   //55
			this.ErrorFlags("Flag.flightHAT.XsensWrongHeader", "Xsens Wrong Header!");      //57
			this.ErrorFlags("Flag.flightHAT.XsensChecksumFault", "Xsens Checksum Fault!");    //59
			this.ErrorFlags("Flag.flightHAT.XsensDataTypeError", "Xsens Data Type Error!");    //61
			this.ErrorFlags("Flag.flightHAT.XsensUnexpectedByteIndex", "Xsens Unexpected Byte Index!");  //63
			this.ErrorFlags("Flag.flightHAT.XsensUnexpectedDataID", "Xsens Unexpected Data ID!"); //65
			this.ErrorFlags("Flag.flightHAT.ADSConfigFault", "ADS Config Fault!");        //67
			this.ErrorFlags("Flag.flightHAT.ADSChecksumFault", "ADS Checksum Fault!");      //69
			this.ErrorFlags("Flag.flightHAT.ADSTooMuchDataTypes", "ADS Too Much Data Types!");   //71
			this.ErrorFlags("Flag.flightHAT.IMUWrongRequestID", "IMU Wrong Request ID!");     //73
			this.ErrorFlags("Flag.flightHAT.IMUWrongID", "IMU Wrong ID!");            //75
			this.ErrorFlags("Flag.flightHAT.SHMWrongID", "SHM Wrong ID!");            //77
			this.ErrorFlags("Flag.flightHAT.WrongRXMUXChecksum", "Wrong RXMUX Checksum!");   //79
			
			return;
		}

		//Save the data to the state array
		this.state[this.data[0]] = this.data[1];
		this.state['Time.stamp'] = Math.round(this.data[2]*1000); //convert python timestamp[s] to JS timestamp [ms]
		
		//console.log(Date.now()-this.state['Time.stamp']) //check lag incomming
		//console.log(this.state['Time.stamp']) //check Timestamp
		//console.log(this.state[this.data[0]]) //check paylaod
		
		//CALCULATIONS

        
            if (this.data[0] === "Bat.FlightHead"){
                this.state[this.data[0]] = this.data[1]*0.0062;
                //console.log(this.state[this.data[0]])
			}

			if (this.data[0] === "Bat.RX_MUX1" || this.data[0] === "Bat.RX_MUX2" || this.data[0] === "Bat.RX_MUX3"){
                this.state[this.data[0]] = 0.0021 * this.data[1] - 0.1366;
                //console.log(this.state[this.data[0]])
			}

			if (this.data[0] === "xSens.AccX" || this.data[0] === "xSens.AccY" || this.data[0] === "xSens.AccZ"){
                this.state[this.data[0]] = this.data[1]/9.806;
                //console.log(this.state[this.data[0]])
			}

			if (this.data[0] === "xSens.AccZ"){
                this.state[this.data[0]] = -this.data[1]/9.806;
                //console.log(this.state[this.data[0]])
			}

			if (this.data[0] === "shm13.Pos"){
                this.state['Dpos.TailR1'] = Math.abs(this.state[this.data[0]]-this.state['servo_rev.ID13'])
				//console.log(Math.abs(this.state[this.data[0]]-this.state['servo_rev.ID13']))
				var timestamp = this.state['Time.stamp'];
				var message = { timestamp: timestamp, value: this.state['Dpos.TailR1'], id: this.data[0]};
				this.notify(message);
				try{ // store in history
					this.history['Dpos.TailR1'].push(message);
					}
					catch (e) {
						console.log(e)
					}
			}

			if (this.data[0] === 'servo_rev.ID13'){
                this.state['Dpos.TailR1'] = Math.abs(this.state["shm13.Pos"]-this.state[this.data[0]])
				//console.log(this.state[this.data[0]]-this.state["shm13.Pos"])
				var timestamp = this.state['Time.stamp'];
				var message = { timestamp: timestamp, value: this.state['Dpos.TailR1'], id: this.data[0]};
				this.notify(message);
				try{ // store in history
					this.history['Dpos.TailR1'].push(message);
					}
					catch (e) {
						console.log(e)
					}
			}

			
			
			
			
			     
			//console.log(this.data[0])
			//console.log(this.data[1])

        //// to notify telemetry server every time new data arrives in uncomment here
		this.generateRealtimeTelemetry();


		//// Save History on every message, for highest possible resolution
		// Real Timestamp
		var timestamp = this.state['Time.stamp'];
		// Artificial timestamp (if no timestamp is sent)
		//var timestamp= Date.now();

		// built message
		var message = { timestamp: timestamp, value: this.state[this.data[0]], id: this.data[0]};
			try{ // store in history
				this.history[this.data[0]].push(message);
				//console.log(this.history[this.data[0]])
				
				// if continous logging is activated, append message to log file
				if(this.continousLogging){					
		
					//Using Promises for less interrupting the main loop
					this.asyncStringyify(message).then(function(write) {//write is the value of the resolved promise in asyncStringify
						fs.appendFile(__dirname + '/saved_logs/TFlex_'+this.FileTimestamp+'_rawMessage.json', write, (err) => {
							if (err) {
								console.log(err);
							} 
						}) 
					}.bind(this));

				}	
				} catch (e) {
					console.log(e)
				}

	});
	
	server.on('error', (err) => {
		console.log(`TFlex UDP server error:\n${err.stack}`);
		try{
			console.log('Try to reconnect...')
			server.bind(50012);
		} catch(e) {
			console.log('Reconnect Failed...')
			console.log(e)
			server.close()
		}

    });
    console.log("TFLEX initialized!");

};

TFlex.prototype.ErrorFlags = function (key, message) {

	if (this.data[0] === key && this.data[1] === '1' && this.state[this.data[0]] !== message){
		this.state[this.data[0]] = message;
		this.generateTelemetry();
		return true;
	} else if (this.data[0] === key && this.data[1] === '1' && this.state[this.data[0]] === message){
		return true;
	} else if (this.data[0] === key && this.data[1] === '0' && this.state[this.data[0]] !== message){
		return true;
	}else if (this.data[0] === key && this.data[1] === '0' && this.state[this.data[0]] === message){
		this.state[this.data[0]] = this.state[this.data[0]]+' Opposite!';
		this.generateTelemetry();
		return true;
	}else{
		return false;
	}

}



// to update every time new data comes in
TFlex.prototype.generateRealtimeTelemetry = function () {

	// Real Timestamp
	var timestamp = this.state['Time.stamp'];
	// Artificial timestamp
	//var timestamp= Date.now();

	// built message
	var message = { timestamp: timestamp, value: this.state[this.data[0]], id: this.data[0]};
	// notify realtimeserver
	this.notify(message);
	//console.log(message);

}


// to update interval based (STFE)
TFlex.prototype.generateTelemetryInterval = function () {

    Object.keys(this.state).forEach(function (id) {

        // Real Timestamp
		var timestamp = this.state['Time.stamp'];
		// Artificial timestamp
        //var timestamp= Date.now();

		// built message
		var message = { timestamp: timestamp, value: this.state[id], id: id};
		// notify realtimeserver
        this.notify(message);


	}, this);
	//console.log(state);
};


// notifiy function, called in generate Telemetry, notifies listeners
TFlex.prototype.notify = function (point) {
    this.listeners.forEach(function (l) {
        l(point);
    });
};


// manages listeners for realtime telemetry
TFlex.prototype.listen = function (listener) {
    this.listeners.push(listener);
    return function () {
        this.listeners = this.listeners.filter(function (l) {
            return l !== listener;
        });
    }.bind(this);
};

// Creating a File Timestamp 
TFlex.prototype.SetFileTimestamp = function () {

	//zero needed for right time and date format when copy-pasting in OpenMCT
	addZero = function(dateNumber) {
		if (dateNumber.toString().length == 1){
			dateNumber = '0'+dateNumber.toString()
		}
		return dateNumber
	}
	//Generate timestamp for the File
	var date = new Date();
	var year = date.getFullYear();
	var month = addZero(date.getMonth() + 1);      // "+ 1" because the 1st month is 0
	var day = addZero(date.getDate());
	var hour = addZero(date.getHours());
	var minutes = addZero(date.getMinutes());
	var seconds = addZero(date.getSeconds());
	this.FileTimestamp = year+ '-'+ month+ '-'+ day+ ' '+ hour+ '-'+ minutes+ '-'+ seconds;

};

//asynchronous Strigify an object/a variable to JSON format
TFlex.prototype.asyncStringyify = function (obj) {
	return new Promise((resolve, reject) => {
	  resolve(JSON.stringify(obj));
	});
  }


// what to do on incoming command
TFlex.prototype.command = function (command) {

	// Logs the history variable (this.history) once
	if(command === ':saveHistory'){
		
		
		this.SetFileTimestamp()

		//Using Promises for not interrupting the main loop
		function asyncSaveHistory(str) {
			return new Promise((resolve, reject) => {
			  resolve(JSON.stringify(str));
			});
		  }

		this.asyncStringyify(this.history).then(function(write) {//write is the value of the resolved promise in asyncStringify
			fs.writeFile(__dirname + '/saved_logs/TFlex_'+this.FileTimestamp+'_History.json', write, (err) => {
				if (err) {
					console.log(err);
				} else {
				console.log('History Saved!')
				}
			}) 
		}.bind(this));
	
	};


	// Logs the history variable (this.history) every 10s
	// because of the structure of this.history, with the current logic the file has to be rewritten on every save
	// due to this, a lot of performance is needed, especially on long recordings >20min with a lot of data (40 telemetry points @10Hz)
	// not recommended, instead save the history at the end of the test with the "saveHistory" command on log only messages continously, so secure the data

	// if(command === ':startcontinousHistoryLog'){
		
	// 	this.SetFileTimestamp()

	// 	Using Promises for not interrupting the main loop
	// 	function asyncLogging(src) {
	// 		return new Promise((resolve, reject) => {
				
	// 		  resolve(JSON.stringify(src));
	// 		});
	// 	  }
		
	
	// 	save log in specified interval
	// 	logging = setInterval(function () {
	// 		asyncLogging(this.history).then(function(write) {//write is the value of the resolved promise in asyncStringify
	// 			fs.writeFile(__dirname + '/saved_logs/TFlex_'+this.FileTimestam+'.json', write, (err) => {
	// 				if (err) {
	// 					throw err;
	// 				}
	// 				console.log(this.history);
	// 				console.log('Logging!')
	// 			}) 
	// 		}.bind(this));
	// 	}.bind(this), 10000); 
	
			
	// };


	// if(command === ':endContinousHistoryLog'){
	// 	clearInterval(logging);
	// 	console.log('Logging stopped!')	
	// };


	// for continous logging use this method, saved file can not be used in OpenMCT as is, but all data is stored more efficiently 
	if(command === ':startLog'){

		this.SetFileTimestamp()

		this.continousLogging = true;
		console.log('Logging started!')	
	};

	if(command === ':endLog'){
		this.continousLogging = false;
		console.log('Logging stopped!')	
	};


	// Example implementation of sending a command
	if(command === ':exampleCommandtoPlane'){
		// sending to the udp port 60012 on the address 'loacalhost'
		server.send(command,60012, 'localhost')
		console.log('Command Sent via UDP Port!')	
	};

	
};

module.exports = function () {
    return new TFlex()
};
