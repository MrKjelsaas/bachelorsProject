/*

  The script reads and prints the raw data from the sensors
  on an Arduino Nano 33 BLE, using the onboard IMU LSM9DS1
  Also makes the readings available as a BLE service

  https://www.arduino.cc/en/Reference/ArduinoLSM9DS1
  https://www.arduino.cc/en/Reference/ArduinoBLE

  Use UUID Generator if you have many devices
*/
#include <ArduinoBLE.h>
#include <Arduino_LSM9DS1.h>

BLEService orientationService("23ce3f92-be01-11e9-9cb5-2a2ae2dbcce4");
const char localName[] = "IMU sensor";


// create characteristics for raw data
// and allow remote device to read and get notifications about them:
BLEFloatCharacteristic AccCharacteristic("23ce450a-be01-11e9-9cb5-2a2ae2dbcce4", BLERead | BLENotify);
BLEFloatCharacteristic GyrochCharacteristic("23ce4276-be01-11e9-9cb5-2a2ae2dbcce4", BLERead | BLENotify);
BLEFloatCharacteristic MagCharacteristic("23ce43ca-be01-11e9-9cb5-2a2ae2dbcce4", BLERead | BLENotify);

// sensor's sample rate is fixed at 119 Hz (check the datasheet)
const float sensorRate = 119.00;

void setup() {
  Serial.begin(115200);
  // Initialize the IMU
  if (!IMU.begin()) {
    Serial.println("Cannot start the IMU");
    // Stops her if there is a problem
    while (true);
  }

  // begin BLE:
  if (BLE.begin()) {
    // set advertised local name and service UUID:
    BLE.setLocalName(localName);
    BLE.setAdvertisedService(orientationService);

    // add the characteristics to the service:
    orientationService.addCharacteristic(AccCharacteristic);
    orientationService.addCharacteristic(GyroCharacteristic);
    orientationService.addCharacteristic(MagCharacteristic);

    // add service and start advertising:
    BLE.addService(orientationService);
    BLE.advertise();
  } else {
    Serial.println("starting BLE failed.");
    // stop here if you can't access the BLE radio:
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
