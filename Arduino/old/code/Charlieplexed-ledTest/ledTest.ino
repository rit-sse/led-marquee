/* Example 1 for Chaplex - a library to control charlieplexed leds
 * *** randomly flickering leds ***
 * 
 * using minimal multiplex steps to controll all leds
 * 
 * author Stefan Götze
 * version 1.0
 *
 * tested with Arduino Uno and ATTiny85
 */
 
#include "Chaplex.h"

byte ctrlpins[] = {2,3,4};    //Arduino pins controlling charlieplexed leds
#define PINS 3                //number of these pins 

#define NEWPATTERN 100        //100 ms for new LED pattern

Chaplex myCharlie(ctrlpins, PINS);     //control instance

charlieLed myLeds[6]  = {{ 0 , 1 },    //controlled leds in sorted order
                         { 1 , 0 },    // every element is one led with 
                         { 1 , 2 },    // {anode-pin,cathode-pin}
                         { 2 , 1 },    // "pin" means here - index in ctrlpins
                         { 2 , 0 },    // array defined above
                         { 1 , 0 }};
                         

void setup() {
}

void loop() {
  //myCharlie.outRow();
  myCharlie.ledWrite(myLeds[0], 1);
  myCharlie.outRow();
  delay(1000);
  myCharlie.ledWrite(myLeds[1], 1);
  myCharlie.outRow();
  delay(1000);
  myCharlie.ledWrite(myLeds[2], 1);
  myCharlie.outRow();
  delay(1000);
  myCharlie.ledWrite(myLeds[3], 1);
  myCharlie.outRow();
  delay(1000);
  myCharlie.ledWrite(myLeds[4], 1);
  myCharlie.outRow();
  delay(1000);
  myCharlie.ledWrite(myLeds[5], 1);
  myCharlie.outRow();
  delay(1000);
  myCharlie.allClear()
  delay(2000);
}
