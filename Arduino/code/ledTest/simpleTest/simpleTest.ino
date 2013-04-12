// cols[] : pins, anode
int cols[36] = {22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 14, 15, 16};

// rows[] : pins, cathode
int rows[7] = {9, 8, 7, 6, 5, 4, 3};


void setup() {
  // put your setup code here, to run once:
  int inMin = 3;
  int inMax = 55;
  for(int i=inMin; i<=inMax; i++)
  {
    pinMode(i, OUTPUT);
    digitalWrite(i, HIGH);
  } 
}

void loop() {
  // put your main code here, to run repeatedly:
  for (int i = 0; i <= 35; i++){
    setCol(i);
    delay(200);
  }
  
  for (int i = 0; i <= 7; i++){
    setRow(i);
    delay(200);
  }
  
  for (int row = 0; row < 7; row++){
    for (int col = 0; col < 35; col++){
      setLed(row, col);
      delay(300);
    }
  }
}

void setLed(int row, int col){
  
  for (int i = 0; i < sizeof(cols); i++){
    digitalWrite(cols[i], LOW);
  }
  for (int i = 0; i < sizeof(rows); i++){
    digitalWrite(rows[i], HIGH);
  }
  digitalWrite(rows[row], LOW);
  digitalWrite(cols[col], HIGH);
}


void setRow(int row){
  for (int i = 0; i <= sizeof(cols); i++){
    digitalWrite(cols[i], HIGH);
  }
  for (int i = 0; i <= sizeof(rows); i++){
    digitalWrite(rows[i], HIGH);
  }
  digitalWrite(rows[row], LOW);
}

void setCol(int col){
  for (int i = 0; i <= sizeof(cols); i++){
    digitalWrite(cols[i], LOW);
  }
  for (int i = 0; i <= sizeof(rows); i++){
    digitalWrite(rows[i], LOW);
  }
  digitalWrite(cols[col], HIGH);
}
