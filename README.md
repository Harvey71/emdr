# emdr

Do It Yourself EMDR equipment (lightbar, buzzers and headphones). Firmware and controller app. 

## Hardware

Please watch this [video](https://youtu.be/0NRr-7e_mLk) about the project.

### Light bar

![light bar](artwork/lightbar.jpg)

The invention of LED stripes with ready mounted LED pixels makes the DIY manufacturing of EMDR light bar a piece of cake. :-)

The only electrical component missing from these stripes is an USB connection. This is done by a Teensy microcontroller,
which implements a USB peripheral protocol on the one hand and the WS2812 serial bus on the other. The USB connection
also powers the microcontroller and the LEDs. Fortunately, an EMDR light bar has never more than one LED illuminated
at the same time, so USB current is sufficient.

Wiring is quite simple, since the Teensy LC already has a 5 V driver on board. 
Please refer to https://github.com/PaulStoffregen/WS2812Serial.

#### Parts list

amount|article|example order link
---|----|----
1|WS2812 LED strip, 1m, 60 LEDs|https://www.amazon.de/gp/product/B01CDTED80
1|Teensy LC microcontroller|https://www.amazon.de/gp/product/B07CXMMP1T
1|aluminium profile for led strips|https://www.amazon.de/gp/product/B06XFT5X4T
2|end caps for led stip profile|https://www.amazon.de/gp/product/B06XGDJPG8
1|reduceer bushing 1/4" to 3/8"|https://www.amazon.de/gp/product/B01MT77RHN
1|mini tripod|https://www.amazon.de/gp/product/B001IXSIE8
950 mm|square wooden staff 19x19 mm|hardware store
1|Teensy case|[www.thingiverse.com/thing:2841269](https://www.thingiverse.com/thing:2841269)
6|countersunk screw 3.0x12 mm|hardware store
1|micro USB cable 1.8m|https://www.amazon.de/dp/B01GGKYE4U

### Buzzers

![buzzers](artwork/buzzers.jpg)


#### Parts list

It would be some act of handcraft to build your own buzzers. It is way easier to purchase some proper erotic device 
called "bullet vibrator" and disassemble the needed parts. 
You just should not tell your clients about the original purpose of these buzzers. ;-)

Again, to connect the buzzers to an USB bus, a Teensy microcontroller is used. Other than with the lightbar you need some
extra electronic components to drive the buzzer motors.

amount|article|example order link
---|----|----
2|bullet vibrator|https://www.amazon.de/gp/product/B000W735GC
1|Teensy LC microcontroller|https://www.amazon.de/gp/product/B07CXMMP1T
1|ULN2001A transistor array|[https://www.conrad.de/de/p/stmicroelectronics...](https://www.conrad.de/de/p/stmicroelectronics-transistor-bjt-arrays-uln2001a-dip-16-anzahl-kanaele-7-npn-darlington-177954.html)
1|resistor 10R, 1W|[https://www.conrad.de/de/p/weltron...](https://www.conrad.de/de/p/weltron-mfr1145-metallschicht-widerstand-10-axial-bedrahtet-0414-1-w-1-1-st-419320.html)
1|perfboard|[https://www.conrad.de/de/p/tru-components...](https://www.conrad.de/de/p/tru-components-su527769-europlatine-hartpapier-l-x-b-160-mm-x-100-mm-35-m-rastermass-2-54-mm-inhalt-1-st-1570681.html)
1|plasic case 75x25x56 mm|https://www.amazon.de/gp/product/B003WGT3N4
4|rubber base self-adhesive|[https://www.conrad.de/de/p/3m-sj-5302...](https://www.conrad.de/de/p/3m-sj-5302-mpcb-geraetefuss-selbstklebend-rund-transparent-x-h-7-9-mm-x-2-2-mm-80-st-527826.html)
1|micro USB cable 1.8m|https://www.amazon.de/dp/B01GGKYE4U
1|single row pin header (male & female)|https://www.amazon.de/dp/B016U9XYBG


#### Electronic schematic
![buzzer electronic schema](artwork/buzzer_sch.png)

#### Electronic layout
![buzzer electronic schema](artwork/buzzer_pcb.png)


### Controller

![controller](artwork/controller.jpg)

Controller is optional. You can also use a PC or Laptop with MacOS, Windows oder Linux to run the controller software.

amount|article|example order link
---|----|----
1|Raspberry Pi model B+|https://www.amazon.de/gp/product/B07BDR5PDW
1|Micro SD-card 16 GB|https://www.amazon.de/gp/product/B008RDCCR6
1|3.5" touchscreen with case for raspberry pi|https://www.amazon.de/gp/product/B07S8CKW58
1|Pi 3 power adapter|https://www.amazon.de/dp/B01566WOAG

### Headphones

Sound stimulation is played by the integrated sound hardware, either of your PC or Raspberry Pi standalone controller.
Just attach an appropriate headphone to the sound jack.

## Software

### Lightbar and buzzers

Easiest way to program the Teensy microcontrollers is to use the [Arduino IDE](https://www.arduino.cc/en/Main/Software) with
[Teensyduino](https://www.pjrc.com/teensy/td_download.html) extention. You can run this on MacOS, Windows or Linux.
Just start the IDE, load the proper Arduino project file from my repository (subdirectory "firmware"), 
attach the teensy device, press the programming button on the device and the upload button in the IDE. Done.

You can test the device by using the Arduino serial monitor tool. Just send the letter "i". You sould receive the
device identifier, either "EMDR Lightbar" or "EMDR Buzzer".

### Controller

#### On PC

Since the controller is a python script, you can run it on any platform supported by pyGame and pyUSB, e.g. Windows,
MacOS or Linux. You have to have Python 3.x installed.

Copy the files from my repository (subdirecotry "controller"), including the "imgs" directory.
Install necessary libraries with `pip install -r requirements.txt`or `pip3 install -r requirements.txt`.
In order to run the pyUSB library, you also need "libusb" to be installed. Please
see https://github.com/pyusb/pyusb for further instructions.

#### On Raspberry Pi

To set up a standalone controller on a Raspberry Pi, you would have to do some expert work, like installing a
Linux OS on a SD card, install an start the LCD driver for the touchscreen display, istall libusb,
change password, configure for graphical desktop with auto login, download and install the controller software
from my repository and set up the desktop to autostart the controller software after boot.

But fotunately, there is [PiBakery](https://www.pibakery.org/). You can use the "recipe"-File from my repository
(subdirectory "pi") and PiBakery to burn a ready-to-go SD-card. At the very first boot, the Raspberry Pi will download
and install all necessary software. For that, the Pi will have to have internet access. Just attach the Pi to your
local ethernet. After a while, the Pi reboots and shows the controller software. From now on, no network connection
is needed again. You can use the Pi as a simple controller panel for the EMDR equipment. 

