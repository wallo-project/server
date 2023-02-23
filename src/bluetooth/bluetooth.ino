/**
 * Code that test the bluetooth communications.
 *
 * @author WALL-O Dev Team.
 * @version 1.0.0
 * @since December 26th 2022
 */
#include <SoftwareSerial.h>

#define LED_PIN 13
#define BL_RXD 10
#define BL_TXD 11

bool running = false;

bool detect = true;

long duration, distance, distanceDepart, distanceGauche, distanceDroite, distanceAvant;

SoftwareSerial BluetoothSerial(BL_RXD, BL_TXD);

void setup() {
  pinMode(LED_PIN, OUTPUT);

  digitalWrite(LED_PIN, LOW);

  Serial.begin(9600);

  BluetoothSerial.begin(9600);
}
void loop() {
  communicate();
  if (running) {
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
  }
  delay(100);
}

void communicate() {
  int state;
  bool commandReply = false;
  state = BluetoothSerial.read();

  if (state == '1') {
    running = true;
    commandReply = true;
    state = 0;

  } else if (state == '2') {
    running = false;
    commandReply = true;
    state = 0;
  } else if (state == '3') {
    commandReply = true;
    state = 0;
  } else {
    state = 0;
  }
  BluetoothSerial.println(String(running)+";"+String(distance)+";"+String(distanceDepart)+";"+String(distanceGauche)+";"+String(distanceDroite)+";"+String(distanceAvant)+";"+String(detect)+";"+String(commandReply));
}