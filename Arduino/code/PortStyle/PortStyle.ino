#include <math.h>

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
	DDRB = B00000111;
	DDRL = B11111111;
	PORTF = B11111111;
        PORTK = PORTF; 
        PORTA = PORTF; 
        PORTC = PORTF; 
        PORTB = PORTF;
        //Serial.begin(9600);
}

void loop(){
  int rows = 8;
  /* 
  The default loop, this needs to stay in place in order
  to scan through the rows
  */
  for (int i = 1; i <= pow(rows,2); i<<=1) {
    //Set your row state here
    PORTL = ~i;
    delay(100);
  }
}
