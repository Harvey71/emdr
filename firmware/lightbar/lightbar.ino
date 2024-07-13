#define BUFLEN 200
#define NUMLED 57

#if defined(__MKL26Z64__)
  // Teensy LC
  #define PIN 24
  #define BAUD_RATE 115200
#else
  // other Teensy, like Teensy 4.0
  #define PIN 1
  #define BAUD_RATE 115200
#endif

#define ID "EMDR Lightbar"

#include "WS2812Serial.h"

byte drawingMemory[NUMLED * 3];
DMAMEM byte displayMemory[NUMLED * 12];
WS2812Serial leds(NUMLED, displayMemory, drawingMemory, PIN, WS2812_GRB);

void setup() {
  Serial.begin(BAUD_RATE);
  leds.begin();
  test();
}

void test() {
  leds.setPixel(0, 0x002000);
  leds.setPixel(NUMLED - 1, 0x200000);
  leds.show();
  delayMicroseconds(500 * 1000);
  leds.clear();
  leds.show();
}

void readln(char* buf) {
  char c = 0;
  int cntr = 0;
  while (c != '\n') {
    if (cntr >= BUFLEN - 1) {
      break;
    }
    if (Serial.available()) {
      c = Serial.read();
      if (c != '\r' && c != '\n') {
        *buf++ = c;
        cntr += 1;
      }
    }
  }
  *buf = 0;
}

void readcmd(char& cmd, int& val) {
  cmd = 0;
  val = 0;
  char buf[BUFLEN];
  char* s = buf;
  readln(buf);
  if (strlen(s)) {
    cmd = *s++;
  }
  if (strlen(s)) {
    val = atoi(s);  
  }
}

void loop() {
  char cmd;
  int val;
  int col = 0x0f0000;
  while (true) {
    readcmd(cmd, val);
    switch (cmd) {
      // color cmd
      case 'c': 
        col = val;
        break;
      // led cmd
      case 'l':
        leds.clear();
        if (val > 0 && val <= NUMLED) {
          leds.setPixel(val - 1, col);
        }
        leds.show();
        break;
      // test command
      case 't' :
        leds.clear();
        leds.setPixel(0, col);
        leds.setPixel(NUMLED - 1, col);
        leds.show();
        break;
      // id command
      case 'i':
        Serial.println(ID);
        break;
    }
  }
}
