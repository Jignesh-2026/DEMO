
#Create a virtual environment:
'''
mkdir choco
cd choco
python3 -m venv myenv
python3 -m venv --system-site-packages myenv
source myenv/bin/activate

'''
#Create different blinking patterns with LEDs by connecting to GPIO pints of Raspberry Pi. 
#A.Using Raspberry pi 3 
#sudo apt update
#sudo apt install python3-gpiozero python3-lgpio
'''
LED	    GPIO   Pin ( BCM)	Physical Pin
Red	    GPIO   17	 Pin 11
Green	GPIO   27	 Pin 13
Yellow	GPIO   22	 Pin 15
Common Ground	GND	 Pin 6'''

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

leds = [4, 5, 6, 7]

for led in leds:
    GPIO.setup(led, GPIO.OUT)

while True:
    for led in leds:
        GPIO.output(led, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(led, GPIO.LOW)

    choice = input("Press 'q' to terminate or Enter to continue: ")

    if choice.lower() == 'q':
        break

GPIO.cleanup()
print("Program terminated")



#
#Display Text , Number , Ascii , Hexdecimal , Binary Number and temperature in Tm1637

'''TM1637 is a display module containing four seven-segment LED digits.

It uses only two GPIO pins for communication:
- CLK: Clock signal.
- DIO: Data input/output.
- VCC: Power supply.
- GND: Ground connection.

TM1637 Pin	Raspberry Pi GPIO	Physical Pin
VCC  	3.3V	1
GND 	GND	   6
CLK	   GPIO    23	             16
DIO	   GPIO    24	             18

'''
#sudo apt install python3-lgpio -y
#nano tm1637_display.py

import tm1637
from time import sleep

display = tm1637.TM1637(clk=5, dio=6)
display.brightness(7)

display.number(1234)
sleep(2)

display.show("TEST")
sleep(2)

display.hex(0xBEEF)
sleep(2)

display.show("AbCd")
sleep(2)

temperature = 25
display.temperature(temperature)
sleep(2)

binary_number = bin(10)[2:]
display.show(binary_number)
sleep(2)

display.show("    ")



#
#Interface 16x2 LCD with Raspberry Pi using I2C module to display text.
'''
LCD I2C Pin	    Raspberry Pi GPIO	Physical Pin
VCC	                   5V	           2
GND	                  GND              6
SDA	                 GPIO 2(SDA1)	   3
SCL	                 GPIO 3(SCL1)	   5

sudo apt update
sudo apt upgrade -y

Enable I2C Interface
Open Raspberry Pi configuration:
sudo raspi-config

Follow these steps:
1. Select Interface Options.
2. Select I2C.
3. Choose Yes to enable I2C.
4. Select Finish.
5. Restart Raspberry Pi.

sudo reboot

sudo apt install -y i2c-tools python3-smbus python3-pip


Install the LCD Python library:
pip install RPLCD smbus2

If Raspberry Pi OS blocks global pip installation, use a virtual environment:
python3 -m venv lcd-env
source lcd-env/bin/activate
pip install RPLCD smbus2


Step 6: Check the I2C address
Run:
sudo i2cdetect -y 1


You should see an address such as:
- 0x27
- 0x3f

nano lcd_display.py


'''
#code 1
from RPLCD.i2c import CharLCD
lcd = CharLCD(
    i2c_expander='PCF8574',
    address=0x27,
    port=1,
    cols=16,
    rows=2
)
lcd.write_string("Pranav Varak")

#code 2

from RPLCD.i2c import CharLCD
lcd = CharLCD(
    i2c_expander='PCF8574',
    address=0x27,
    port=1,
    cols=16,
    rows=2
)
lcd.clear()
lcd.cursor_pos = (0, 0)
lcd.write_string("Pranav")
lcd.cursor_pos = (1, 0)
lcd.write_string("Varak")

#code 3
from RPLCD.i2c import CharLCD
from time import sleep

lcd = CharLCD(
    i2c_expander='PCF8574',
    address=0x27,
    port=1,
    cols=16,
    rows=2
)

while True:
    lcd.clear()

    lcd.cursor_pos = (0, 0)
    lcd.write_string("Pranav")

    lcd.cursor_pos = (1, 0)
    lcd.write_string("Varak")

    sleep(2)

    lcd.clear()

    lcd.cursor_pos = (0, 0)
    lcd.write_string("Varak")

    lcd.cursor_pos = (1, 0)
    lcd.write_string("Pranav")

    sleep(2)


#code 4
from RPLCD.i2c import CharLCD

lcd = CharLCD(
    i2c_expander='PCF8574',
    address=0x27,
    port=1,
    cols=16,
    rows=2
)

lcd.clear()

lcd.cursor_pos = (0, 0)
lcd.write_string("Pranav")

lcd.cursor_pos = (1, 0)
lcd.write_string("        Varak")

#code 5
from RPLCD.i2c import CharLCD
from time import sleep

lcd = CharLCD(
    i2c_expander='PCF8574',
    address=0x27,
    port=1,
    cols=16,
    rows=2
)

text = "Pranav Varak"

while True:
    scrolling_text = " " * 16 + text + " " * 16

    for i in range(len(scrolling_text) - 15):
        display_text = scrolling_text[i:i + 16]

        lcd.cursor_pos = (0, 0)
        lcd.write_string(display_text)

        sleep(4)




#
#Use Telegram to control raspberry pi GPIO
'''Required Python Libraries
Library	Purpose
python-telegram-bot	  Communicate with Telegram Bot
gpiozero	          Control Raspberry Pi GPIO pins
lgpio	              GPIO backend, particularly for Pi 5

'''

import telebot
from gpiozero import LED

led = LED(17)
bot = telebot.TeleBot("")

@bot.message_handler(commands=['on'])
def on(message):
    led.on()
    bot.reply_to(message, "LED ON")

@bot.message_handler(commands=['off'])
def off(message):
    led.off()
    bot.reply_to(message, "LED OFF")

bot.infinity_polling()



#
#Write a program to read the CPU%, Memory% and CPU temperature of Raspberry Pi.

'''
Update Raspberry Pi
Execute:
sudo apt update
sudo apt upgrade -y

Install the required library
Install psutil:
sudo apt install python3-psutil -y


You can also install it using pip in a virtual environment:
python3 -m venv system-env
source system-env/bin/activate
pip install psutil


Check CPU temperature
Run this command:
cat /sys/class/thermal/thermal_zone0/temp


Divide this number by 1000.

Therefore:
45000 / 1000 = 45°C


'''

#code
import psutil
import time

# Function to read CPU temperature
def get_temperature():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as file:
            temp = int(file.read()) / 1000
        return temp
    except:
        return None


# Main program
try:
    while True:

        # Read CPU usage
        cpu = psutil.cpu_percent(interval=1)

        # Read Memory usage
        memory = psutil.virtual_memory().percent

        # Read CPU temperature
        temperature = get_temperature()

        # Display results
        print("----------------------------")
        print("RASPBERRY PI SYSTEM MONITOR")
        print("----------------------------")

        print("CPU Usage: ", cpu, "%")
        print("Memory Usage: ", memory, "%")

        if temperature is not None:
            print("CPU Temperature: ", temperature, "°C")
        else:
            print("Temperature not available")

        print("----------------------------")

        time.sleep(2)

except KeyboardInterrupt:
    print("\nProgram stopped")



#code second to show output on TM1637
#Code:
import time
import tm1637
import psutil

display = tm1637.TM1637(clk=23, dio=24)
display.brightness(7)

while True:
    cpu=int(psutil.cpu_percent(interval=1))
    display.show(f"{cpu:04d}")
    print("CPU percent",cpu)
    time.sleep(2)
    display.show("    ")
    time.sleep(2)
    temp=psutil.sensors_temperatures()['cpu_thermal'][0].current
    n=int(float(temp))
    print("CPU Temperature:",n)
    
    display.show(str(n))
    time.sleep(2)
    display.show("    ")
    time.sleep(2)
    memory=psutil.virtual_memory().percent
    n=int(float(memory))
    print("memory percent: ",memory)
    display.show(str(n))
    time.sleep(2)
    display.show("    ")
    time.sleep(2)




#
#Interface Pi Camera with Raspberry Pi to capture image and video.
'''
Update Raspberry Pi
Open the Terminal and execute:
sudo apt update
sudo apt full-upgrade -y


Install the Camera Library
Install Picamera2:
sudo apt install -y python3-picamera2


Install camera applications:
sudo apt install -y rpicam-apps


Check Camera Connection
Run:
rpicam-hello --list-cameras


Test Camera Preview
Execute:
rpicam-hello


Create a Python Program
Create a new Python file:
nano camera_capture.py

command used to handle this camera on cmd
rpicam-hello -timeout 0
rpicam-still --output photo.jpg  #o means output
rpicam-still -o ~/small.jpg --width 640 --height 480
rpicam-vid -t 10000 -o video.h264
rpicam-still -o bright_photo.jpg --brightness 0.3 
'''

#Code 1: Capture Image

from picamera2 import Picamera2
import time
picam2 = Picamera2()
config = picam2.create_still_configuration()
picam2.configure(config)
picam2.start()
time.sleep(2)
picam2.capture_file("image.jpg")
picam2.stop()
print("Image Captured Successfully")

#Code 2: Record Video

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
import time
picam2 = Picamera2()
video_config = picam2.create_video_configuration()
picam2.configure(video_config)
encoder = H264Encoder()
picam2.start()
picam2.start_recording(
    encoder,
    "video.h264"
)
time.sleep(10)

picam2.stop_recording()
picam2.stop()
print("Video Recorded Successfully")


#code 3: photo and video
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
import time

# Initialize camera
camera = Picamera2()

# Configure camera
config = camera.create_video_configuration()
camera.configure(config)

# Start camera
camera.start()
time.sleep(2)

# Capture image
camera.capture_file("image.jpg")
print("Image captured successfully!")

# Record video
encoder = H264Encoder(bitrate=10000000)

output = FileOutput("video.h264")

camera.start_recording(encoder, output)

print("Video recording started...")

time.sleep(10)

camera.stop_recording()

print("Video recorded successfully!")

# Stop camera
camera.stop()

print("Camera stopped.")



#
#Interface RFID module with Raspberry Pi to read and write to RFID tags/cards.
'''
Required Python Libraries
For Raspberry Pi 5, use the following libraries:
Library	Purpose
spidev	 SPI communication with RFID module
python3-rpi-lgpio	GPIO compatibility for Raspberry Pi 5
mfrc522	  Read and write RFID cards
RPi.GPIO API	GPIO interface provided through rpi-lgpio


Connect the RC522 module to Raspberry Pi 5:

RC522 Pin	Raspberry Pi GPIO	Physical Pin

SDA / SS	  GPIO 8 (CE0)	      24
SCK	          GPIO 11 (SCLK)	  23
MOSI	      GPIO 10 (MOSI)	  19
MISO	      GPIO 9 (MISO)    	  21
IRQ	          Not connected	      —
GND	              GND	          6
RST	             GPIO 25	      22
3.3V	         3.3V	           1


Update Raspberry Pi
sudo apt update
sudo apt upgrade -y


Enable SPI Interface
Enter:
sudo raspi-config


Follow these steps:
1. Select Interface Options.
2. Select SPI.
3. Select Yes to enable SPI.
4. Select Finish.
5. Restart Raspberry Pi.
sudo reboot


Install Required Libraries
Install the system packages:
sudo apt install python3-spidev python3-rpi-lgpio python3-venv -y


Create a virtual environment:
python3 -m venv --system-site-packages rfid-env

Activate it:
source rfid-env/bin/activate

Install the RFID library:
pip install --no-deps mfrc522

Check SPI Connection
Run:
ls /dev/spidev*


optional
If these devices appear, SPI is enabled.
Add your user to the required groups:
sudo usermod -aG spi,gpio $USER

Restart Raspberry Pi:
sudo reboot

Create a Python Program
Create a file:
nano rfid_read_write.py


'''

#code
from mfrc522 import SimpleMFRC522

# Initialize RFID reader
reader = SimpleMFRC522()

try:
    while True:

        print("\n--- RFID CARD SYSTEM ---")
        print("1. Read RFID Card")
        print("2. Write RFID Card")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":

            print("Place your RFID card near reader...")

            card_id, text = reader.read()

            print("\nCard Read Successfully!")
            print("Card ID:", card_id)
            print("Card Data:", text)

        elif choice == "2":

            data = input("Enter data to write (max 16 characters): ")

            print("Place your RFID card near reader...")

            card_id = reader.write(data)

            print("\nData Written Successfully!")
            print("Card ID:", card_id)

        elif choice == "3":

            print("Exiting RFID System...")
            break

        else:
            print("Invalid Choice!")

except KeyboardInterrupt:
    print("\nProgram stopped")

finally:
    reader.cleanup()



#code 2: Read RFID UID
from JoyIT_RC522 import SimpleMFRC522
reader = SimpleMFRC522()
print("Place RFID card near the reader...")
card_id = reader.read_id()
print("Card UID:", card_id)

#Code 3: Write Data to RFID Card
from JoyIT_RC522 import SimpleMFRC522
reader = SimpleMFRC522()
text = input("Enter text: ")
print("Place RFID card near the reader...")
reader.write(text)
print("Data written successfully.")


#code 4: Read Stored RFID Data
from JoyIT_RC522 import SimpleMFRC522
reader = SimpleMFRC522()
print("Place RFID card near the reader...")
card_id, text = reader.read()
print("Card UID:", card_id)
print("Stored Data:", text)



#
#Interface Fingerprint Sensor with Raspberry Pi.
'''
Fingerprint sensor	   Raspberry Pi 5
VCC                    Suitable power pin (check sensor datasheet)
GND	                   Physical pin 6 (GND)
TX	                   GPIO15 / RXD (physical pin 10)
RX	                   GPIO14 / TXD (physical pin 8)

Enable UART on Raspberry Pi 5
1. Open the terminal.
2. Run:
sudo raspi-config


3. Select Interface Options → Serial Port.
4. Select No when asked whether to enable the login shell over serial.
5. Select Yes to enable the serial hardware.
6. Finish and reboot:
sudo reboot 

After reboot, check the serial port:
ls -l /dev/serial0

Install Python libraries
Run:
sudo apt update
sudo apt install python3-venv python3-pip -y

Create a virtual environment:
python3 -m venv --system-site-packages fingerprint-env
source fingerprint-env/bin/activate


Install the required libraries:
pip install pyfingerprint pyserial

Python program: Enroll and identify fingerprints
Create a Python file:
nano fingerprint.py


'''

#code

from pyfingerprint.pyfingerprint import PyFingerprint
import time

try:
    sensor = PyFingerprint(
        '/dev/serial0',
        57600,
        0xFFFFFFFF,
        0x00000000
    )

    if not sensor.verifyPassword():
        raise ValueError("Fingerprint sensor password is incorrect")

    print("Fingerprint sensor connected successfully!")

except Exception as e:
    print("Sensor connection failed:", e)
    raise SystemExit


def enroll_fingerprint():
    print("\nPlace your finger on the sensor...")

    while not sensor.readImage():
        pass

    sensor.convertImage(0x01)

    result = sensor.searchTemplate()

    if result[0] >= 0:
        print("Fingerprint already registered!")
        return

    print("Remove your finger...")
    time.sleep(2)

    print("Place the same finger again...")

    while not sensor.readImage():
        pass

    sensor.convertImage(0x02)

    if sensor.compareCharacteristics() == 0:
        print("Fingerprints do not match!")
        return

    sensor.createTemplate()
    position = sensor.storeTemplate()

    print("Fingerprint enrolled successfully!")
    print("Fingerprint ID:", position)


def search_fingerprint():
    print("\nPlace your finger on the sensor...")

    while not sensor.readImage():
        pass

    sensor.convertImage(0x01)

    result = sensor.searchTemplate()

    position = result[0]
    accuracy = result[1]

    if position == -1:
        print("Fingerprint not found!")
    else:
        print("Fingerprint matched!")
        print("Fingerprint ID:", position)
        print("Accuracy score:", accuracy)


while True:
    print("\n--- FINGERPRINT SYSTEM ---")
    print("1. Enroll Fingerprint")
    print("2. Search Fingerprint")
    print("3. Exit")

    choice = input("Enter your choice: ")

    try:
        if choice == "1":
            enroll_fingerprint()

        elif choice == "2":
            search_fingerprint()

        elif choice == "3":
            print("Exiting...")
            break

        else:
            print("Invalid choice!")

    except Exception as e:
        print("Operation error:", e)


#code 2: Test R307 Connection
from pyfingerprint.pyfingerprint import PyFingerprint
try:
    sensor = PyFingerprint(
        '/dev/serial0',
        57600,
        0xFFFFFFFF,
        0x00000000
    )
    if sensor.verifyPassword():
        print(
            "Fingerprint sensor "
            "connected successfully!"
        )
    else:
        print(
            "Fingerprint sensor "
            "password verification failed."
        )
except Exception as e:
    print(
        "Fingerprint sensor "
        "could not be initialized!"
    )
    print("Error:", e)

# code 3: Capture Fingerprint
from pyfingerprint.pyfingerprint import PyFingerprint
import time
try:
    sensor = PyFingerprint(
        '/dev/serial0',
        57600,
        0xFFFFFFFF,
        0x0000000   )
    if sensor.verifyPassword():
        print("Fingerprint sensor connected successfully!  ")
    else:
        print("Password verification failed.")
        exit()
    print("Place your finger on the sensor..."   )
    while not sensor.readImage():
        time.sleep(0.1)
    print("Fingerprint captured successfully!"  )
except Exception as e:
    print("Error:", e)






#
#motion detector
'''
HC-SR501 PIR pin	Raspberry Pi 5 pin
VCC	      5V –      Physical pin 2
OUT   	GPIO4 –     Physical pin 7
GND	     GND –      Physical pin 6

Install the required library
Open the Raspberry Pi terminal and execute these commands one by one.

Step 1: Update Raspberry Pi
sudo apt update
sudo apt upgrade -y


Install GPIO Zero
sudo apt install python3-gpiozero python3-lgpio -y

Check the library
python3 -c "from gpiozero import MotionSensor; print('GPIO Zero installed successfully')"


'''

#code

from gpiozero import MotionSensor
from time import sleep

# Connect PIR sensor to GPIO 4
pir = MotionSensor(4)

print("Motion Detection System Started")
print("Waiting for sensor to become ready...")

# Wait until sensor detects no motion
pir.wait_for_no_motion()

print("Sensor Ready! Waiting for motion...")

try:
    while True:

        if pir.motion_detected:
            print("Motion Detected!")

        else:
            print("No Motion Detected")

        sleep(1)

except KeyboardInterrupt:
    print("\nProgram Stopped")


#
#Interface GPS module with Raspberry Pi.
'''
GPS module pin	   Raspberry Pi 5 pin
VCC	                 3.3V (physical pin 1), if supported by your module
GND	                 GND (physical pin 6)
TX	                 GPIO15 /   RXD (physical pin 10)
RX	                 GPIO14 / TXD (physical pin 8)

Open the terminal.

Step 2: Edit the boot configuration:
sudo nano /boot/firmware/config.txt
Add this line at the bottom:
dtparam=uart0=on

Save using CTRL + O, Enter, then CTRL + X.

Step 5: Restart Raspberry Pi:
sudo reboot

Check the UART device:
ls -l /dev/ttyAMA0


Install the required libraries
Run these commands one by one:

Step 1: Update Raspberry Pi
sudo apt update


Step 2: Install Python serial and NMEA libraries
sudo apt install python3-serial python3-pynmea2 -y

Check the libraries
python3 -c "import serial, pynmea2; print('GPS libraries installed successfully')"


'''

#code

import serial
import pynmea2
import time

# Connect GPS module to Raspberry Pi 5 UART
gps = serial.Serial(
    "/dev/ttyAMA0",
    baudrate=9600,
    timeout=1
)

print("GPS Module Connected Successfully!")
print("Waiting for GPS signal...")

try:
    while True:
        line = gps.readline().decode(
            "ascii", errors="replace"
        ).strip()

        if line.startswith("$"):
            try:
                msg = pynmea2.parse(line)

                if msg.sentence_type == "GGA":

                    if int(msg.gps_qual) > 0:
                        print("\n--- GPS LOCATION ---")
                        print("Latitude:", msg.latitude)
                        print("Longitude:", msg.longitude)
                        print("Altitude:", msg.altitude, "meters")
                        print("Satellites:", msg.num_sats)

                    else:
                        print("Waiting for satellite fix...")

                elif msg.sentence_type == "RMC":
                    if msg.status == "A":
                        speed = float(msg.spd_over_grnd or 0)
                        print(
                            "Speed:",
                            round(speed * 1.852, 2),
                            "km/h"
                        )

            except (pynmea2.ParseError, ValueError):
                pass

except KeyboardInterrupt:
    print("\nGPS Program Stopped")

finally:
    gps.close()



#code 2 Read Raw GPS Data Using Python
import serial
gps = serial.Serial(
    port="/dev/ttyAMA0",
    baudrate=9600,
    timeout=1
)
print("GPS serial connection started...")
print("Reading NMEA data...\n")
try:
    while True:
        line = gps.readline().decode(
            "ascii",
            errors="replace"
        ).strip()
        if line:
            print(line)
except KeyboardInterrupt:
    print("\nGPS program stopped.")
finally:
    gps.close()


#code 3 GPS Data With Latitude, Longitude, Time, Speed
import serial
import pynmea2
import time

gps = serial.Serial(
    port="/dev/ttyAMA0",
    baudrate=9600,
    timeout=1
)
print("GPS data reader started...")
print("Waiting for GPS fix...\n")
last_status = 0
try:
    while True:
        line = gps.readline().decode(
            "ascii",
            errors="replace"
        ).strip()
        if not line:
            continue
        try:
            message = pynmea2.parse(line)
            if isinstance(
                message,
                pynmea2.types.talker.RMC
            ):
                if message.status == "A":
                    print("\n----- GPS FIX -----")
                    print("Latitude :", message.latitude)
                    print("Longitude:", message.longitude)
                    print("Time     :", message.timestamp)
                    print("Speed    :", message.spd_over_grnd)
                    print("Course   :", message.true_course)
                else:
                    if time.time() - last_status >= 5:
                        print(
                            "Waiting for valid GPS fix..."
                        )
                        last_status = time.time()
        except pynmea2.ParseError:
            pass
except KeyboardInterrupt:
    print("\nGPS program stopped.")
finally:
    gps.close()

#
#Interface ADS 1115 with Raspberry Pi to act as oscilloscope.
'''
ADS1115 to Raspberry Pi 5
ADS1115 pin	  Raspberry Pi 5 pin
VDD	            3.3V – Physical pin 1
GND	            GND – Physical pin 6
SCL	            GPIO3 – Physical pin 5
SDA	             GPIO2 – Physical pin 3
A0            	Potentiometer middle pin (wiper)
ADDR	          GND (default address 0x48)


Potentiometer connections
Potentiometer pin	Connection
First outer pin	     3.3V
Middle pin	         ADS1115 A0
Other outer pin	     GND



Enable I2C on Raspberry Pi 5
Step 1: Open the terminal and type:
sudo raspi-config


Step 2: Select:

Interface Options → I2C → Enable

Step 3: Restart Raspberry Pi:
sudo reboot

Step 4: Install I2C tools:
sudo apt update
sudo apt install i2c-tools -y


Step 5: Check whether ADS1115 is detected:
sudo i2cdetect -y 1

Install Python libraries
Step 1: Install Python virtual environment support:
sudo apt install python3-venv python3-pip -y


Step 2: Create a project folder:
mkdir ads1115_scope
cd ads1115_scope


Step 3: Create and activate a virtual environment:
python3 -m venv --system-site-packages scope-env
source scope-env/bin/activate


Step 4: Install the required libraries:
pip install adafruit-blinka adafruit-circuitpython-ads1x15 matplotlib

Create the Python program
Step 1: Create a Python file:
nano oscilloscope.py


'''

#
#code

import time
import board
import matplotlib.pyplot as plt

from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ads1x15.analog_in import AnalogIn

# Initialize I2C and ADS1115
i2c = board.I2C()
ads = ADS1115(i2c, data_rate=860, gain=1)

# Read analog signal from channel A0
channel = AnalogIn(ads, 0)

print("ADS1115 Oscilloscope Started")
print("Reading analog signal...")

# Oscilloscope settings
samples = 100
sample_interval = 0.002

plt.ion()

fig, ax = plt.subplots()
x = [i * sample_interval for i in range(samples)]
y = [0] * samples

line, = ax.plot(x, y)

ax.set_title("ADS1115 Digital Oscilloscope")
ax.set_xlabel("Time (seconds)")
ax.set_ylabel("Voltage (V)")
ax.set_ylim(0, 3.3)
ax.grid(True)

try:
    while True:
        start = time.perf_counter()
        readings = []

        for i in range(samples):
            readings.append(channel.voltage)

            # Maintain approximate sampling interval
            remaining = sample_interval - (
                time.perf_counter() - start
            )

            if remaining > 0:
                time.sleep(remaining)

            start = time.perf_counter()

        line.set_ydata(readings)

        ax.set_ylim(
            min(0, min(readings) - 0.1),
            max(3.3, max(readings) + 0.1)
        )

        fig.canvas.draw()
        fig.canvas.flush_events()
        plt.pause(0.01)

except KeyboardInterrupt:
    print("\nOscilloscope stopped")

finally:
    plt.close()

#code 
import time
import board
from adafruit_ads1x15 import ADS1115
from adafruit_ads1x15 import AnalogIn
from adafruit_ads1x15 import ads1x15
i2c = board.I2C()
ads = ADS1115(i2c)
channel = AnalogIn(
    ads,
    ads1x15.Pin.A0
)
print("ADS1115 detected!")
print("Reading A0...")
while True:
    print(
        "Raw:", channel.value,
        "Voltage:", round(channel.voltage, 3), "V"
    )
    time.sleep(0.5)






#Code 2: Read A0–A3

import time
import board
from adafruit_ads1x15 import ADS1115
from adafruit_ads1x15 import AnalogIn
from adafruit_ads1x15 import ads1x15
i2c = board.I2C()
ads = ADS1115(i2c)
a0 = AnalogIn(
    ads,
    ads1x15.Pin.A0
)
a1 = AnalogIn(
    ads,
    ads1x15.Pin.A1
)
a2 = AnalogIn(
    ads,
    ads1x15.Pin.A2
)
a3 = AnalogIn(
    ads,
    ads1x15.Pin.A3
)
print("ADS1115 Multi-Channel Reading Started")
while True:
    print("\n-------------------------")
    print(
        "A0:",
        round(a0.voltage, 3),
        "V"
    )
    print(
        "A1:",
        round(a1.voltage, 3),
        "V"
    )
    print(
        "A2:",
        round(a2.voltage, 3),
        "V"
    )
    print(
        "A3:",
        round(a3.voltage, 3),
        "V"
    )
    time.sleep(1)


#Code 3: Live Voltage Graph
import time
import board
import matplotlib.pyplot as plt
from adafruit_ads1x15 import ADS1115
from adafruit_ads1x15 import AnalogIn
from adafruit_ads1x15 import ads1x15
i2c = board.I2C()
ads = ADS1115(i2c)
channel = AnalogIn(
    ads,
    ads1x15.Pin.A0
)
times = []
voltages = []
start_time = time.time()
plt.ion()
fig, ax = plt.subplots()
line, = ax.plot([], [])
ax.set_xlabel("Time (seconds)")
ax.set_ylabel("Voltage (V)")
ax.set_title("ADS1115 - A0 Voltage")
print("ADS1115 Graph Started")
print("Close the graph window or press Ctrl+C to stop.")
try:
    while plt.fignum_exists(fig.number):
        voltage = channel.voltage
        current_time = time.time() - start_time
        times.append(current_time)
        voltages.append(voltage)
        line.set_xdata(times)
        line.set_ydata(voltages)
        ax.relim()
        ax.autoscale_view()
        plt.draw()
        plt.pause(0.5)
except KeyboardInterrupt:
    print("\nProgram stopped by user.")
finally:
    plt.close("all")
    print("ADS1115 program stopped.")


#
#Design a web dashboard using Flask. Control relay module via web.
'''
Relay module	Raspberry Pi 5
VCC	             5V – Physical pin 2
GND         	GND – Physical pin 6
IN	            GPIO17 – Physical pin 11

Install the required libraries
Open the Raspberry Pi terminal.

Step 1: Update Raspberry Pi
sudo apt update
sudo apt upgrade -y

Install Python and required packages
sudo apt install python3-venv python3-gpiozero python3-lgpio python3-flask -y

Create a project folder
mkdir relay_dashboard
cd relay_dashboard

Create a virtual environment
python3 -m venv --system-site-packages flask-env


Step 5: Activate it
source flask-env/bin/activate

Step 6: Check Flask installation
python -c "import flask, gpiozero; print('Libraries installed successfully')"

Create the Flask web application
Step 1: Create a Python file:
nano app.py


'''

#code 

from flask import Flask, render_template_string, redirect, url_for
from gpiozero import OutputDevice

app = Flask(__name__)

# Relay connected to GPIO17
# Most common relay modules are active LOW.
relay = OutputDevice(
    17,
    active_high=False,
    initial_value=False
)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Raspberry Pi Relay Dashboard</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>
        body {
            font-family: Arial, sans-serif;
            background: #eef2f3;
            text-align: center;
            padding: 40px 15px;
        }

        .dashboard {
            background: white;
            max-width: 450px;
            margin: auto;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 12px #0002;
        }

        h1 {
            color: #263238;
        }

        .status {
            font-size: 24px;
            font-weight: bold;
            margin: 25px;
        }

        .on {
            color: green;
        }

        .off {
            color: red;
        }

        button {
            padding: 14px 35px;
            margin: 10px;
            border: none;
            border-radius: 8px;
            color: white;
            font-size: 18px;
            cursor: pointer;
        }

        .on-button {
            background: #28a745;
        }

        .off-button {
            background: #dc3545;
        }
    </style>
</head>

<body>
    <div class="dashboard">
        <h1>Relay Control Dashboard</h1>
        <p>Raspberry Pi 5</p>

        <div class="status {{ 'on' if status else 'off' }}">
            Relay Status: {{ 'ON' if status else 'OFF' }}
        </div>

        <form action="/relay/on" method="POST">
            <button class="on-button" type="submit">
                TURN ON
            </button>
        </form>

        <form action="/relay/off" method="POST">
            <button class="off-button" type="submit">
                TURN OFF
            </button>
        </form>
    </div>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(
        HTML,
        status=relay.is_active
    )


@app.route("/relay/on", methods=["POST"])
def turn_on():
    relay.on()
    return redirect(url_for("home"))


@app.route("/relay/off", methods=["POST"])
def turn_off():
    relay.off()
    return redirect(url_for("home"))


if __name__ == "__main__":
    try:
        app.run(
            host="0.0.0.0",
            port=5000,
            debug=False
        )
    finally:
        relay.off()
        relay.close()



#
#11. Interface Fingerprint Sensor and 16X2 LCD with Raspberry and display message RFID UID matched or unmatched
#code
import smbus
import time

I2C_ADDR = 0x27
LCD_WIDTH = 16

LCD_CHR = 1
LCD_CMD = 0

LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0

LCD_BACKLIGHT = 0x08
ENABLE = 0b00000100

BUS = 1

bus = smbus.SMBus(BUS)

def lcd_toggle_enable(bits):
    time.sleep(0.0005)

    bus.write_byte(I2C_ADDR, bits | ENABLE)
    time.sleep(0.0005)

    bus.write_byte(I2C_ADDR, bits & ~ENABLE)
    time.sleep(0.0005)

def lcd_byte(bits, mode):
    high_bits = mode | (bits & 0xF0) | LCD_BACKLIGHT
    low_bits = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT

    bus.write_byte(I2C_ADDR, high_bits)
    lcd_toggle_enable(high_bits)

    bus.write_byte(I2C_ADDR, low_bits)
    lcd_toggle_enable(low_bits)

def lcd_init():
    lcd_byte(0x33, LCD_CMD)
    lcd_byte(0x32, LCD_CMD)
    lcd_byte(0x06, LCD_CMD)
    lcd_byte(0x0C, LCD_CMD)
    lcd_byte(0x28, LCD_CMD)
    lcd_byte(0x01, LCD_CMD)

    time.sleep(0.005)

def lcd_clear():
    lcd_byte(0x01, LCD_CMD)
    time.sleep(0.002)

def lcd_display_string(message, line):
    if line == 1:
        lcd_byte(LCD_LINE_1, LCD_CMD)
    elif line == 2:
        lcd_byte(LCD_LINE_2, LCD_CMD)

    message = message.ljust(LCD_WIDTH)[:LCD_WIDTH]

    for char in message:
        lcd_byte(ord(char), LCD_CHR)

def lcd_message(line1, line2):
    lcd_clear()
    lcd_display_string(line1, 1)
    lcd_display_string(line2, 2)

def lcd_cleanup():
    lcd_clear()
    bus.close()







# Code:rfid_lcd.py
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

from lcd16x2 import (
    lcd_init,
    lcd_message,
    lcd_clear,
    lcd_cleanup
)

AUTHORIZED_UID = "B9-86-28-03"

reader = SimpleMFRC522()

lcd_init()

print("=" * 50)
print("       RFID + FINGERPRINT + I2C LCD")
print("=" * 50)

print("Initializing I2C LCD...")
print("LCD initialized.")

print("Initializing RFID reader...")
print("RFID reader initialized.")

print()
print("=" * 50)
print("             SYSTEM READY")
print("=" * 50)

print()
print("Step 1: Scan RFID card.")
print("Step 2: Scan fingerprint.")
print()
print("Press Ctrl+C to stop.")

lcd_message("RFID SYSTEM", "READY")

try:

    while True:

        print()
        print("-" * 50)
        print("             RFID CARD DETECTED")
        print("-" * 50)

        lcd_message("RFID CARD", "DETECTING...")

        id, text = reader.read()

        uid = format(id, 'X').upper()

        uid_bytes = id.to_bytes(4, byteorder='big')

        uid_string = "-".join(
            "{:02X}".format(byte)
            for byte in uid_bytes
        )

        print("RFID UID:", uid_string)

        if uid_string == AUTHORIZED_UID:

            print("RFID UID MATCHED")
            print("RFID authentication successful.")

            lcd_message(
                "RFID UID",
                "MATCHED"
            )

            time.sleep(2)

            lcd_message(
                "ACCESS",
                "AUTHORIZED"
            )

            time.sleep(2)

        else:

            print("RFID UID UNMATCHED")
            print("RFID authentication failed.")

            lcd_message(
                "RFID UID",
                "UNMATCHED"
            )

            time.sleep(2)

            lcd_message(
                "ACCESS",
                "DENIED"
            )

            time.sleep(2)

        lcd_message(
            "SCAN RFID",
            "CARD..."
        )

        print()
        print("Ready for next authentication.")

        time.sleep(1)

except KeyboardInterrupt:

    print()
    print("Program stopped.")

finally:

    lcd_cleanup()
    GPIO.cleanup()

    print("GPIO/SPI closed.")
    print("Program completed.")

#
#Simulate door lock by interfacing fingerprint sensor and relay moule with raspberry Pi.
#code
import serial
import adafruit_fingerprint

uart = serial.Serial(
    "/dev/serial0",
    baudrate=57600,
    timeout=1
)

finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

def get_fingerprint_image():
    print("Place finger on sensor...")

    while True:
        result = finger.get_image()

        if result == adafruit_fingerprint.OK:
            print("Image captured.")
            return True

        elif result == adafruit_fingerprint.NOFINGER:
            continue

        else:
            print("Error:", result)
            return False

try:
    location = int(input("Enter fingerprint ID (1-27): "))

    if location < 1 or location > 27:
        print("ID must be between 1 and 27.")
        raise SystemExit

    print("\n--- First Scan ---")

    if not get_fingerprint_image():
        raise SystemExit

    result = finger.image_2_tz(1)

    if result != adafruit_fingerprint.OK:
        print("Could not convert first image.")
        raise SystemExit

    print("Remove your finger...")

    while finger.get_image() != adafruit_fingerprint.NOFINGER:
        pass

    print("\n--- Second Scan ---")
    print("Place the SAME finger again...")

    if not get_fingerprint_image():
        raise SystemExit

    result = finger.image_2_tz(2)

    if result != adafruit_fingerprint.OK:
        print("Could not convert second image.")
        raise SystemExit

    print("Creating fingerprint model...")

    result = finger.create_model()

    if result != adafruit_fingerprint.OK:
        print("Fingerprints did not match.")
        raise SystemExit

    print("Storing fingerprint...")

    result = finger.store_model(location)

    if result == adafruit_fingerprint.OK:
        print("\nFingerprint enrolled successfully!")
        print("Fingerprint ID:", location)
    else:
        print("Could not store fingerprint.")
        print("Error:", result)

finally:
    uart.close()
    print("Serial connection closed.")


#
#Create two factor authentication system by interfacing fingerprint sensor, RFID and relay with Raspberry Pi.
#code
rc522.py
import spidev
import RPi.GPIO as GPIO
import time

class MFRC522:
    CommandReg = 0x01
    CommIEnReg = 0x02
    DivIEnReg = 0x03
    CommIrqReg = 0x04
    DivIrqReg = 0x05
    ErrorReg = 0x06
    Status1Reg = 0x07
    Status2Reg = 0x08
    FIFODataReg = 0x09
    FIFOLevelReg = 0x0A
    WaterLevelReg = 0x0B
    ControlReg = 0x0C
    BitFramingReg = 0x0D
    CollReg = 0x0E

    ModeReg = 0x11
    TxModeReg = 0x12
    RxModeReg = 0x13
    TxControlReg = 0x14
    TxASKReg = 0x15
    TxSelReg = 0x16
    RxSelReg = 0x17
    RxThresholdReg = 0x18
    DemodReg = 0x19

    MfTxReg = 0x1C
    MfRxReg = 0x1D
    SerialSpeedReg = 0x1F

    CRCResultRegH = 0x21
    CRCResultRegL = 0x22
    ModWidthReg = 0x24

    RFCfgReg = 0x26
    GsNReg = 0x27
    CWGsPReg = 0x28
    ModGsPReg = 0x29

    TModeReg = 0x2A
    TPrescalerReg = 0x2B
    TReloadRegH = 0x2C
    TReloadRegL = 0x2D

    VersionReg = 0x37

    PCD_IDLE = 0x00
    PCD_AUTHENT = 0x0E
    PCD_TRANSCEIVE = 0x0C
    PCD_RESETPHASE = 0x0F
    PCD_CALCCRC = 0x03

    PICC_REQIDL = 0x26
    PICC_ANTICOLL = 0x93
    PICC_HALT = 0x50
    PICC_AUTHENT1A = 0x60

    MI_OK = 0
    MI_NOTAGERR = 1
    MI_ERR = 2

    def __init__(self, spi_bus=0, spi_device=0, rst_pin=25):
        self.rst_pin = rst_pin

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.rst_pin, GPIO.OUT)

        self.spi = spidev.SpiDev()
        self.spi.open(spi_bus, spi_device)
        self.spi.max_speed_hz = 1000000
        self.spi.mode = 0

        self.MFRC522_Init()

    def _write_reg(self, addr, val):
        self.spi.xfer2([((addr << 1) & 0x7E), val])

    def _read_reg(self, addr):
        data = self.spi.xfer2([((addr << 1) & 0x7E) | 0x80, 0])
        return data[1]

    def _set_bitmask(self, reg, mask):
        self._write_reg(reg, self._read_reg(reg) | mask)

    def _clear_bitmask(self, reg, mask):
        self._write_reg(reg, self._read_reg(reg) & (~mask))

    def MFRC522_Reset(self):
        self._write_reg(self.CommandReg, self.PCD_RESETPHASE)

    def AntennaOn(self):
        temp = self._read_reg(self.TxControlReg)

        if ~(temp & 0x03):
            self._set_bitmask(self.TxControlReg, 0x03)

    def AntennaOff(self):
        self._clear_bitmask(self.TxControlReg, 0x03)

    def MFRC522_Init(self):
        GPIO.output(self.rst_pin, GPIO.HIGH)
        time.sleep(0.05)

        self.MFRC522_Reset()

        self._write_reg(self.TModeReg, 0x8D)
        self._write_reg(self.TPrescalerReg, 0x3E)
        self._write_reg(self.TReloadRegL, 30)
        self._write_reg(self.TReloadRegH, 0)

        self._write_reg(self.TxASKReg, 0x40)
        self._write_reg(self.ModeReg, 0x3D)

        self.AntennaOn()

    def calculate_crc(self, data):
        self._clear_bitmask(self.DivIrqReg, 0x04)
        self._set_bitmask(self.FIFOLevelReg, 0x80)

        for byte in data:
            self._write_reg(self.FIFODataReg, byte)

        self._write_reg(self.CommandReg, self.PCD_CALCCRC)

        for _ in range(255):
            n = self._read_reg(self.DivIrqReg)

            if n & 0x04:
                break

            time.sleep(0.001)

        return [
            self._read_reg(self.CRCResultRegL),
            self._read_reg(self.CRCResultRegH)
        ]

    def ToCard(self, command, send_data):
        back_data = []
        back_len = 0
        status = self.MI_ERR
        irq_en = 0x00
        wait_irq = 0x00

        if command == self.PCD_AUTHENT:
            irq_en = 0x12
            wait_irq = 0x10

        elif command == self.PCD_TRANSCEIVE:
            irq_en = 0x77
            wait_irq = 0x30

        self._write_reg(self.CommIEnReg, irq_en | 0x80)
        self._clear_bitmask(self.CommIrqReg, 0x80)
        self._set_bitmask(self.FIFOLevelReg, 0x80)
        self._write_reg(self.CommandReg, self.PCD_IDLE)

        for c in send_data:
            self._write_reg(self.FIFODataReg, c)

        self._write_reg(self.CommandReg, command)

        if command == self.PCD_TRANSCEIVE:
            self._set_bitmask(self.BitFramingReg, 0x80)

        i = 2000

        while True:
            n = self._read_reg(self.CommIrqReg)
            i -= 1

            if not (i != 0 and not (n & 0x01) and not (n & wait_irq)):
                break

            time.sleep(0.001)

        self._clear_bitmask(self.BitFramingReg, 0x80)

        if i != 0:
            error = self._read_reg(self.ErrorReg)

            if not (error & 0x1B):
                status = self.MI_OK

                if n & irq_en & 0x01:
                    status = self.MI_NOTAGERR

                if command == self.PCD_TRANSCEIVE:
                    n = self._read_reg(self.FIFOLevelReg)

                    last_bits = self._read_reg(self.ControlReg) & 0x07

                    if last_bits != 0:
                        back_len = (n - 1) * 8 + last_bits
                    else:
                        back_len = n * 8

                    if n == 0:
                        n = 1

                    if n > 16:
                        n = 16

                    for _ in range(n):
                        back_data.append(
                            self._read_reg(self.FIFODataReg)
                        )

        return status, back_data, back_len

    def Request(self, req_mode):
        self._write_reg(self.BitFramingReg, 0x07)

        status, back_data, back_bits = self.ToCard(
            self.PCD_TRANSCEIVE,
            [req_mode]
        )

        if status != self.MI_OK or back_bits != 0x10:
            status = self.MI_ERR

        return status, back_bits

    def Anticoll(self):
        self._write_reg(self.BitFramingReg, 0x00)

        status, back_data, back_bits = self.ToCard(
            self.PCD_TRANSCEIVE,
            [self.PICC_ANTICOLL, 0x20]
        )

        if status == self.MI_OK and len(back_data) == 5:
            checksum = 0

            for i in range(4):
                checksum ^= back_data[i]

            if checksum != back_data[4]:
                status = self.MI_ERR

        return status, back_data

    def SelectTag(self, uid):
        buffer = [
            self.PICC_ANTICOLL,
            0x70
        ] + uid

        crc = self.calculate_crc(buffer)
        buffer += crc

        status, back_data, back_bits = self.ToCard(
            self.PCD_TRANSCEIVE,
            buffer
        )

        if status == self.MI_OK and back_bits == 0x18:
            return back_data[0]

        return 0

    def HaltA(self):
        buffer = [
            self.PICC_HALT,
            0x00
        ]

        buffer += self.calculate_crc(buffer)

        self.ToCard(
            self.PCD_TRANSCEIVE,
            buffer
        )

    def read_uid(self):
        status, _ = self.Request(self.PICC_REQIDL)

        if status != self.MI_OK:
            return None

        status, uid = self.Anticoll()

        if status != self.MI_OK:
            return None

        return uid[:4]

    def get_uid_string(self):
        uid = self.read_uid()

        if uid is None:
            return None

        return "-".join(f"{x:02X}" for x in uid)

    def close(self):
        self.AntennaOff()
        self.spi.close()
        GPIO.cleanup(self.rst_pin)




