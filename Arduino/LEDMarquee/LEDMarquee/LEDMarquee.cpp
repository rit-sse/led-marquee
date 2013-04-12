/*
 * LEDMarquee.cpp
 *
 * Created: 4/12/2013 6:01:46 PM
 *  Author: corb
 */ 


#include <avr/io.h>
#include <math.h>

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
	DDRB = 0b00000111;
	DDRL = 0b11111111;
	PORTF = 0b11111111;
    PORTK = PORTF; 
    PORTA = PORTF; 
    PORTC = PORTF; 
    PORTB = PORTF;	
}

int main(void)
{
	setup();
	int rows = 8;
    while(1)
    {
		/*
		The default loop, this needs to stay in place in order
		to scan through the rows
		*/
		for (int i = 1; i <= pow(rows,2); i<<=1) {
			//Set your row state here
			PORTL = ~i;
		}
	}
}