int incomingByte = 0;

#include <Servo.h>
int press1 = 0;
Servo servo;


void setup() {
  Serial.begin(9600);
}


void loop() {
  
  //Read in data from serial
  if (Serial.available() > 0) {
    incomingByte = Serial.read();
    Serial.println(incomingByte);
    
    if(incomingByte == (byte)97 ){
      counterClockWise(5000);
    }
    else if(incomingByte == (byte)98 ){
      clockWise(5000);
    }
  }
  delay(100);
}

void clockWise(int ms){
  servo.attach(7);
  servo.write(160);
  delay(ms);
  servo.detach();
}

void counterClockWise(int ms){
  servo.attach(7);
  servo.write(20);
  delay(ms);
  servo.detach();
}