rfid_test.py
from rc522 import MFRC522
import time

reader = MFRC522()

print("=" * 50)
print("           RFID TEST")
print("=" * 50)

print("MFRC522 initialized.")
print("Place your RFID card near the reader.")
print("Press Ctrl+C to stop.\n")

last_uid = None

try:
    while True:
        uid = reader.get_uid_string()

        if uid:
            if uid != last_uid:
                print("-" * 50)
                print("RFID CARD DETECTED")
                print("-" * 50)
                print("RFID UID:", uid)
                print("RFID test successful.")
                print()

                last_uid = uid

            time.sleep(1)

        else:
            last_uid = None
            time.sleep(0.2)

except KeyboardInterrupt:
    print("\nRFID test stopped.")

finally:
    reader.close()

relay_test.py
import RPi.GPIO as GPIO
import time

RELAY_PIN = 17

RELAY_ON = GPIO.LOW
RELAY_OFF = GPIO.HIGH

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT, initial=RELAY_OFF)

print("=" * 50)
print("             RELAY TEST")
print("=" * 50)

try:
    print("Relay OFF")
    GPIO.output(RELAY_PIN, RELAY_OFF)
    time.sleep(2)

    print("Relay ON")
    GPIO.output(RELAY_PIN, RELAY_ON)
    time.sleep(3)

    print("Relay OFF")
    GPIO.output(RELAY_PIN, RELAY_OFF)
    time.sleep(2)

    print("Relay test completed successfully.")

