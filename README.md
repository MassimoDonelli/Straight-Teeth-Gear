# Straight-Teeth-Gear
A simple tool for the design of Straight teeth wheels and gears.
# About the project
Straight-teeth-gear.py is a tool that permits the design of a Straight teeth wheels and gears. The code is written in python3 and it permits to save the wheels geometries in dxf format..


The tool permits the design of the following wheels:
 -------------------------------------------------------------
W   -  Single wheel design you must insert  \\
	1) Pressure angle theta, \\
	2) wheel module m \\
	3) theet number Z\\
	4) axis diameter\\
G  -  Driven and conducted wheels design you must insert:
	1) Transmission ratio R=Z2/Z1
	2) Pressure angle theta, 
	3) wheel module m 
	4) axis diameter

Usage: python3 Source/Straight-teeth-geer.py < Examples/InputGear_Ratio=2_m=2.txt

Output example:
__________________________________
Phase 1 Insert Data
Do you want to design a Gear o a single Wheel (G/W):
G or W:G
Insert the transmission ratio R=Z2/Z1:Insert the pressure angle theta (15°/20°):Normalized gear module: [0.5  0.75 1.   1.25 1.5  1.75 2.   2.25 2.5  2.75 3.   3.25 3.5 ]
Insert the gear module [mm]:Insert the main axis hole diameter [mm]:End ...
__________________________________
Phase 2 Estimates the gear geometry \
Teeth Number of the two wheels (Z1 Driver, Z2 Conducted Wheel): Z1 =  14  Z2 =  42
Transmission Ratio: 3.0
Primary diameter Z1: 35.0
Primary diameter Z2: 105.0
External diameter Z1: 40.0
External diameter Z2: 110.0
Step P: 7.853981633974483
Addendum: 2.5
Dedendum: 3.125
Tooth Heigh: 5.625
Inter axis distance: 70.0
_______________________________________
PRIMITIVE_DIAMETER: 35.0
EXTERNAL_DIAMETER: 40.0
FOOT_DIAMETER: 28.75
BASE_DIAMETER: 32.88924172750679
BETA: 6.428571428571429
DELTA: 0.853958291841252
_______________________________________
PRIMITIVE_DIAMETER: 105.0
EXTERNAL_DIAMETER: 110.0
FOOT_DIAMETER: 98.75
BASE_DIAMETER: 98.66772518252039
BETA: 2.142857142857143
DELTA: 0.8539582918412485
End ...
__________________________________
Do you want to save the CAD of the wheel (Y/N)?
