# Velocity-with-Lidar-and-Raspberry-PI
## Description
log speed in CSV-file with Lidar and Raspberry PI
## Source
(https://github.com/garmin/LIDARLite_RaspberryPi_Library/)

(http://static.garmin.com/pumac/LIDAR_Lite_v3_Operation_Manual_and_Technical_Specifications.pdf )

## Hardware
(https://www.kiwi-electronics.nl/nl/lidar-lite-v3-afstandsmeter-2814 )

(https://www.sparkfun.com/products/14032)


(https://www.sossolutions.nl/raspberry-pi-3a )

(https://www.kiwi-electronics.nl/nl/raspberry-pi-3-model-aplus-3913)


(https://www.sossolutions.nl/raspberry-camera-module-v2 )

(https://www.kiwi-electronics.nl/nl/raspberry-pi-camera-module-2-8mp-2359)


(https://www.allekabels.be/zwakstroom/7375/1052659/abs-behuizing-222x146x75m.html )


(https://www.allekabels.be/condensator/1266/4262/condensator.html )


(https://www.bol.com/be/nl/p/anker-powercore-powerbank-20-100-mah-zwart/9200000074893191/)


## Software
### Python Program
The principal is to measure 2 times a distance in a certain time.
The program takes, with a loop of 1 second, a distance measurement and calculates the difference with the distance of the previous loop.
The LIDAR has a problem with the reflection of mirrors or material like a mirror.
Cars reflect the laser back in a wrong direction, only if you measure the distance in the front of the car, the measurement is correct.
You will get no or bad result if you measure beside the road.
This means this project works only in a road with a curve.
You get a very good result (diffuse reflection) with bikers, even beside the road.

Each second a measurement means :
at a velocity of 60km/h a difference of 17 meter; 
120km/h : 33 meter
The LIDAR works till 40 meter.
It is not possible to measure a higher velocity is without reducing the loop-time of one second.
But less than one second gives more measurement of the same car.

The “velocity” calculated with the module itself, is not accurate.
As it is only one byte, the max speed is 36 km/h.
You can get a higher velocity in reducing the time, but the accuracy is very low.

To check the program and the LIDAR, the program took a picture each second.
After a day I got 54.000 pictures … nice to make a time lapse movie.
But too many pictures !
It’s better to take a picture if there is a car.
Much better if you could take pictures 5 second before it happens and 5 second after it.
So the program keeps always the last 5 pictures in memory.
If the event happens, the program writes first these 5 pictures and writes the next 5 seconds (loop) a picture.
