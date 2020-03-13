/*

  The script reads and prints the raw data from the sensors in serial
  see https://www.arduino.cc/en/Reference/ArduinoLSM9DS1 for more info
*/

#include <Arduino_LSM9DS1.h>

void setup() {
  Serial.begin(115200);
  // Initialize the IMU
  if (!IMU.begin()) {
    Serial.println("Cannot start the IMU");
    // Stops her if there is a problem
    while (true);
  }
}

void loop() {

  // The values from the rotation, accelerometer and the magnetic field
  float xgyro, ygyro, zgyro, xacc, yacc, zacc, xmag, ymag, zmag;

  // Query if new acceleration, gyroscope and magneticfield data is available
  if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable() && IMU.magneticFieldAvailable()) {

    // Query the gyroscope, accelerometer and magneticfield and returns the values
    IMU.readGyroscope(xgyro, ygyro, zgyro);
    IMU.readAcceleration(xacc, yacc, zacc);
    IMU.readMagneticField(xmag, ymag, zmag);

    // Prints the raw data for x, y and z-axises from the gyroscope in degrees per second
    Serial.print("Gyro in d/s: ");  Serial.print(xgyro);  Serial.print(" ");  Serial.print(ygyro); Serial.print(" ");  Serial.println(zgyro);

    // Prints the raw data for x, y and z-axises from the accelerometer in g's (9,81m/s^2)
    Serial.print("Acce in g's: ");  Serial.print(xacc);  Serial.print(" ");  Serial.print(yacc); Serial.print(" ");  Serial.println(zacc);

    // Prints the raw data for x, y and z-axises from the magnetometer in microtesla
    Serial.print("Magn in uT:  ");  Serial.print(xmag);  Serial.print(" ");  Serial.print(ymag); Serial.print(" ");  Serial.println(zmag);
    Serial.println("\n");
  }
}
