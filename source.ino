#include <NewPing.h>
#include <Servo.h>

#define MAX_DISTANCE 200
#define INTERVAL_BUZZ_ON 50
#define INTERVAL_BUZZ_OFF_1 1000
#define INTERVAL_BUZZ_OFF_2 500
#define INTERVAL_BUZZ_OFF_3 250
#define INTERVAL_BUZZ_OFF_4 100
#define INTERVAL_RADAR 200
#define INTERVAL_SERVO 15

#define PIN_SERVO 12
#define PIN_ECHO 11
#define PIN_TRIGGER 10
#define PIN_BUZZER 32


Servo servo;											// servo variable, using Servo.h library
int angle = 0;											// servomotor angle
int buzzerState = LOW;									// next buzzer state
int servoRotation = 0; 									// next servo rotation (0 for 0->180, 1 for 180->0) 
unsigned long previousMillisBuzzer = 0;					// timer for buzzer
unsigned long previousMillisRadar = 0;					// timer for ultrasonic sensor
unsigned long previousMillisServo = 0;					// timer for servo
unsigned int distance = 0;								// measured distance in cm
float dist1 = MAX_DISTANCE / 3;           				// distance markers for buzzer
float dist2 = 2 * MAX_DISTANCE / 3;
float dist3 = MAX_DISTANCE / 6;

NewPing sonar(PIN_TRIGGER, PIN_ECHO, MAX_DISTANCE);		// sonar variable, using NewPing.h library

void setup ()
{
  pinMode(PIN_BUZZER, OUTPUT);							// initialize PIN_BUZZER as output
  Serial.begin (9600);									// begin serial communication
  servo.attach(PIN_SERVO);								// initialize PIN_SERVO
  servo.write(angle);									// move to initial angle
}

void loop ()
{
  unsigned long currentMillisBuzzer = millis();
  unsigned long currentMillisRadar = millis();
  unsigned long currentMillisServo = millis();
  
  if(currentMillisRadar - previousMillisRadar >= INTERVAL_RADAR) {				// "equivalent" to delay(INTERVAL_RADAR)
      previousMillisRadar = currentMillisRadar;
      distance = sonar.ping_cm();												// measure distance
    }

  if(currentMillisServo - previousMillisServo >= INTERVAL_SERVO) {				// "equivalent" to delay(INTERVAL_SERVO)
    previousMillisServo = currentMillisServo;
    
    Serial.print(angle);                              							// print current servo angle to serial port
    Serial.print(",");
    Serial.print(distance);                           							// print current distance of nearest object to serial port
    Serial.println();
    
    if(servoRotation == 0) {    // 0 -> 180
      servo.write(angle);														// rotate servo
      angle += 1;																// increase angle
      if(angle == 180)															// if at 180 degrees, begin rotating to 0 degrees
        servoRotation = 1;
    } else {                    // 180 -> 0									
      servo.write(angle);														// rotate servo
      angle -= 1;																// decrease angle
      if(angle == 0)															// if at 0 degrees, begin rotating to 180 degrees
        servoRotation = 0;  
    }
  }


 if(distance > dist1 && distance <= MAX_DISTANCE) {						// if distance to nearest object is in interval (2/3*MAX_DISTANCE, MAX_DISTANCE]
    if (buzzerState == HIGH) {
      if(currentMillisBuzzer - previousMillisBuzzer >= INTERVAL_BUZZ_ON) {		// "equivalent" to delay(INTERVAL_BUZZ_ON)
        previousMillisBuzzer = currentMillisBuzzer;
        buzzerState = LOW;														// next buzzer state -> off
        digitalWrite(PIN_BUZZER, buzzerState);									// turn off buzzer
      }
    } else {
      if(currentMillisBuzzer - previousMillisBuzzer >= INTERVAL_BUZZ_OFF_1) {	// "equivalent" to delay(INTERVAL_BUZZ_OFF_1)
        previousMillisBuzzer = currentMillisBuzzer;
        buzzerState = HIGH;														// next buzzer state -> on
        digitalWrite(PIN_BUZZER, buzzerState);									// turn on buzzer
      }
    }
  } else if(distance > dist2 && distance <= dist1) {						// if distance to nearest object is in interval (1/3*MAX_DISTANCE, 2/3*MAX_DISTANCE]
    if (buzzerState == HIGH) {
      if(currentMillisBuzzer - previousMillisBuzzer >= INTERVAL_BUZZ_ON) {		// "equivalent" to delay(INTERVAL_BUZZ_ON)
        previousMillisBuzzer = currentMillisBuzzer;
        buzzerState = LOW;														// next buzzer state -> off
        digitalWrite(PIN_BUZZER, buzzerState);									// turn off buzzer
      }
    } else {
      if(currentMillisBuzzer - previousMillisBuzzer >= INTERVAL_BUZZ_OFF_2) {	// "equivalent" to delay(INTERVAL_BUZZ_OFF_2)
        previousMillisBuzzer = currentMillisBuzzer;
        buzzerState = HIGH;														// next buzzer state -> on
        digitalWrite(PIN_BUZZER, buzzerState);									// turn on buzzer
      }
    }
  } else if(distance > dist3 && distance <= dist2) {						// if distance to nearest object is in interval (1/6*MAX_DISTANCE, 1/3*MAX_DISTANCE]
    if (buzzerState == HIGH) {
      if(currentMillisBuzzer - previousMillisBuzzer >= INTERVAL_BUZZ_ON) {		// "equivalent" to delay(INTERVAL_BUZZ_ON)
        previousMillisBuzzer = currentMillisBuzzer;
        buzzerState = LOW;														// next buzzer state -> off
        digitalWrite(PIN_BUZZER, buzzerState);									// turn off buzzer
      }
    } else {
      if(currentMillisBuzzer - previousMillisBuzzer >= INTERVAL_BUZZ_OFF_3) {	// "equivalent" to delay(INTERVAL_BUZZ_OFF_3)
        previousMillisBuzzer = currentMillisBuzzer;
        buzzerState = HIGH;														// next buzzer state -> on
        digitalWrite(PIN_BUZZER, buzzerState);									// turn on buzzer
      }
    }
  } else if(distance > 0 && distance <= dist3) {						// if distance to nearest object is in interval (0, 1/6*MAX_DISTANCE]
    if (buzzerState == HIGH) {
      if(currentMillisBuzzer - previousMillisBuzzer >= INTERVAL_BUZZ_ON) {		// "equivalent" to delay(INTERVAL_BUZZ_ON)
        previousMillisBuzzer = currentMillisBuzzer;
        buzzerState = LOW;														// next buzzer state -> off
        digitalWrite(PIN_BUZZER, buzzerState);									// turn off buzzer
      }
    } else {
      if(currentMillisBuzzer - previousMillisBuzzer >= INTERVAL_BUZZ_OFF_4) {	// "equivalent" to delay(INTERVAL_BUZZ_OFF_4)
        previousMillisBuzzer = currentMillisBuzzer;
        buzzerState = HIGH;														// next buzzer state -> on
        digitalWrite(PIN_BUZZER, buzzerState);									// turn on buzzer
      }
    }
  } 
}
