"""
Be sure to check the learn guides for more usage information.

This example is for use on (Linux) computers that are using CPython with
Adafruit Blinka to support CircuitPython libraries. CircuitPython does
not support PIL/pillow (python imaging library)!

Author(s): Melissa LeBlanc-Williams for Adafruit Industries
"""

import os
from datetime import *
import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7735
heure = ""

print("###### init LCD = ok")

# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D27)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()
disp = st7735.ST7735R(
    spi,
    rotation=0,
    height=128,
    x_offset=2,
    y_offset=3,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
if disp.rotation % 180 == 90:
    height = disp.width  # we swap height/width to rotate it to landscape!
    width = disp.height
else:
    width = disp.width  # we swap height/width to rotate it to landscape!
    height = disp.height
image = Image.new("RGB", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image)

padding = -2
x = 0

##################### FONTS ####################################
font = ImageFont.truetype('/home/tft/fonts/DejaVuSans-Bold.ttf', 14 )
font2 = ImageFont.truetype('/home/tft/fonts/dejavu/DejaVuSans.ttf', 14 )
font3 = ImageFont.truetype('/home/tft/fonts/DejaVuSans-Bold.ttf', 14)
font4 = ImageFont.truetype('/home/tft/fonts/PixelOperator.ttf', 16)
font5 = ImageFont.truetype('/home/tft/fonts/lineawesome-webfont.ttf', 18)
font6 = ImageFont.truetype('/home/tft/fonts/PixelOperator.ttf', 17)
#font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)

api = True

def get_ip():
    cmd = "hostname -I | awk '{print $1}'"
    IP = subprocess.check_output(cmd, shell = True ).decode("utf-8")
    return IP
    draw.text((3,110), "IP : " + str(IP) ,fill = "WHITE", font=font4)


def salon_con():
    network = open("/etc/spotnik/network","r")
    net = network.read()
    if net.find("rrf") != -1:
        salon = "RESEAU RRF"
    if net.find("tec") != -1:
        salon = "SALON TECHNIQUE"
    if net.find("loc") != -1:
        salon = "SALON LOCAL"
    if net.find("bav") != -1:
        salon = "SALON BAVARDAGE"
    if net.find("exp") != -1:
        salon = "SALON EXPERIMENTAL"
    if net.find("int") != -1:
        salon = "SALON INTERNATIONAL"
    if net.find("fon") != -1:
        salon = "RESEAU FON"
    if net.find("default") != -1:
        salon = "MODE PERROQUET"
    if net.find("ri49") != -1:
        salon = "RESEAU RI49"
    draw.text((6,30), salon, font=font4, fill="WHITE")



#['Fri', 'Sep', '29', '15:12:16', '2023:', 'ReflectorLogic:', 'Node', 'left:', '(94)', 'F4ICR', 'H\n']
def get_nodes():
    global nb_nodes
    f = os.popen('egrep -a -h "Node joined:" /tmp/svxlink.log | tail -1')
    lognodesin = str(f.read()).split(" ")
    #print(lognodesin)
    #print(len(lognodesin))
    if len(lognodesin)>=2:
        if lognodesin[7]=="joined:":
            DPTNODEin=lognodesin[8].rstrip("\r\n")
            CALLNODEin=lognodesin[9].rstrip("\r\n")
            NODEDPTin=lognodesin[10].rstrip("\r\n")
            CALLin = DPTNODEin+ " " +CALLNODEin + " "+NODEDPTin
            #print("NODE IN : " + CALLin)
            draw.text((3,86), "In :" +CALLin ,fill = "WHITE", font=font4)
#            nb_nodes += 1
 #           print("nbre de nodes IN:" + str(nb_nodes))
        if lognodesin[8]=="joined:":
            DPTNODEin=lognodesin[9].rstrip("\r\n")
            CALLNODEin=lognodesin[10].rstrip("\r\n")
            NODEDPTin=lognodesin[11].rstrip("\r\n")
            CALLin = DPTNODEin+ " " +CALLNODEin + " "+NODEDPTin
            #print("NODE IN : " + CALLin)
            draw.text((3,86), "In :" +CALLin ,fill = "WHITE", font=font4)
    f = os.popen('egrep -a -h "Node left:" /tmp/svxlink.log | tail -1')
    lognodesout = str(f.read()).split(" ")
    #print(lognodesout)
    #print(len(lognodesout))
    if len(lognodesout)>=2:
        if lognodesout[7]=="left:":
            DPTNODEout=lognodesout[8].rstrip("\r\n")
            CALLNODEout=lognodesout[9].rstrip("\r\n")
            NODEDPTout=lognodesout[10].rstrip("\r\n")
            CALLout = DPTNODEout+ " " +CALLNODEout + " "+NODEDPTout
            #print("NODE OUT : " + CALLout)
            draw.text((3,98), "Out :" +CALLout ,fill = "WHITE", font=font4)
        if lognodesout[8]=="left:":
            DPTNODEout=lognodesout[9].rstrip("\r\n")
            CALLNODEout=lognodesout[10].rstrip("\r\n")
            NODEDPTout=lognodesout[11].rstrip("\r\n")
            CALLout = DPTNODEout+ " " +CALLNODEout + " "+NODEDPTout
            #print("NODE IN : " + CALLin)
            draw.text((3,98), "Out :" +CALLout ,fill = "WHITE", font=font4)






##Fri Sep 29 15:50:15 2023: ReflectorLogic: Connected nodes: GW-EL, GW-ASL, (77) F4JAK H, (44) F4JRM H, (67) F5TFB V, (05) F5HII H, (63) F1ZZR R, (76) F1ZIB T, (57) F4EOC V, (77) F1ZRY V, SRV-RI49, (972) FM0JZ V, (972) FM4TI H, (BE) ON0LUS V, (13) F1ZWG R, (49) F5ZTV T, (56) F4JRD H, (QC) VE2KBS H, (49) F5ZRH R, (43) F1ZMV T, (49) F1ZSM R, (92) F5ZSY V, (44) F1ZZB U, (49) F6ZZY R, (16) F0EQJ H, 
##(33) F5RUE B, (972) FM1LF H, (13) F4ALT H, (92) F4ICM H, (67) F5SWB B, (67) F5SWB V

def get_number_nodes():
    f = os.popen('egrep -a -h "Connected nodes:" /tmp/svxlink.log | tail -1')
    nb_nodes = str(f.read()).split(",")
    nb_nodes = len(nb_nodes)
   # draw.text((3,110), "Nbre de nodes : " + str(nb_nodes) ,fill = "WHITE", font=font4)


def get_svxlog():
    f = os.popen('egrep -a -h "Talker start:|Talker stop:" /tmp/svxlink.log | tail -1')
    logsvx = str(f.read()).split(" ")
    #print(logsvx)
    #print(len(logsvx))
    #print(logsvx[7])
    #print(logsvx[8])
    #print(logsvx[9])
    #print(logsvx[10])

    if len(logsvx)>=2:
        if logsvx[7]=="start:":
            if len(logsvx)==9:
                CALL=logsvx[8].rstrip("\r\n")
                #print("TX ON : " + CALL)
                draw.text((5,65), CALL ,fill = "BLUE", font=font)
            if len(logsvx)==11:
                DPT=logsvx[8].rstrip("\r\n")
                CALL=logsvx[9].rstrip("\r\n")
                NODE=logsvx[10].rstrip("\r\n")
                CALL = DPT+ " " +CALL + " "+NODE
                #print("TX ON " + CALL)
                draw.text((5,65), CALL ,fill = "BLUE", font=font)
        if logsvx[8]=="start:":
            if len(logsvx)==10:
                CALL=logsvx[9].rstrip("\r\n")
                #print("TX ON " + CALL)
                draw.text((5,65), CALL ,fill = "BLUE", font=font)
            if len(logsvx)==12:
                DPT=logsvx[9].rstrip("\r\n")
                CALL=logsvx[10].rstrip("\r\n")
                NODE=logsvx[11].rstrip("\r\n")
                CALL = DPT+ " " +CALL + " "+NODE
                #print("TX ON " + CALL)
                draw.text((5,65), CALL ,fill = "BLUE", font=font)

'''

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Shell scripts for system monitoring from here:
    # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d' ' -f1"
    IP = "IP: " + subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB  %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %d/%d GB  %s", $3,$2,$5}\''
    Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "cat /sys/class/thermal/thermal_zone0/temp |  awk '{printf \"CPU Temp: %.1f C\", $(NF-0) / 1000}'"  # pylint: disable=line-too-long
    Temp = subprocess.check_output(cmd, shell=True).decode("utf-8")

    # Write four lines of text.
    y = padding
    draw.text((x, y), IP, font=font, fill="#FFFFFF")
    y += font.getsize(IP)[1]
    draw.text((x, y), CPU, font=font, fill="#FFFF00")
    y += font.getsize(CPU)[1]
    draw.text((x, y), MemUsage, font=font, fill="#00FF00")
    y += font.getsize(MemUsage)[1]
    draw.text((x, y), Disk, font=font, fill="#0000FF")
    y += font.getsize(Disk)[1]
    draw.text((x, y), Temp, font=font, fill="#FF00FF")

    # Display image.
    disp.image(image)
    time.sleep(0.1)

'''


IP = get_ip()
print("###### get ip adress : " + str(IP))


while True:

    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    salon_con()
    get_svxlog()
    #get_number_nodes()
    get_nodes()
    draw.line([(0,0),(127,0)], fill = "cyan",width = 2)
    draw.line([(4,18),(123,18)], fill = "cyan",width = 1)
    draw.line([(4,46),(123,46)], fill = "cyan",width = 1)
    draw.line([(4,86),(123,86)], fill = "cyan",width = 1)
    draw.line([(127,0),(127,127)], fill = "cyan",width = 2)
    draw.line([(127,127),(0,127)], fill = "cyan",width = 2)
    draw.line([(0,127),(0,0)], fill = "cyan",width = 2)
    draw.text((6, 18), 'Réseau connecté : ', fill = "YELLOW", font=font4)
    draw.text((6, 48), 'STATION :', fill = "cyan", font=font4)
    draw.text((104,0), chr(62016), font=font5, fill="green")
    draw.text((2,0), chr(61931), font=font5, fill="blue")
    draw.text((3,110), "IP : " + str(IP) ,fill = "WHITE", font=font4)
    draw.text((32, 2), str(time.strftime('%H:%M:%S')), fill="cyan", font=font4)

    disp.image(image)
    time.sleep(0.1)
