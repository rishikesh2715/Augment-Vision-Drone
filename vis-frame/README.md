# Visualization Framework

This is a customized implementation of NASA's telemetry visualization tool OpenMCT: https://nasa.github.io/openmct/. It is capable of gathering data from several sources and displaying them in a highly modular and customizable manner.
Several plugins got added to the core application OpenMCT (openmct/example), a telemetry server was implemented to serve OpenMCT and receive data via a UDP port. Furthermore several python scripts were added to feed the telemetry server and ease the implementation of new telemetry sources.
- to start or install OpenMCT: open a command prompt or terminal in /openmct and type `npm start` or `npm install`
- to start or install the telemetry server: open a command promt or terminal in /OpenMCT_Telemetry_Server and type `npm start` or `npm install`
- existing implementations and a generic implementation of python scripts feeding the server can be obtained from /python_scripts

Documentation available under: https://gitlab.lrz.de/lls/vis-frame/-/wikis/home

All changes to the source code can be viewed in the Wiki under "How-to-Install-and-Update-OpenMCT" - "Update OpenMCT to the newest version of NASA": https://gitlab.lrz.de/lls/vis-frame/-/wikis/Home/How-to-Install-and-Update-OpenMCT

# Citation
If you find the introduction and repo useful, you can cite it as follows:

Weber, Marius; Koeberle, Sebastian; Hornung, Mirko: OpenMCT for Engineers. Online available at https://gitlab.lrz.de/lls/vis-frame.


@misc{Weber.2020,  
 author = {Weber, Marius and Koeberle, Sebastian and Hornung Mirko},  
 date = {2020},  
 title = {OpenMCT for Engineers},  
 url = {https://gitlab.lrz.de/lls/vis-frame},  
 institution = {{Institute of Aircraft Design, Technical University of Munich}}  
}