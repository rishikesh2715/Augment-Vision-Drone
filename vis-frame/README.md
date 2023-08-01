# Visualization Framework

This is a customized implementation of NASA's telemetry visualization tool OpenMCT: https://nasa.github.io/openmct/. It is capable of gathering data from several sources and displaying them in a highly modular and customizable manner.
Several plugins got added to the core application OpenMCT (openmct/example), a telemetry server was implemented to serve OpenMCT and receive data via a UDP port. Furthermore several python scripts were added to feed the telemetry server and ease the implementation of new telemetry sources.
- to start or install OpenMCT: open a command prompt or terminal in /openmct and type `npm start` or `npm install`
- to start or install the telemetry server: open a command promt or terminal in /OpenMCT_Telemetry_Server and type `npm start` or `npm install`
- existing implementations and a generic implementation of python scripts feeding the server can be obtained from /python_scripts

