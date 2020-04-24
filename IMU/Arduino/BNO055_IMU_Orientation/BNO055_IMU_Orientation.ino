#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

/* This driver uses the Adafruit unified sensor library (Adafruit_Sensor),
   which provides a common 'type' for sensor data and some helper functions.

   To use this driver you will also need to download the Adafruit_Sensor
   library and include it in your libraries folder.

   You should also assign a unique ID to this sensor for use with
   the Adafruit Sensor API so that you can identify this particular
   sensor in any data logs, etc.  To assign a unique ID, simply
   provide an appropriate value in the constructor below (12345
   is used by default in this example).

   Connections
   ===========
   Connect SCL to analog 5
   Connect SDA to analog 4
   Connect VDD to 3.3-5V DC
   Connect GROUND to common ground

   History
   =======
   2015/MAR/03  - First release (KTOWN)
*/

/* Set the delay between fresh samples */
<<<<<<< HEAD
#define BNO055_SAMPLERATE_DELAY_MS (50)
=======
#define BNO055_SAMPLERATE_DELAY_MS (100)
>>>>>>> 953334121235bc9002bcbbe5520cb7887962465f

// Check I2C device address and correct line below (by default address is 0x29 or 0x28)
//                                   id, address
Adafruit_BNO055 bno = Adafruit_BNO055(55, 0x28);

/**************************************************************************/
/*
    Displays some basic information on this sensor from the unified
    sensor API sensor_t type (see Adafruit_Sensor for more information)
*/
/**************************************************************************/
<<<<<<< HEAD
void displaySensorDetails(void)
{
=======
/*
  void displaySensorDetails(void)
  {
>>>>>>> 953334121235bc9002bcbbe5520cb7887962465f
  sensor_t sensor;
  bno.getSensor(&sensor);
  Serial.println("------------------------------------");
  Serial.print  ("Sensor:       "); Serial.println(sensor.name);
  Serial.print  ("Driver Ver:   "); Serial.println(sensor.version);
  Serial.print  ("Unique ID:    "); Serial.println(sensor.sensor_id);
  Serial.print  ("Max Value:    "); Serial.print(sensor.max_value); Serial.println(" xxx");
  Serial.print  ("Min Value:    "); Serial.print(sensor.min_value); Serial.println(" xxx");
  Serial.print  ("Resolution:   "); Serial.print(sensor.resolution); Serial.println(" xxx");
  Serial.println("------------------------------------");
  Serial.println("");
  delay(500);
<<<<<<< HEAD
}

/**************************************************************************/
=======
  }
  /*
  /**************************************************************************/
>>>>>>> 953334121235bc9002bcbbe5520cb7887962465f
/*
    Arduino setup function (automatically called at startup)
*/
/**************************************************************************/
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

<<<<<<< HEAD
  /* Display some basic information on this sensor */
  displaySensorDetails();
=======
  /* Display some basic information on this sensor
    displaySensorDetails();*/
>>>>>>> 953334121235bc9002bcbbe5520cb7887962465f
}

/**************************************************************************/
/*
    Arduino loop function, called once 'setup' is complete (your own code
    should go here)
*/
/**************************************************************************/
void loop(void)
{
  /* Get a new sensor event */
  sensors_event_t event;
  bno.getEvent(&event);

<<<<<<< HEAD
  /* Board layout:
         +----------+
         |         *| RST   PITCH  ROLL  YAW
     ADR |*        *| SCL
     INT |*        *| SDA     ^            /->
     PS1 |*        *| GND     |            |
     PS0 |*        *| 3VO     Y    Z-->    \-X
         |         *| VIN
         +----------+
  */

  /* calibration data for each sensor. */
  uint8_t sys, gyro, accel, mag = 0;
  bno.getCalibration(&sys, &gyro, &accel, &mag);
=======
  /* The processing sketch expects data as roll, pitch, yaw */
  Serial.print(event.orientation.y, 4);
  Serial.print(",");
  Serial.print(event.orientation.z, 4);
  Serial.print(",");
  Serial.print(event.orientation.x, 4);

  /*calibration data for each sensor. If the value is 0 = uncalibrated, if value is 3 = calibrated
  The calibration data will not be printed in the raspicode file. You have to first calibrate with arduino in serial*/
  uint8_t sys, gyro, accel, mag = 0;
  bno.getCalibration(&sys, &gyro, &accel, &mag);
  Serial.print(",");
>>>>>>> 953334121235bc9002bcbbe5520cb7887962465f
  Serial.print(sys, DEC);
  Serial.print(",");
  Serial.print(gyro, DEC);
  Serial.print(",");
  Serial.print(accel, DEC);
  Serial.print(",");
<<<<<<< HEAD
  Serial.print(mag, DEC);
  Serial.print(",");
  
  /* The processing sketch expects data as roll, pitch, heading */
  Serial.print(event.orientation.x, 4);
  Serial.print(",");
  Serial.print(event.orientation.y, 4);
  Serial.print(",");
  Serial.println(event.orientation.z, 4);

=======
  Serial.println(mag, DEC);
>>>>>>> 953334121235bc9002bcbbe5520cb7887962465f
  delay(BNO055_SAMPLERATE_DELAY_MS);
}