except KeyboardInterrupt:
    print("\nRelay test stopped.")

finally:
    GPIO.output(RELAY_PIN, RELAY_OFF)
    GPIO.cleanup(RELAY_PIN)	

fingerprint_test.py
import serial
import time
import struct

PORT = "/dev/serial0"
BAUDRATE = 57600

class R307:
    def __init__(self, port=PORT, baudrate=BAUDRATE):
        self.ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            timeout=2
        )

        time.sleep(1)

    def checksum(self, packet):
        return sum(packet) & 0xFFFF

    def send_command(self, command, params=b""):
        address = b"\xFF\xFF\xFF\xFF"
        packet_type = b"\x01"
        length = len(params) + 3

        body = (
            packet_type +
            struct.pack(">H", length) +
            bytes([command]) +
            params
        )

        checksum = self.checksum(body)

        packet = (
            b"\xEF\x01" +
            address +
            body +
            struct.pack(">H", checksum)
        )

        self.ser.reset_input_buffer()
        self.ser.write(packet)

        return self.read_response()

    def read_response(self):
        header = self.ser.read(9)

        if len(header) < 9:
            return None, b""

        if header[0:2] != b"\xEF\x01":
            return None, b""

        packet_type = header[6]
        length = struct.unpack(">H", header[7:9])[0]

        data = self.ser.read(length)

        if len(data) != length:
            return None, b""

        confirmation = data[0]
        params = data[1:-2]

        return confirmation, params

    def verify_password(self):
        password = b"\x00\x00\x00\x00"

        confirmation, _ = self.send_command(
            0x13,
            password
        )

        return confirmation == 0x00

    def get_image(self):
        confirmation, _ = self.send_command(0x01)

        return confirmation

    def image_to_template(self, buffer_id=1):
        confirmation, _ = self.send_command(
            0x02,
            bytes([buffer_id])
        )

        return confirmation

    def search(self, buffer_id=1, start_page=0, page_num=1000):
        params = (
            bytes([buffer_id]) +
            struct.pack(">H", start_page) +
            struct.pack(">H", page_num)
        )

        confirmation, data = self.send_command(
            0x04,
            params
        )

        if confirmation != 0x00:
            return None

        if len(data) < 4:
            return None

        finger_id = struct.unpack(">H", data[0:2])[0]
        score = struct.unpack(">H", data[2:4])[0]

        return finger_id, score

    def close(self):
        self.ser.close()

