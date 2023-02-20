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
#define BL_RXD 10
#define BL_TXD 11

bool running = false;

SoftwareSerial BluetoothSerial(BL_RXD, BL_TXD);

void setup() {
  pinMode(LED_PIN, OUTPUT);

  digitalWrite(LED_PIN, LOW);

  Serial.begin(9600);

  BluetoothSerial.begin(9600);
}

void loop()
{
  communicate(5, 0);
  if (running) {
    digitalWrite(LED_PIN, HIGH);
  }
  else {
    digitalWrite(LED_PIN, LOW);
  }
}

void communicate(int speed, int angle) {
  String data = "";
  String commandResponse = "";
  
  if (BluetoothSerial.available()) {
    data = BluetoothSerial.readString();
  }

  if (data.startsWith("START")) {
    running = true;
    commandResponse = "START_OK";
  }
  else if (data.startsWith("STOP")) {
    running = false;
    commandResponse = "STOP_OK";
  }
  else if (data.startsWith("OK")) {
    commandResponse = "";
  }
  else if (data.startsWith("TEST_CONNECTION")) {
    commandResponse = "CONNECTION_ESTABLISHED";
  }
  else if (!data.equals("")) {
    commandResponse = "UNKOWN_COMMAND";
  }

  if (!data.equals("")) {
    data = "\"running\":" + String(running) + ",\"speed\":" + String(speed); 
    if (!commandResponse.equals("")) {
      data += ",\"commandResponse\":\"" + commandResponse + "\"";
    }
    data = "{" + data + "}";
    BluetoothSerial.println(data);
  }
}