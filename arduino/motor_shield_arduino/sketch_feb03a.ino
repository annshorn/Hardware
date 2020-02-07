/*************************************************************
Motor Shield 1-Channel DC Motor Demo
by Randy Sarafan

For more information see:
https://www.instructables.com/id/Arduino-Motor-Shield-Tutorial/

*************************************************************/

void setup() {
  
  //Setup Channel A
  pinMode(12, OUTPUT); //Initiates Motor Channel A pin
  pinMode(9, OUTPUT); //Initiates Brake Channel A pin

  Serial.begin(9600);
  while (! Serial);
  //Serial.println("Speed 0 to 255");
  
}

void loop(){

  if (Serial.available()) {
      int speed = Serial.parseInt();
      Serial.print(speed);Serial.print("\n");
      if (speed >= 0 && speed <= 255) {
         analogWrite(3, speed);
      }
  }
  //forward @ full speed
  //digitalWrite(12, HIGH); //Establishes forward direction of Channel A
  //digitalWrite(9, LOW);   //Disengage the Brake for Channel A
  //analogWrite(3, 255);   //Spins the motor on Channel A at full speed
  
  //delay(3000);
  
  //digitalWrite(9, HIGH); //Eengage the Brake for Channel A

  //delay(1000);
  
  //backward @ half speed
  //digitalWrite(12, LOW); //Establishes backward direction of Channel A
  //digitalWrite(9, LOW);   //Disengage the Brake for Channel A
  //analogWrite(3, 123);   //Spins the motor on Channel A at half speed
  
  //delay(3000);
  
  //digitalWrite(9, HIGH); //Eengage the Brake for Channel A
  
  //delay(1000);
  
}
