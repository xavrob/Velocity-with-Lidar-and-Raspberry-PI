# Velocity-with-Lidar-and-Raspberry-PI
## Description
log speed in CSV-file with Lidar and Raspberry PI
## Source
(https://github.com/garmin/LIDARLite_RaspberryPi_Library/)

(https://circuitpython.readthedocs.io/projects/lidarlite/en/latest/api.html )

(https://github.com/adafruit/Adafruit_CircuitPython_LIDARLite )

(http://static.garmin.com/pumac/LIDAR_Lite_v3_Operation_Manual_and_Technical_Specifications.pdf )

## Hardware
https://www.kiwi-electronics.nl/nl/lidar-lite-v3-afstandsmeter-2814 

https://www.sparkfun.com/products/14032
## Software
### Python Program
The principal is to measure 2 times a distance in a certain time.
So each second one measurement and make the difference with the distance of the previous loop.
The LIDAR has a problem with the reflection of mirrors or material like a mirror.
Cars reflect the laser back, only if you measure the distance in the front of the car, otherwise the laser reflect in another direction.
You will get no or bad result if you measure beside the road.
This means this project works only in a road with a curve.
You get a very good result (diffuse reflection) with bikers, even beside the road.

Each second a measurement means :
at a velocity of 60km/h a difference of 17 meter
120km/h : 33 meter
The LIDAR works till 40 meter.
An higher velocity is not possible to measure, without reducing the loop-time of one second.
But less than one second gives more measurement of the same car.

The velocity calculated with the module himself, is not accurate.
As it is only one byte, the max speed is 36 km/h.
You can get an higher velocity in reducing the time, but the accuracy is very low.
