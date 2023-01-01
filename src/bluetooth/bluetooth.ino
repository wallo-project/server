/**
 * Code that test the bluetooth communications.
 * 
 * @author WALL-O Dev Team.
 * @version 1.0.0
 * @since December 26th 2022
 */

// include the necessary libraries
#include <SoftwareSerial.h>

// setup the pins
#define BLE_RXD 10
#define BLE_TXD 11

// setup the bluetooth communication
SoftwareSerial bluetooth(BLE_RXD, BLE_TXD);

/**
 * Setup function executed on the startup
 */
void setup() {
  // init the szerial
  Serial.begin(9600);

  // wait for the serial to be started
  while (!Serial) {;}

  // init the bluetooth
  bluetooth.begin(9600);
}

/**
 * Setup function executed on the startup
 */
void loop() { 
  if (bluetooth.available()) {
    Serial.write(bluetooth.read());
  }
  if (Serial.available()) {
    bluetooth.write(Serial.read());
    
  }
}