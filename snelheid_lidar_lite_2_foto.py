# snelheid_lidar_lite_2_foto.py           21-03-2022
# https://raw.githubusercontent.com/Sanderi44/Lidar-Lite/master/python/lidar_lite.py
# sander.idelson@gmail.com
# https://www.sanderbot.com/
# https://github.com/Sanderi44/Lidar-Lite
# https://github.com/Sanderi44/Lidar-Lite/blob/master/python/lidar_lite.py
# https://github.com/Sanderi44/Lidar-Lite/find/master
# https://picamera.readthedocs.io/en/release-1.10/_modules/picamera/camera.html
#
# stop motion animatie
# ffmpeg -r 10 -i Animatie/Beeld%04d.jpg Animatie.mp4
# %04d is het maximum toegelaten, dus 0001 t/m 9999
#
# bij 120km/u = 33meter/sec
# indien men om de 5 meter een meting wenst
# moet er om de 0,15sec een meting gedaan worden
#
# indien de snelheid > 25km/u mag men 1 sec pause nemen
# anders gaat men dezelfde wagen 2 x loggen
# < 25km/u zijn fietsers
########################################################################
# Onopvallend verloopt de opname niet. 
# Bij elke opname wordt een rode led op de Pi Camera actief, dit valt enorm op. 
# Deze led kan je uitschakelen in het configuratiebestand 
#      sudo nano /boot/config.txt van de Raspberry Pi. 
# Open als systeembeheerder dit configuratiebestand 
# en voeg de volgende regel toe:

#      disable_camera_led=1
# 
# Sla de aanpassing op en herstart de Pi om de nieuwe instelling te activeren. 
# Test of alles nog werkt.
########################################################################
# werkt samen met lidar_lite_2.py
from lidar_lite_2 import Lidar_Lite
import time
import tijd
#import snelheid_2
from picamera import PiCamera
# https://picamera.readthedocs.io/en/release-1.13/
import RPi.GPIO as GPIO
# https://picamera.readthedocs.io/en/release-1.10/recipes1.html#capturing-to-a-pil-image 
import io
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

############################################

def foto(volgnr):
    global fotonaam1
    global fotonaam2
    global foto_annot
    t = time.localtime()
    jaar = t[0]
    maand = t[1]
    dag = t[2]
    uur = t[3]
    minu = t[4]
    sec = t[5]
    u = t[3]
    jjjjmmdd = str(jaar) + str(f'{maand:02d}') + str(f'{dag:02d}')
#                    print(jjjjmmdd)
    uu = str(f'{uur:02d}') 
#                    print(uumm)
    uummss = uu + str(f'{minu:02d}') + str(f'{sec:02d}')
#                    print(uummss)
    fotonaam1 = '/home/pi/Pictures/foto-'
    print(fotonaam1)
#    fotonaam2 = jjjjmmdd + '-' + uu + '-' + str(f'{volgnr:04d}') + '.jpg' 
    fotonaam2 = jjjjmmdd + '-' + uu + '-'  
    print(fotonaam2)
    foto_annot = jjjjmmdd + '-' + uummss + '-' + str(f'{volgnr:05d}') + '.jpg' 
    print(foto_annot)

def berekening_datum():    # wordt enkel gebruikt in print
    t = time.localtime()
    jaar = t[0]
    maand = t[1]
    dag = t[2]
    uur = t[3]
    minu = t[4]
    sec = t[5]
    u = t[3]
    jjjj_mm_dd = str(jaar) + '-' + str(f'{maand:02d}') + '-' + str(f'{dag:02d}')
#                    print(jjjjmmdd)
    uu_mm_ss = str(f'{uur:02d}') + ':' + str(f'{minu:02d}') + ':' + str(f'{sec:02d}')
#                    print(uummss)
    datum = jjjj_mm_dd + ' ' + uu_mm_ss
    return datum

def writeCSV(distance2,distance1,velocity2,velocity2_km_uur,snelheid_km_uur,tijd_verschil):
    tijdnu = int(time.time())
    tijddag=[0,0,0]
    tijd.u_dag(tijddag)
#        uur        = tijddag[0]
#        combinatie = tijddag[1]
#        dag        = tijddag[2]
#
#
    tijd_v = round(tijd_verschil,5)
    tijd_v_US = str(tijd_v)
    tijd_v_BE = tijd_v_US.replace(".",",")
#
    veloc = round(velocity2_km_uur,2)
    veloc_US = str(veloc)
    veloc_BE = veloc_US.replace(".",",")
#
    snelh = round(snelheid_km_uur,2)
    snelh_US = str(snelh)
    snelh_BE = snelh_US.replace(".",",")
