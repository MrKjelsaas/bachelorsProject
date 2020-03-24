/*  
  Arduino LSM9DS1 - Simple Accelerometer  
  This example reads the acceleration values from the LSM9DS1 
  sensor and continuously prints them to the Serial Monitor 
  or Serial Plotter.  
  The circuit:  
  - Arduino Nano 33 BLE Sense 
  created 10 Jul 2019 
  by Riccardo Rizzo 
  This example code is in the public domain.  
*/  

#include <Arduino_LSM9DS1.h>  
#include <MadgwickAHRS.h> 

Madgwick filter;  
const float sensorRate = 104.00;  

void setup() {  
  Serial.begin(9600); 
  while (!Serial);  
  Serial.println("Started");  

  if (!IMU.begin()) { 
    Serial.println("Failed to initialize IMU!");  
    while (1);  
  } 

  filter.begin(sensorRate); 


} 


void loop() { 

  float xAcc, yAcc, zAcc; 
  float xGyro, yGyro, zGyro;  

  float roll, pitch, yaw; 
  // check if the IMU is ready to read: 
  if (IMU.accelerationAvailable() &&  
      IMU.gyroscopeAvailable()) { 
    // read accelerometer & gyrometer:  
    IMU.readAcceleration(xAcc, yAcc, zAcc); 
    IMU.readGyroscope(xGyro, yGyro, zGyro); 

    filter.updateIMU(xGyro, yGyro, zGyro, xAcc, yAcc, zAcc);  

    roll = filter.getRoll();  
    pitch = filter.getPitch();  
    yaw = filter.getYaw();  
    Serial.print(roll); 
    Serial.print(",");  
    Serial.print(pitch);  
    Serial.print(",");  
    Serial.println(yaw);  

  } 
}
