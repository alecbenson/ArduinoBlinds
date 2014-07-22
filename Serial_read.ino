int incomingByte = 0;
char incomingData[80];
int index = 0;
int lastIndex = 0;

void setup() {
  Serial.begin(9600);
}


void loop() {
  
  //Read in data from serial
  if (Serial.available() > 0) {
    incomingByte = Serial.read();
    incomingData[index] = incomingByte;
    index++;
  }
  
  //If nothing has changed since last iteration, print the string
  if(index == lastIndex && index != 0){
    Serial.println(incomingData);
    memset(incomingData, 0, sizeof(incomingData) );
    index = 0;
    lastIndex = 0;
  }
  
  lastIndex = index;
  delay(1000);
}