#
    csvBestand = open('/home/pi/CSV/snelheid_lidar_lite_2.csv','a')
    csvBestand.write('%s;%s;%s;%s;%s;%s;%s;%s   \n' %
                          (tijdnu,       # ???????????????
                           tijddag[1],
                           distance2,distance1,velocity2,veloc_BE,snelh_BE,tijd_v_BE
                           ))
    csvBestand.close()


# CSV-titel
csvBestand = open('/home/pi/CSV/snelheid_lidar_lite_2.csv','a')
csvBestand.write('PC-tijd;jmd;week;dag;ums;jmdums;distance2;distance1;0.1m-per-sec;velocity2_km_uur;snelheid_km_uur;tijd_verschil \n')
csvBestand.close()
#

fotonaam1 = ' '
fotonaam2 = ' '
fotonaam  = ' '
distance1 = 0
distance2 = 0
afstanden = ' '
velocity1 = 0
velocity2 = 0
velocity22 = 0
tijd1 = time.time()
tijd2 = time.time()
tijd3 = time.time()
tijd1 = 0
tijd2 = 0
tijd3 = 0
tijd_verschil_tot = time.time()
tijd_verschil_tot = 0
teller = 0
snelheid = 0
volgnr = 0
uu_mm = ' '
uur   = ' '
auto = 0
kopie = 0

# met Sanderi44/Lidar-Lite
lidar = Lidar_Lite()
connected = lidar.connect(1)

print(connected)

# met Sanderi44/Lidar-Lite
if connected < -1:
  print("Not Connected")

time.sleep(1)

############################################

#startcamera()
#def startcamera():
############################################
# Use GPIO numbering
GPIO.setmode(GPIO.BCM)
# Set GPIO for camera LED
# Use 5 for Model A/B and 32 for Model B+
CAMLED = 5 
# Set GPIO to output
GPIO.setup(CAMLED, GPIO.OUT, initial=False) 
# 2 iterations with half a second
# between on and off
GPIO.output(CAMLED,True) # On
time.sleep(0.5)
GPIO.output(CAMLED,False) # Off
time.sleep(0.5)
GPIO.output(CAMLED,True) # On
time.sleep(0.5)
GPIO.output(CAMLED,False) # Off
time.sleep(0.5)
#
camera = PiCamera()
# camera.rotation = 180
camera.resolution = (1024, 768)
# camera.resolution = (648, 486)
# camera.resolution = (324, 243)
camera.start_preview(alpha=128, fullscreen=False, window=(0, 50, 640, 360))
camera.annotate_text_size = 32

# https://picamera.readthedocs.io/en/release-1.10/recipes1.html#capturing-to-a-pil-image 
# Create the in-memory stream
stream = io.BytesIO()
camera.capture(stream, format='jpeg')
#   "Rewind" the stream to the beginning so we can read its content
stream.seek(0)
image = Image.open(stream)

image1 = image.copy()
image2 = image.copy()
image3 = image.copy()
image4 = image.copy()
image5 = image.copy()
 
############################################

while True:
#    distance3 = lidar.getDistance()
#    print(distance3)
#   met Sanderi44/Lidar-Lite
    distance2 = lidar.getDistance()
    print('distance2 : ',distance2)
    tijd2 = time.time()
#    time.sleep(0.1)
#    velocity2 = lidar.getVelocity()
#    velocity22 = snelheid_2.meter_uur()
#    velocity2 = velocity22[0]
#    print(velocity2)
    distance_verschil = distance2 - distance1
    tijd_verschil = tijd2 - tijd1
#                if tijd_verschil > 0.01:
#                    print(tijd2,tijd_verschil)
    tijd_verschil_tot = tijd_verschil_tot + tijd_verschil
    teller = teller + 1
    tijd_verschil_gem = tijd_verschil_tot / teller
    snelheid = distance_verschil / tijd_verschil # cm/sec
#                print(distance1,distance2,distance_verschil,f'{tijd_verschil:.5f}',f'{snelheid:.2f}')
    snelheid_km_uur = snelheid * 0.036
    snelheid_km_uur_abs = abs(snelheid_km_uur)
#    print('snelheid_km_uur : ',snelheid_km_uur)
    velocity2_km_uur = velocity2 * 0.36
    velocity2_km_uur_abs = abs(velocity2_km_uur)
#    print('velocity2_km_uur : ',velocity2_km_uur)
    old_uu_mm = uu_mm
    old_uur   = uur
    t = time.localtime()
#    jaar = t[0]
#    maand = t[1]
#    dag = t[2]
    uur = t[3]
    minu = t[4]
    uu_mm = str(f'{uur:02d}') + ':' + str(f'{minu:02d}')
########################################################################
    if distance1 > 120 and distance2 > 120 and snelheid_km_uur_abs > 5 and snelheid_km_uur_abs < 200: 