def wait_for_finger(sensor):
    print("Place your finger on R307...")

    while True:
        result = sensor.get_image()

        if result == 0x00:
            print("Fingerprint detected.")
            return True

        time.sleep(0.2)

sensor = R307()

print("=" * 55)
print("                 FINGERPRINT TEST")
print("=" * 55)

try:
    print("Connecting to R307...")

    if sensor.verify_password():
        print("R307 connected.")
        print("Password verification successful.")

    else:
        print("R307 password verification failed.")
        raise SystemExit

    print()
    print("Stored fingerprints: sensor memory available")
    print()
    print("Place a registered finger on the sensor.")

    wait_for_finger(sensor)

    result = sensor.image_to_template(1)

    if result != 0x00:
        print("Could not convert fingerprint image.")
        raise SystemExit

    result = sensor.search(1, 0, 1000)

    if result:
        finger_id, score = result

        print("Detected fingerprint ID:", finger_id)
        print("Accuracy/Score:", score)
        print("FINGERPRINT MATCHED")
        print("Fingerprint test successful.")

    else:
        print("FINGERPRINT NOT MATCHED")
        print("Fingerprint test failed.")

except KeyboardInterrupt:
    print("\nFingerprint test stopped.")

finally:
    sensor.close()



identify_fingerprint.py
from fingerprint_test import R307
import time

