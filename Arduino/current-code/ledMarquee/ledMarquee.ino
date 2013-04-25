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

// Font file from font.ino in the same directory.
// Usage:   FONT[(ASCII value - 32)]   <-- gives a character.
extern const char FONT[97][8];


void setup(){
	
	/*
	This sets up the ports for output
	ports E,K,A,C, and B are the columns,
	while port L is the rows
	*/
	DDRF = B11111111;
	DDRK = B11111111;
	DDRA = B11111111;
	DDRC = B11111111;
	DDRB = B11100000;
	DDRL = B11111111;

  // i2c setup 
  Wire.begin(4);                // join i2c bus with address #4
  Wire.onReceive(receiveEvent); // register event
  Serial.begin(9600);           // start serial for output
}


// Executes whenever data is received from the RPi over i2c.
// This function is registered as an event, see setup().
void receiveEvent(int howMany)
{
  while(Wire.available()) // While there is data to be read
  {
    char c = Wire.read(); // receive byte as a character
    Serial.println(c);         // print the character
    Serial.println(lookup((int) c));
  }
}

int shiftSize[] = { 32, 24, 16, 8, 0 };

// Takes an int (ASCII value of a character) and looks up
// and returns the character.
//uint16_t* lookup(int ascii){
char* lookup(int ascii){
  if (!(ascii >= 32))
    return 0;
  ascii -= 32;
  //uint16_t* row = calloc(7, sizeof(uint8_t));
  char character[8];
  strcpy(character,FONT[ascii]);
  /*for (int i = 0; i < 7 ; i++){
    character[i] >>= 2; 
    character[i] <<= shiftSize[i];
    (*row)[i] |= character[i];
  }
  return row;
  */
  return character;
}

void loop(){
  int rows = 8;
  /* 
  The default loop, this needs to stay in place in order
  to scan through the rows
  */
  int index = 0;
  for (int i = 1; i <= pow(rows,2); i<<=1) {
    
    int strLen = 2;
    uint16_t row= 0;
    //Serial.println(row, BIN);
    row |= FONT[40][index] << (8 * (strLen - 1));
    //Serial.println(row, BIN);
    row |= FONT[37][index] << 2;
    //Serial.println(row, BIN);
    //row |= FONT[37][index];
    //Set your row state here
    PORTF = row >> 8;
    PORTK = row & 0x00FF;
    //PORTK = FONT[37][index];
    //PORTA = FONT[44][index];
    //PORTC = FONT[44][index];
    //PORTB = FONT[47][index];
    index++;
    PORTL = ~i;

    delay(2);
  }
  
}
