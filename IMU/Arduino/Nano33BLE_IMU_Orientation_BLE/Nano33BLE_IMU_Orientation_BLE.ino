/*
  The script uses Madgwick orientation calculation to calculate heading, pitch, and roll
  on an Arduino Nano 33 BLE, using the onboard IMU LSM9DS1
  Also makes the readings available as a BLE service
  https://www.arduino.cc/en/Reference/ArduinoLSM9DS1
  https://github.com/arduino-libraries/MadgwickAHRS7
  https://www.arduino.cc/en/Reference/ArduinoBLE

  Use UUID Generator if you have many devices

*/
#include <Arduino_LSM9DS1.h>
#include <MadgwickAHRS.h>
#include <ArduinoBLE.h>

BLEService orientationService("23ce3f92-be01-11e9-9cb5-2a2ae2dbcce4");
const char localName[] = "IMU Sensor";

// create characteristics for heading, pitch, roll
// and allow remote device to read and get notifications about them:
BLEFloatCharacteristic headingCharacteristic("23ce450a-be01-11e9-9cb5-2a2ae2dbcce4", BLERead | BLENotify);
BLEFloatCharacteristic pitchCharacteristic("23ce4276-be01-11e9-9cb5-2a2ae2dbcce4", BLERead | BLENotify);
BLEFloatCharacteristic rollCharacteristic("23ce43ca-be01-11e9-9cb5-2a2ae2dbcce4", BLERead | BLENotify);

// initialize a Madgwick filter:
Madgwick filter;

// sensor's sample rate is fixed at 119 Hz (check the datasheet)
const float sensorRate = 119.00;

// values for orientation:
float roll = 0.0;
float pitch = 0.0;
float heading = 0.0;

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

  // begin BLE:
  if (BLE.begin()) {
    // set advertised local name and service UUID:
    BLE.setLocalName(localName);
    BLE.setAdvertisedService(orientationService);

    // add the characteristics to the service:
    orientationService.addCharacteristic(headingCharacteristic);
    orientationService.addCharacteristic(pitchCharacteristic);
    orientationService.addCharacteristic(rollCharacteristic);

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
  // listen for BLE peripherals to connect:
  BLEDevice central = BLE.central();

  // if a central is connected to this peripheral:
  if (central) {
    Serial.print("Connected to central: ");
    // print the central's MAC address:
    Serial.println(central.address());

    // while the central is still connected to peripheral:
    while (central.connected()) {
      updateOrientation();
    }

    // when the central disconnects, print it out:
    Serial.print("Disconnected from central: ");
    Serial.println(central.address());
  }
}

void updateOrientation() {

  // The values from the rotation and accelerometer
  float xgyro, ygyro, zgyro, xacc, yacc, zacc;

  // Query if new acceleration and gyroscope data is available
  if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable()) {

    // Query the gyroscope and the accelerometer and returns the values
    IMU.readGyroscope(xgyro, ygyro, zgyro);
    IMU.readAcceleration(xacc, yacc, zacc);

    // update the filter, which computes orientation:
    filter.updateIMU(xgyro, ygyro, zgyro, xacc, yacc, zacc);

    // update the heading, pitch and roll:
    roll = filter.getRoll();
    pitch = filter.getPitch();
    heading = filter.getYaw();

    // Prints the heading, pitch and roll data
    Serial.print("Orientation: ");
    Serial.print(heading);
    Serial.print(" ");
    Serial.print(pitch);
    Serial.print(" ");
    Serial.println(roll);

    // update the BLE characteristics with the orientation values:
    headingCharacteristic.writeValue(heading);
    pitchCharacteristic.writeValue(pitch);
    rollCharacteristic.writeValue(roll);
  }
}