sensor = R307()

print("=" * 55)
print("             FINGERPRINT IDENTIFICATION")
print("=" * 55)

try:
    if not sensor.verify_password():
        print("R307 connection failed.")
        raise SystemExit

    print("R307 connected successfully.")
    print("Stored fingerprint database is ready.")
    print()
    print("Place your registered finger on the sensor.")

    while True:

        result = sensor.get_image()

        if result == 0x00:
            print("Fingerprint detected.")

            result = sensor.image_to_template(1)

            if result != 0x00:
                print("Unable to process fingerprint.")
                time.sleep(1)
                continue

            result = sensor.search(1, 0, 1000)

            if result:
                finger_id, score = result

                print("---------------------------------------")
                print("FINGERPRINT MATCHED")
                print("Fingerprint ID:", finger_id)
                print("Accuracy/Score:", score)
                print("---------------------------------------")

            else:
                print("FINGERPRINT NOT FOUND")

            print("\nReady for next fingerprint...")

            time.sleep(2)

        time.sleep(0.2)

except KeyboardInterrupt:
    print("\nIdentification stopped.")

finally:
    sensor.close()

users.json
{
    "users": [
        {
            "name": "User 1",
            "rfid_uid": "B9-86-28-03",
            "fingerprint_id": 1
        },
        {
            "name": "User 2",
            "rfid_uid": "12-34-56-78",
            "fingerprint_id": 2
        }
    ]
}

