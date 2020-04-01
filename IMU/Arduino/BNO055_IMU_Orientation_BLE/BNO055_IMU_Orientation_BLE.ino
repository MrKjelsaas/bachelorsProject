#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include <ArduinoBLE.h>

/* Set the delay between fresh samples */
#define BNO055_SAMPLERATE_DELAY_MS (100)

// Check I2C device address and correct line below (by default address is 0x29 or 0x28)
//                                   id, address
Adafruit_BNO055 bno = Adafruit_BNO055(55, 0x28);


BLEService orientationService("23ce3f92-be01-11e9-9cb5-2a2ae2dbcce4");
const char localName[] = "BNO055-Sensor";

// create characteristics for heading, pitch, roll
// and allow remote device to read and get notifications about them:
BLEFloatCharacteristic rollCharacteristic("23ce450a-be01-11e9-9cb5-2a2ae2dbcce4", BLERead | BLENotify);
BLEFloatCharacteristic pitchCharacteristic("23ce4276-be01-11e9-9cb5-2a2ae2dbcce4", BLERead | BLENotify);
BLEFloatCharacteristic headingCharacteristic("23ce43ca-be01-11e9-9cb5-2a2ae2dbcce4", BLERead | BLENotify);


void setup(void)
{
  Serial.begin(115200);
  Serial.println("Orientation Sensor Test"); Serial.println("");

  /* Initialise the sensor */
  if (!bno.begin())
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while (1);
  }

  delay(1000);

  /* Use external crystal for better accuracy */
  bno.setExtCrystalUse(true);

  /* Display some basic information on this sensor
    displaySensorDetails();*/

    // begin BLE:
  if (BLE.begin()) {
    // set advertised local name and service UUID:
    BLE.setLocalName(localName);
    BLE.setAdvertisedService(orientationService);

    // add the characteristics to the service:
    orientationService.addCharacteristic(rollCharacteristic);
    orientationService.addCharacteristic(pitchCharacteristic);
    orientationService.addCharacteristic(headingCharacteristic);

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

/**************************************************************************/
/*
    Arduino loop function, called once 'setup' is complete (your own code
    should go here)
*/
/**************************************************************************/
void updateOrientation()
{
  /* Get a new sensor event */
  sensors_event_t event;
  bno.getEvent(&event);

  /* The processing sketch expects data as roll, pitch, yaw */
  Serial.print(event.orientation.z, 4);
  Serial.print(",");
  Serial.print(event.orientation.y, 4);
  Serial.print(",");
  Serial.print(event.orientation.x, 4);

  /*calibration data for each sensor. If the value is 0 = uncalibrated, if value is 3 = calibrated
  The calibration data will not be printed in the raspicode file. You have to first calibrate with arduino in serial*/
  uint8_t sys, gyro, accel, mag = 0;
  bno.getCalibration(&sys, &gyro, &accel, &mag);
  Serial.print(",");
  Serial.print(sys, DEC);
  Serial.print(",");
  Serial.print(gyro, DEC);
  Serial.print(",");
  Serial.print(accel, DEC);
  Serial.print(",");
  Serial.println(mag, DEC);
  
  delay(BNO055_SAMPLERATE_DELAY_MS);

  // update the BLE characteristics with the orientation values:
    rollCharacteristic.writeValue(event.orientation.z);
    pitchCharacteristic.writeValue(event.orientation.y);
    headingCharacteristic.writeValue(event.orientation.x);
}
