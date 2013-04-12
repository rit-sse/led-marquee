// cols[] : pins, anode
int cols[4] = {22, 23, 24, 25};

// rows[] : pins, cathode
int rows[4] = {8, 9, 10, 11};


void setup() {
  // put your setup code here, to run once:
  int inMin = 22;
  int inMax = 25;
  for(int i=inMin; i<=inMax; i++)
  {
    pinMode(i, OUTPUT);
    digitalWrite(i, LOW);
  }
  
  inMin = 8;
  inMax = 11;
  for(int i=inMin; i<=inMax; i++)
  {
    pinMode(i, OUTPUT);
    digitalWrite(i, LOW);
  }
  
}

void loop() {
  // put your main code here, to run repeatedly: 
  delay(2000);
  setLed(0, 0, true);
  delay(2000);
  setLed(0, 0, false);
  
  
}

void setLed(int row, int col, boolean state){
  if (state == true){
    digitalWrite(rows[row], HIGH);
    digitalWrite(cols[col], LOW);
  } else {
    digitalWrite(rows[row], LOW);
    digitalWrite(cols[col], HIGH);
  }
}