access_control.py
import json
import time
import RPi.GPIO as GPIO

from rc522 import MFRC522
from fingerprint_test import R307

RELAY_PIN = 17

RELAY_ON = GPIO.LOW
RELAY_OFF = GPIO.HIGH

USERS_FILE = "users.json"

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT, initial=RELAY_OFF)

def load_users():
    with open(USERS_FILE, "r") as file:
        data = json.load(file)

    return data["users"]

def find_user_by_rfid(users, uid):
    for user in users:
        if user["rfid_uid"].upper() == uid.upper():
            return user

    return None

def authenticate_rfid(reader, users):
    print()
    print("-" * 60)
    print("                    RFID CARD DETECTED")
    print("-" * 60)

    uid = reader.get_uid_string()

    if not uid:
        return None

    print("RFID UID:", uid)

    user = find_user_by_rfid(users, uid)

    if user:
        print("RFID UID MATCHED")
        print("RFID authentication successful.")
        print("User:", user["name"])

        return user

    print("RFID UID NOT MATCHED")
    print("Access denied.")

    return None

def authenticate_fingerprint(sensor, expected_id):
    print()
    print("=" * 60)
    print("                 FINGERPRINT AUTHENTICATION")
    print("=" * 60)

    print("Place your finger on R307...")

    while True:
        result = sensor.get_image()

        if result == 0x00:
            print("Fingerprint detected.")
            break

        time.sleep(0.2)

    result = sensor.image_to_template(1)

    if result != 0x00:
        print("Fingerprint image conversion failed.")
        return False

    result = sensor.search(1, 0, 1000)

    if not result:
        print("FINGERPRINT NOT MATCHED")
        return False

    finger_id, score = result

    print("Detected fingerprint ID:", finger_id)
    print("Accuracy:", score)

    if finger_id == expected_id:
        print()
        print("FINGERPRINT MATCHED")
        print("Fingerprint ID:", finger_id)

        return True

    print()
    print("FINGERPRINT ID DOES NOT MATCH USER")
    print("Expected ID:", expected_id)
    print("Detected ID:", finger_id)

    return False

