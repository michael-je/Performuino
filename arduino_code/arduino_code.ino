#include <Wire.h>
#include <Adafruit_MCP4725.h>
#include <IRremote.h>

Adafruit_MCP4725 dac;
IRsend irsend;

int LEDPin = 2;
int IRPin = 3;
int solenoidPin = 9;
int lowCapPin = 5;
int bloopPin = 6;
int lampPin = 7;
int motorPin = 10;
int eyesPin = 12;
int mouthPin = 13;
int photoResistorPin = A0;

int dac_value;
int pwm_value;
int command;
int motor_pwm_value;

unsigned int projector_power[68] = {9050,4500,550,550,600,550,550,600,550,550,550,600,550,600,550,550,550,600,550,1700,550,1700,550,1700,550,1750,550,1700,550,1700,550,1700,550,1700,550,1700,600,550,550,1700,550,600,550,550,600,550,550,1700,550,600,550,600,550,1700,550,550,550,1700,600,1700,550,1700,550,600,550,1700,550,};
unsigned int projector_pink[68] = {8950,4550,550,550,550,600,500,650,550,550,550,600,550,550,550,600,550,600,550,1700,550,1750,500,1700,550,1700,550,1750,550,1700,550,1700,550,1750,500,1750,500,600,550,600,550,1700,550,550,550,600,550,600,550,550,550,600,550,1750,500,1700,550,600,550,1750,500,1700,550,1750,500,1750,550,};
unsigned int projector_blue[68] = {9050,4500,550,600,550,550,550,600,550,550,550,600,550,600,550,550,550,600,550,1700,550,1750,500,1750,500,1750,500,1750,550,1700,550,1700,550,1750,500,1750,500,1750,550,550,550,600,550,550,550,600,550,1750,500,600,550,550,550,600,550,1750,500,1750,500,1750,550,1700,550,550,550,1750,550,};
unsigned int projector_white[68] = {9000,4500,550,600,550,600,550,550,550,600,550,550,550,600,550,600,550,550,550,1700,600,1700,550,1700,550,1700,550,1700,550,1700,550,1750,550,1700,550,1700,550,1700,550,1700,550,600,550,550,600,550,550,1700,550,600,550,550,600,550,550,600,550,1700,550,1700,550,1700,550,600,550,1700,550,};
unsigned int projector_red[68] = {9000,4500,550,600,550,600,550,550,550,600,550,550,600,550,550,600,550,550,550,1750,550,1700,550,1700,550,1700,550,1700,550,1750,550,1700,550,1700,550,550,600,550,550,1700,550,600,550,600,550,550,550,1700,550,600,550,1750,500,1700,550,600,550,1700,550,1700,550,1750,550,550,550,1700,550,};


void setup() {
  pinMode(LEDPin, OUTPUT);
  pinMode(solenoidPin, OUTPUT);
  pinMode(lowCapPin, OUTPUT);
  pinMode(lampPin, OUTPUT);
  pinMode(motorPin, OUTPUT);
  pinMode(bloopPin, OUTPUT);
  pinMode(photoResistorPin, INPUT);

  Serial.begin(9600);
  dac.begin(0x60);
  dac.setVoltage(0, false);
  digitalWrite(lowCapPin, HIGH);
  digitalWrite(motorPin, LOW);
  digitalWrite(bloopPin, LOW);
  digitalWrite(solenoidPin, LOW);
}

void loop() {
  if (Serial.available()) {
    Serial.print("peek: ");
    Serial.println(Serial.peek());
    switch (Serial.read()) {

      case '3':                             // dac voltage -> oscillator frequency
        dac_value = Serial.parseInt();      // reads the follwing intiger bytes, then stops at a '!'
        dac.setVoltage(dac_value, false);
        break;
        

      case '4':                             // lowCap_pwm
        pwm_value = Serial.parseInt();
        analogWrite(lowCapPin, pwm_value);
        break;
        
        
      case 'b':                            // bloop on
        digitalWrite(bloopPin, HIGH);
        break;
        
      case 'c':                            // bloop off
        digitalWrite(bloopPin, LOW);
        break;
        

      case '7':                           // motor_pwm
        motor_pwm_value = Serial.parseInt();
        analogWrite(motorPin, motor_pwm_value);
        break;


      case 's':                           // solenoid on
        digitalWrite(solenoidPin, HIGH);
        break;

      case 't':                           // solenoid off
        digitalWrite(solenoidPin, LOW);
        break;
        

      case 'p':                           // projector
        delay(1);
        command = Serial.read();
        if (command == '0'){
          irsend.sendRaw(projector_power, 68, 38);
        }
        else if (command == '1'){
          irsend.sendRaw(projector_pink, 68, 38);
        }
        else if (command == '2'){
          irsend.sendRaw(projector_blue, 68, 38);
        }
        else if (command == '3'){
          irsend.sendRaw(projector_white, 68, 38);
        }
        else if (command == '4'){
          irsend.sendRaw(projector_red, 68, 38);
        }
        break;

      case 'q':                           // senses whether projector is on/off -> turns it off if it's on
        if (analogRead(photoResistorPin) >= 800){
          irsend.sendRaw(projector_power, 68, 38);
        }
        break;

      case 'l':                           // lamp on
        digitalWrite(lampPin, HIGH);
        break;

      case 'o':                           // lamp off
        digitalWrite(lampPin, LOW);
        break;
        

      case 'e':                           // eyes on
        digitalWrite(eyesPin, HIGH);
        break;

      case 'f':                           // eyes off
        digitalWrite(eyesPin, LOW);
        break;
        

      case 'm':                           // mouth on
        digitalWrite(mouthPin, HIGH);
        break;

      case 'n':                           // mouth off
        digitalWrite(mouthPin, LOW);
        break;
        
        
      default:
        break;
    }
  }
}
