#include <Wire.h>               // I2C communication protocol for DAC
#include <Adafruit_MCP4725.h>   // library for communicating with the DAC
#include <IRremote.h>           // library for using the infrared LED as a remote control for the projector

Adafruit_MCP4725 dac;           // construct a dac object
IRsend irsend;                  // construct an infrared commication object

int IRPin = 3;
int solenoidPin = 9;
int lowCapPin = 5;              // open/close the synth circuit to a 100uF capacitor. when open it greatly lowers the oscillator frequency
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

// lists used by the IR emitter to send specific commands to the projector
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

  Serial.begin(9600);                       // enable the serial connection with python script
  dac.begin(0x60);                          // enable the DAC module
  dac.setVoltage(0, false);                 // intialise DAC output to 0
  digitalWrite(lowCapPin, HIGH);
  digitalWrite(motorPin, LOW);
  digitalWrite(bloopPin, LOW);
  digitalWrite(solenoidPin, LOW);
}

void loop() {
  // excecute commands based on received serial information from python script
  
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