def grant_access():
    print()
    print("=" * 60)
    print("                 TWO-FACTOR AUTH SUCCESS")
    print("=" * 60)

    print("RFID: MATCHED")
    print("Fingerprint: MATCHED")
    print("ACCESS GRANTED")

    GPIO.output(RELAY_PIN, RELAY_ON)

    print("Relay ON")
    print("Door/lock activated.")

    time.sleep(5)

    GPIO.output(RELAY_PIN, RELAY_OFF)

    print("Relay OFF")
    print("Door/lock secured again.")

reader = MFRC522()
sensor = R307()

try:
    print("=" * 60)
    print("           RFID + FINGERPRINT + RELAY")
    print("=" * 60)

    print()
    print("Initializing MFRC522...")
    print("MFRC522 initialized.")

    print()
    print("Connecting to R307...")

    if sensor.verify_password():
        print("R307 connected.")
        print("Fingerprint sensor ready.")

    else:
        print("R307 connection failed.")
        raise SystemExit

    users = load_users()

    print()
    print("Users loaded:", len(users))

    print()
    print("=" * 60)
    print("                    SYSTEM READY")
    print("=" * 60)

    print()
    print("Step 1: Scan RFID card.")
    print("Step 2: Scan fingerprint.")
    print()
    print("Press Ctrl+C to stop.")

    last_uid = None

    while True:
        uid = reader.get_uid_string()

        if uid:

            if uid != last_uid:

                last_uid = uid

                user = authenticate_rfid(
                    reader,
                    users
                )

                if user:

                    expected_fingerprint = int(
                        user["fingerprint_id"]
                    )

                    fingerprint_ok = authenticate_fingerprint(
                        sensor,
                        expected_fingerprint
                    )

                    if fingerprint_ok:
                        grant_access()

                    else:
                        print()
                        print("=" * 60)
                        print("             TWO-FACTOR AUTH FAILED")
                        print("=" * 60)

                        print("RFID: MATCHED")
                        print("Fingerprint: NOT MATCHED")
                        print("ACCESS DENIED")

                print()
                print("Ready for next authentication...")

                time.sleep(2)

        else:
            last_uid = None

        time.sleep(0.2)

