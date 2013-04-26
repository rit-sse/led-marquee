/**
* ledMarquee.ino
* 
* Arduino side of the SSE LED Marquee.
* Receives a char[] over i2c from the Raspberry Pi, 
* handles the char[], prints it out to the LEDs, scrolling.
* 
*/



#include <math.h>
#include <stdlib.h>
#include <string.h>
#include <ctypes.h>
#include <Wire.h>
#include "Timer.h"

// Font file from font.ino in the same directory.
// Usage:   FONT[(ASCII value - 32)]   <-- gives a character.
extern const byte FONT[97][8];

Timer t;
byte* outChar;

void setup(){
	
	/*
	This sets up the ports for output
	ports E,K,A,C, and B are the columns,
	while port L is the rows
	*/
	DDRF = 0b11111111;
	DDRK = 0b11111111;
	DDRA = 0b11111111;
	DDRC = 0b11111111;
	DDRB = 0b11100000;
	DDRL = 0b11111111;

  t.every(1000, updateChar);

  // i2c setup 
  Wire.begin(4);                // join i2c bus with address #4
  Wire.onReceive(receiveEvent); // register event
  //Serial.begin(9600);           // start serial for output
  outChar = lookup('H'); //(byte*)calloc(7, sizeof(byte));
}


// Executes whenever data is received from the RPi over i2c.
// This function is registered as an event, see setup().
void receiveEvent(int howMany)
{
  while(Wire.available()) // While there is data to be read
  {
    char c = Wire.read(); // receive byte as a character
    //Serial.print(c);         // print the character
    free(outChar);
    outChar = lookup(c);
    //Serial.println(*outChar, HEX);
    //Serial.println("Freed");
  }
}

// Takes an int (ASCII value of a character) and looks up
// and returns the character.
//uint16_t* lookup(int ascii){
byte* lookup(char ascii){
  if (ascii < 32)
    return NULL;
  ascii -= 32;
  byte* character = (byte*)calloc(7, sizeof(byte));
  memcpy(character,FONT[ascii], sizeof(byte)*7);
  return character;
}

byte charArray[] = "Hello, Corb!";
int charIndex = 0;

void updateChar(){
  free(outChar);
  outChar = lookup(charArray[charIndex++]);
  charIndex %= sizeof(charArray)/sizeof(charArray[0]) - 1;
}

void loop(){
  t.update();
  int rows = 8;
  /* 
  The default loop, this needs to stay in place in order
  to scan through the rows
  */
  int index = 0;
  for (int i = 1; i <= pow(rows,2); i<<=1) {
    
    //int strLen = 2;
    //uint16_t row= 0;
    //Serial.println(row, BIN);
    //row |= FONT[40][index] << (8 * (strLen - 1));
    //Serial.println(row, BIN);
    //row |= FONT[37][index] << 2;
    //Serial.println(row, BIN);
    //row |= FONT[37][index];
    //Set your row state here
    //PORTF = row >> 8;
    //PORTK = row & 0x00FF;
    //PORTK = FONT[37][index];
    //PORTA = FONT[44][index];
    //PORTC = FONT[44][index];
    //PORTB = FONT[47][index];
    PORTF = outChar[index++];
    PORTL = ~i;
    delay(2);
  }
  
}
