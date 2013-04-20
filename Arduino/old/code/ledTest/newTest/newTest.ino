#include <FrequencyTimer2.h>


// Test patterns:
#define SPACE { \
    {0, 0, 0, 0, 0}, \
    {0, 0, 0, 0, 0}, \
    {0, 0, 0, 0, 0}, \
    {0, 0, 0, 0, 0}, \
    {0, 0, 0, 0, 0}, \
    {0, 0, 0, 0, 0}, \
    {0, 0, 0, 0, 0}  \
}

#define H { \
    {1, 0, 0, 0, 1}, \
    {1, 0, 0, 0, 1}, \
    {1, 0, 0, 0, 1}, \
    {1, 1, 1, 1, 1}, \
    {1, 0, 0, 0, 1}, \
    {1, 0, 0, 0, 1}, \
    {1, 0, 0, 0, 1}  \
}




// Rows are negative (cathode)
// Cols are positive (anode)

const int numRows = 7;
const int numCols = 5;

int pins[(numRows + numCols)] = {9, 8, 7, 6, 5, 4, 3, 22};

int rows[numRows] = {pins[0], pins[1], pins[2], pins[3], pins[4], pins[5], pins[6]};
int cols[numCols] = {pins[4]};

byte leds[numRows][numCols];

// Patterns testing:
byte col = 0;
const int numPatterns = 2;
byte patterns[numPatterns][numRows][numCols] = {
  H,SPACE
};

int pattern = 0;


void setup() {
  // put your setup code here, to run once:
  // set up all pins
  for (int i = 0; i < (numRows + numCols); i++){
    pinMode(pins[i], OUTPUT);
    digitalWrite(pins[i], LOW);
  }
  
  clearLeds();
  
  // Not sure how the following works.
  FrequencyTimer2::disable();
  // Set refresh rate (interrupt timeout period)
  FrequencyTimer2::setPeriod(2000);
  // Set interrupt routine to be called
  FrequencyTimer2::setOnOverflow(display);

  setPattern(pattern);
  
  
  
}

void loop() {
  // put your main code here, to run repeatedly: 
  pattern = ++pattern % numPatterns;
  slidePattern(pattern, 60);
}


void clearLeds() {
  // Clear display array
  for (int i = 0; i < numRows; i++){
    for (int j = 0; j < numCols; j++) {
      leds[i][j] = 0;
    }
  }
}

void setPattern(int pattern) {
  for (int i = 0; i < numRows; i++) {
    for (int j = 0; j < numCols; j++) {
      leds[i][j] = patterns[pattern][i][j];
    }
  }
}

void slidePattern(int pattern, int del) {
  for (int l = 0; l < 8; l++) {
    for (int i = 0; i < 7; i++) {
      for (int j = 0; j < 8; j++) {
        leds[j][i] = leds[j][i+1];
      }
    }
    for (int j = 0; j < 8; j++) {
      leds[j][7] = patterns[pattern][j][0 + l];
    }
    delay(del);
  }
}

// Interrupt routine
void display() {
  digitalWrite(cols[col], LOW);  // Turn whole previous column off
  col++;
  if (col == numCols) {
    col = 0;
  }
  for (int row = 0; row < numRows; row++) {
    if (leds[col][7 - row] == 1) {
      digitalWrite(rows[row], LOW);  // Turn on this led
    }
    else {
      digitalWrite(rows[row], HIGH); // Turn off this led
    }
  }
  digitalWrite(cols[col], HIGH); // Turn whole column on at once (for equal lighting times)
}