except KeyboardInterrupt:
    print()
    print("Program stopped.")

finally:
    GPIO.output(RELAY_PIN, RELAY_OFF)

    reader.close()
    sensor.close()

    GPIO.cleanup()

    print("GPIO/SPI/UART closed.")
    print("Program completed.")





#
#Design and implement a Node-RED flow on Raspberry Pi that integrates a physical push-button and an LED 
#with a web dashboard. The flow must allow users to toggle the LED from the dashboard and via the physical button. 
#A button press should force the LED ON for 5 seconds and then automatically restore the LED to the dashboard’s last state

'''
Software and libraries required
Software / Node	     Purpose
Node-RED	      Visual flow programming
Dashboard 2.0	   Web dashboard interface
GPIO nodes	      Read button and control LED
Trigger node	   Create 5-second timing
Change and Switch nodes	   Manage LED state

Component	Raspberry Pi 5 connection
LED anode (+)	GPIO27 – Physical pin 13, through 220Ω resistor
LED cathode (−)	GND – Physical pin 6
Push-button first side	3.3V – Physical pin 1
Push-button other side	GPIO17 – Physical pin 11
10kΩ resistor	Between GPIO17 and GND

nstall Node-RED on Raspberry Pi
Step 1: Update Raspberry Pi
sudo apt update
sudo apt upgrade -y

Install Node-RED

If Node-RED is not already installed, use its official Raspberry Pi installation instructions:
Node-RED installation for Raspberry PiStep 3: Enable and start Node-RED
sudo systemctl enable nodered.service
sudo systemctl start nodered.service


Open Node-RED

Find your Raspberry Pi IP address:
hostname -I


Open a browser and enter:
http://YOUR_PI_IP:1880

Install the required Node-RED dashboard
We will use FlowFuse Dashboard 2.0.
1. Open the Node-RED editor.
2. Click the menu (top-right three lines).
3. Select Manage Palette.
4. Open the Install tab.
5. Search for:
@flowfuse/node-red-dashboard

Install GPIO nodes
The Raspberry Pi GPIO nodes allow Node-RED to read the physical button and control the LED.
1. Open Manage Palette.
2. Select Install.
3. Search for:
node-red-node-pi-gpio


'''


#
#Design IoT based home automation system using Raspberry Pi

