## LED Blinking Patterns and Telegram-Based GPIO Control Using Raspberry Pi 5      

#Project Creation:
"New Project->Next->Next->Create FirmWare Project->Family(Raspberry Pi)->Next->Finish"

#For LED:
"On left pane click 2nd opt->Tap 'P'->search 'LED'"

"Drag  Button & attach Gnd and Vcc"


#Code:

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

leds = [17, 27, 22, 23]

for led in leds:
    GPIO.setup(led, GPIO.OUT)

while True:
    for led in leds:
        GPIO.output(led, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(led, GPIO.LOW)

    choice = input("Press q to terminate or Enter to continue: ")

    if choice.lower() == 'q':
        break


## Interface TM1637 with Raspberry Pi and Display current time.

#Project Creation:
"Create New Flowchart->Next->(make sure family is rasp.pi 3)Next->Finish"

#Steps:
#1."Right Click Peripherals->"
"Add periferal->"
"Category:Display->"
"7 Segment Display"

#2."Drag Assignment Block(Sqaure)Under Setup->"
"Double Click Assignment-> "
"New(Under Variables)->"
"Add:  Var name=tm,Type=TIME , Var name=hr,Type=INTERGER , Var name=mn,Type=INTEGER , Var name=cur_tm,Type=STRING"

#3."Under Assignment empty list Select:"
"tm :=tm"
"hr :=tmHour(tm)"
"mn :=tmMinute(tm)"
"cur_tm :=toString(hr)+toString(mn)"

#4."Under Peripherals -> U2(Rpi LED Matrix)"
"Select printString-> Drag & place under Assignment Block"
"double click printString->"
"Under Arguments->Strings :=cur_tm"




## Interface 16x2 LCD with Raspberry Pi using I2C module to display text.

#Project Creation:
"Create New Flowchart->Next->(make sure family is rasp.pi 3)Next->Finish"

#Steps:
#1."Right Click Peripherals->"
"Add periferal->"
"Category:Display->"
"I2c LCD Display"

#2."Under Peripherals -> LCD1(I2c controller LDC)"
"Select print & drag drop under Setup->"
"Under Arguments->Strings ='The Text You want to print in dbl quotes'"


