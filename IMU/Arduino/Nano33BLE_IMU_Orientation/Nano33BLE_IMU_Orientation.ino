/*
  The script uses Madgwick orientation calculation to calculate the yaw, pitch, and roll
  on an Arduino Nano 33 BLE, using the onboard IMU LSM9DS1
  https://www.arduino.cc/en/Reference/ArduinoLSM9DS1
  https://github.com/arduino-libraries/MadgwickAHRS
*/

#include <Arduino_LSM9DS1.h>
#include <MadgwickAHRS.h>

// initialize a Madgwick filter:
Madgwick filter;

// sensor's sample rate is fixed at 119 Hz (check the datasheet)
const float sensorRate = 119.00;

// values for orientation
float roll = 0.0;
float pitch = 0.0;
float yaw = 0.0;

void setup() {
  Serial.begin(9600);
  // Initialize the IMU
  if (!IMU.begin()) {
    Serial.println("Cannot start the IMU");
    // Stops her if there is a problem
    while (true);
  }

  // start the Madgwick filter to run at the sample rate:
  filter.begin(sensorRate);

}

void loop() {

  // The values from the gyroscope and accelerometer
  float xgyro, ygyro, zgyro, xacc, yacc, zacc;

  // Query if new acceleration and gyroscope data is available
  if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable()) {

    // Query the gyroscope and the accelerometer and returns the values
    IMU.readGyroscope(xgyro, ygyro, zgyro);
    IMU.readAcceleration(xacc, yacc, zacc);

    // update the filter, which computes orientation:
    filter.updateIMU(xgyro, ygyro, zgyro, xacc, yacc, zacc);

    // update the yaw, pitch and roll:
    roll = filter.getRoll();
    pitch = filter.getPitch();
    yaw = filter.getYaw();

    // Prints the yaw, pitch and roll data
    Serial.println("roll    pitch   yaw");
    Serial.print(roll);
    Serial.print("\t");
    Serial.print(pitch);
    Serial.print("\t");
    Serial.println(yaw);

  }
}
