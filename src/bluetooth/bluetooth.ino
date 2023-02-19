/**
 * Code that test the bluetooth communications.
 *
 * @author WALL-O Dev Team.
 * @version 1.0.0
 * @since December 26th 2022
 */
#include <string.h>
#include <SoftwareSerial.h>

#define LED_PIN 13
#define BL_RXD 2
#define BL_TXD 3

bool running = false;

SoftwareSerial BluetoothSerial(BL_RXD, BL_TXD);

void setup() {
  digitalWrite(LED_PIN, LOW);

  Serial.begin(9600);
  while (!Serial.available()) {;}

  BluetoothSerial.begin(9600);
  while (!BluetoothSerial.available()) {;}
}

void loop()
{
  communicate();
  Serial.println("couccou");
  if (running) {
    digitalWrite(LED_PIN, HIGH);
  }
  else {
    digitalWrite(LED_PIN, LOW);
  }
}

void communicate() {
  String data = "";
  String commandResponse = "";
  
  if (BluetoothSerial.available()) {
    data = BluetoothSerial.readString();
    Serial.println(data);
  }

  if (data.equals("START")) {
    running = true;
    commandResponse = "OK";
  }
  else if (data.equals("STOP")) {
    running = false;
    commandResponse = "OK";
  }
  else if (data.equals("OK")) {
    commandResponse = "";
  }
  else {
    commandResponse = "UNKOWN COMMAND";
  }

  data = "{here are some data,commandResponse:" + commandResponse + "}";
  
  Serial.println(data);
  BluetoothSerial.print(data);
}