#
# wegschrijven van de 5 foto's
# teller op 5 zetten
# later snelheid tussen 10 km/u en 120 km/u
#
        writeCSV(distance2,distance1,velocity2,velocity2_km_uur,snelheid_km_uur,tijd_verschil)
        print('auto : ',auto)
        if auto == 0:
#           eerst 5 vorige frames saven, dan de volgende 5
            auto = 5
            kopie = 0
#           blijkbaar verliest "image" zijn inhoud na "saven"
#           men kan maar een "image" copieren als een nieuwe inhoud aanwezig is
#           AttributeError: 'NoneType' object has no attribute 'copy'
            if kopie >= 5:
                volgnr = volgnr + 1
                fotonaam = fotonaam1 + fotonaam2 + str(f'{volgnr:04d}') + '.jpg'
# https://pythonguides.com/python-save-an-image-to-file/
                image5 = image5.save(fotonaam)
            if kopie >= 4:
                volgnr = volgnr + 1
                fotonaam = fotonaam1 + fotonaam2 + str(f'{volgnr:04d}') + '.jpg'
                image4 = image4.save(fotonaam)
            if kopie >= 3:
                volgnr = volgnr + 1
                fotonaam = fotonaam1 + fotonaam2 + str(f'{volgnr:04d}') + '.jpg'
                image3 = image3.save(fotonaam)
            if kopie >= 2:
                volgnr = volgnr + 1
                fotonaam = fotonaam1 + fotonaam2 + str(f'{volgnr:04d}') + '.jpg'
                image2 = image2.save(fotonaam)
            if kopie >= 1:
                volgnr = volgnr + 1
                fotonaam = fotonaam1 + fotonaam2 + str(f'{volgnr:04d}') + '.jpg'
                image1 = image1.save(fotonaam)
        else:
            if auto > 0:
                auto = auto - 1
        volgnr = volgnr + 1
        fotonaam = fotonaam1 + fotonaam2 + str(f'{volgnr:04d}') + '.jpg'
        image = image.save(fotonaam)
    else:
# zolang teller > 0 nieuwe foto's wegschrijven na het "event"
        print('else auto : ',auto)
        if auto > 0:
            volgnr = volgnr + 1
            fotonaam = fotonaam1 + fotonaam2 + str(f'{volgnr:04d}') + '.jpg'
            image = image.save(fotonaam)
            auto = auto - 1

    foto(volgnr)
    camera.annotate_text = foto_annot
    fotonaam = fotonaam1 + fotonaam2
    print(fotonaam)
#    camera.capture(fotonaam)
# https://picamera.readthedocs.io/en/release-1.10/recipes1.html#capturing-to-a-pil-image 
# Create the in-memory stream
    stream = io.BytesIO()
    camera.capture(stream, format='jpeg')
#   "Rewind" the stream to the beginning so we can read its content
    stream.seek(0)
    image = Image.open(stream)
# men kan pas een "image" gebruiken als het gelezen is 
# AttributeError: 'NoneType' object has no attribute 'copy'
    kopie = kopie + 1
# steeds de laatste 5 foto's bijhouden (en dus opschuiven)
# https://www.geeksforgeeks.org/python-pil-copy-method/
    if kopie >= 5:
        image5 = image4.copy()
    if kopie >= 4:
        image4 = image3.copy()
    if kopie >= 3:
        image3 = image2.copy()
    if kopie >= 2:
        image2 = image1.copy()
    if kopie >= 1:
        image1 = image.copy()

###########################################################################
#https://stackoverflow.com/questions/35176639/compare-images-python-pil
# from PIL import Image

# im1 = Image.open('image1.jpg')
# im2 = Image.open('image2.jpg')

# if list(im1.getdata()) == list(im2.getdata()):
#     print("Identical")
# else:
#     print ("Different")
###########################################################################

    time.sleep(0.45) # niet te snel achter elkaar meten zodat om de seconde een foto
#                     in één seconde legt men 33 meter af tegen 120km/uur
#                     in één seconde legt men 25 meter af tegen 100km/uur
#                     in één seconde legt men 17 meter af tegen 60km/uur
#                     in één seconde legt men  8 meter af tegen 30km/uur
#                     in één seconde legt men  4 meter af tegen 15km/uur
#
    tijd3 = time.time()
    tijd_verschil_fotos = tijd3 - tijd1
    print('tijd_verschil tussen 2 fotos : ',tijd_verschil_fotos)
#
#   met Sanderi44/Lidar-Lite
    distance1 = lidar.getDistance()
    print('distance1 : ',distance1)
    tijd1 = time.time()
    time.sleep(0.2) # 1/2 sec wachten tot de volgende afstandsmeting
#
    if old_uur != uur:   # elk uur een nieuwe nummering, normaal max 3600 foto's
        volgnr = 0

######################################
