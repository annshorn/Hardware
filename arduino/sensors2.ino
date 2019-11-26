#include <Wire.h>
const int MPU2 = 0x69, MPU1=0x68;

int16_t AcX,AcY,AcZ;
//float gForceX, gForceY, gForceZ, gyroX, gyroY, gyroZ,rotX, rotY, rotZ;
//float gForceX2, gForceY2, gForceZ2;

void setup(){
  Wire.begin();
  Wire.beginTransmission(MPU1);
  Wire.write(0x6B);
  Wire.write(0b00000000);
  Wire.endTransmission();  
  Wire.beginTransmission(MPU1);
  Wire.write(0x1B);
  Wire.write(0x00000000);
  Wire.endTransmission(); 
  Wire.beginTransmission(MPU1);
  Wire.write(0x1C);
  Wire.write(0b00000000);
  Wire.endTransmission(); 
  
  Wire.begin();
  Wire.beginTransmission(MPU2);
  Wire.write(0x6B);
  Wire.write(0b00000000); 
  Wire.endTransmission();  
  Wire.beginTransmission(MPU2); 
  Wire.write(0x1B);
  Wire.write(0x00000000);
  Wire.endTransmission(); 
  Wire.beginTransmission(MPU2);
  Wire.write(0x1C);
  Wire.write(0b00000000);
  Wire.endTransmission(); 
  Serial.begin(38400);
  
}

void loop(){
  GetMpuValue(MPU1);
//  Serial.print("Acc 1 \n");

  GetMpuValue(MPU2);
//  Serial.print("Acc 2 \n");
}

void GetMpuValue(const int MPU){
  Wire.beginTransmission(MPU);
  Wire.write(0x3B);  
  Wire.endTransmission(false);
  Wire.requestFrom(MPU,12,true);  
  AcX=Wire.read()<<8|Wire.read();    
  AcY=Wire.read()<<8|Wire.read();  
  AcZ=Wire.read()<<8|Wire.read();  
//  GyX=Wire.read()<<8|Wire.read();  
//  GyY=Wire.read()<<8|Wire.read();  
//  GyZ=Wire.read()<<8|Wire.read();  
  
//  Serial.print("Accelerometer: ");
  Serial.print(MPU);Serial.print(" : ");
  Serial.print(AcX);Serial.print(",");Serial.print(AcY);Serial.print(",");Serial.println(AcZ); 
//  Serial.print("X = "); Serial.print(AcX);
//  Serial.print(" | Y = "); Serial.print(AcY);
//  Serial.print(" | Z = "); Serial.println(AcZ); 
  
//  Serial.print("Gyroscope: ");
//  Serial.print("X = "); Serial.print(GyX);
//  Serial.print(" | Y = "); Serial.print(GyY);
//  Serial.print(" | Z = "); Serial.println(GyZ);
//  Serial.println(" ");
  delay(0.001);
  
}
