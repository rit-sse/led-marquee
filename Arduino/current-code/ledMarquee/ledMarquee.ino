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
#include <limits.h>

// Font file from font.ino in the same directory.
// Usage:   FONT[(ASCII value - 32)]   <-- gives a character.
extern byte FONT[217][8];
char** board;
String input;

// Executes whenever data is received from the RPi over i2c.
// This function is registered as an event, see setup().
void receiveEvent(int howMany)
{
  input = "";
  while(Wire.available()) { //While we've got data
    char c = Wire.read();
    if (c != '\n')
      input += c;
  }

  free(*board); 
  free(board);
  board = parse(input);
}

// Takes an int (ASCII value of a character) and looks up
int lookup(char ascii){ 
  if (((int)ascii) < 32){
    return 135;
  }
  return ((int) ascii) - 32;
}

String* show(const void *object, size_t size){
  String* str = new String;
  const unsigned char *byte;
  for ( byte = (unsigned char*)object; size--; ++byte ){
    unsigned char mask;
    for ( mask = 1 << (CHAR_BIT - 1); mask; mask >>= 1 ){
      *str += (mask & *byte ? '*' : '.');
    }
  }
  *str += '\n';
  return str;
}

void shiftr(char *chars, int rightShifts, int length) {
  if (!(rightShifts >= 1 && rightShifts <= 7))
    return;

  int leftShifts = 8 - rightShifts;

  char previouschar = chars[0]; // keep the char before modification
  chars[0] = (char) (((chars[0] & 0xff) >> rightShifts) | ((chars[length - 1] & 0xff) << leftShifts));
  for (int i = 1; i < length; i++) {
    char tmp = chars[i];
    chars[i] = (char) (((chars[i] & 0xff) >> rightShifts) | ((previouschar & 0xff) << leftShifts));
    previouschar = tmp;
  }
}

int getlen(char charArray[]){
  if (strlen(charArray)*8 < 35){
    return strlen(charArray);
  } 
  else {
    return 5;
  }
}

char** parse(String str){
  char charArray[str.length()+1];

  str.toCharArray(charArray, str.length()+1);

  strrev(charArray);

  /* construct the board */
  char* row = (char*) calloc(strlen(charArray)*7, sizeof(char));
  char** board = (char**) malloc(7*sizeof(char*));
  for (int i = 0; i < 7; ++i){
    board[i] = row + i*strlen(charArray);
  }

  for (int c = 0; c < strlen(charArray); c++){
    for (int i = 0; i < 7; i++){
      *(board[i]) |= FONT[lookup(charArray[c])][i];
      if (c != strlen(charArray)-1){ 
        shiftr(board[i], 6, strlen(charArray)); 
      }
    }
  }

  return board;
}

void printBoard(String inString){
  for (int i = 0; i < 7; i++){
    String* str = show(board[i], inString.length());
    Serial.print(*str);
    free(str);
  }
}

void setup(){
  /*
  Hard coding in the degree sign. 
  At the moment, looking up the degree sign is incorrect.
  Therefore, any unknown character prints a degree sign.
  */
  FONT[135][0] = 0x70;
  FONT[135][1] = 0x88;
  FONT[135][2] = 0x88;
  FONT[135][3] = 0x70;
  FONT[135][4] = 0x00;
  FONT[135][5] = 0x00;
  FONT[135][6] = 0x00;
  FONT[135][7] = 0x00;

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

  // i2c setup 
  Wire.begin(4);                // join i2c bus with address #4
  Wire.onReceive(receiveEvent); // register event
  Serial.begin(9600);           // start serial for output
  board = parse("SSELED");
  printBoard("SSELED");
}



void loop(){

  int rows = 8;
  /* 
   The default loop, this needs to stay in place in order
   to scan through the rows
   */

  int index = 0;
  for (int i = 1; i <= pow(rows,2); i<<=1) {
    //Set your row state here
    PORTF = board[index][0];
    PORTK = board[index][1];
    PORTA = board[index][2];
    PORTC = board[index][3];
    PORTB = board[index][4];
    PORTL = ~i;
    index++;
    delay(2);
  }
}

