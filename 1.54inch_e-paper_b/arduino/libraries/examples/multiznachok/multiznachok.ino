/* Multiznachok (мультизначок): Flippable E-Paper badge
 * Demonstrates the epd1in54bRLE library (like wavesgare's epd1in54b, but with RLE support).
 * To create an RLE image from (e.g.) MY_BLACK_ASCII_200X200_PBM_IMAGE.pbm:
 *   * python pbm2epd.py < MY_BLACK_ASCII_200X200_PBM_IMAGE.pbm > MY_BLACK_IMAGE.cpp
 *   * edit MY_BLACK_IMAGE.cpp and change BITMAP_NAME_GOES_HERE to MY_BLACK_IMAGE
 *   * define MY_BLACK_IMAGE at imagedata.h
 *   * add it to black_pages
 *   * If you also have a red layer, do the same with MY_RED_ASCII_200X200_PBM_IMAGE.pbm
 *   * If you only have a black (or red) layer, use NULL as the other layer
 */
#include <SPI.h>
#include <epd1in54bRLE.h>
#include "imagedata.h"


#define NUM_PAGES 4
const unsigned char *black_pages[NUM_PAGES] = { coen, jazz_black, dod_black, galei_black };
const unsigned char *red_pages[NUM_PAGES] =   { NULL, jazz_red,   dod_red,   galei_red };

#define BUTTON_PREV 15
#define BUTTON_NEXT 14
#define LED_OK 6 // Should be pwm
#define LED_OK_LEVEL 32 // save some power ;)
#define LED_INIT_LEVEL 255 // good way to tell whether we're stuck in epd init

Epd epd;
int page = 0;

void displayPage(void) {
  analogWrite(LED_OK, LED_INIT_LEVEL);
  Serial.println("Initializing...");
  int ret = epd.Init();
  if (ret != 0) {
    Serial.println("Failed");
    while (true) {
      digitalWrite(13, LOW);
      delay(250);
      digitalWrite(13,HIGH);
      delay(250);
    }
  }
  analogWrite(LED_OK, 0);
  Serial.println("Displaying...");
  //epd.DisplayFrame(black_pages[page], red_pages[page]);
  epd.DisplayRLE(black_pages[page], red_pages[page]);
  Serial.println("Done");
  epd.Sleep();
  analogWrite(LED_OK, LED_OK_LEVEL);
}

void setup() {
  pinMode(BUTTON_PREV, INPUT_PULLUP);
  pinMode(BUTTON_NEXT, INPUT_PULLUP);
  pinMode(LED_OK, OUTPUT);
  analogWrite(LED_OK, LED_OK_LEVEL);
  Serial.begin(9600);
  displayPage();
}

void loop() {
  if (digitalRead(BUTTON_NEXT) == LOW) {
    page = (page + 1) % NUM_PAGES;
    displayPage();
  } else if (digitalRead(BUTTON_PREV) == LOW) {
    page = (page + NUM_PAGES - 1) % NUM_PAGES;
    displayPage();
  }
  delay(20);
}
