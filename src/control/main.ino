#include <Arduino.h>

// Pin Configurations
const int PIN_LASER_TRIGGER = 12;
const int PIN_GALVO_SYNC    = 11;
const int PIN_O2_SENSOR     = A0;
const int PIN_GAS_VALVE     = 8;

// Safety Thresholds
const float MAX_O2_PERCENTAGE = 0.1; // Maximum 0.1% Oxygen allowed for metal sintering
const int REFRESH_RATE_MS     = 100;

// System States
enum PrinterState { PURGING, READY, PRINTING, ERROR_HALT };
PrinterState currentState = PURGING;

float readOxygenLevel() {
    int rawAnalog = analogRead(PIN_O2_SENSOR);
    // Calibration: 0-1023 analog maps to 0.0% - 25.0% O2 concentration
    return (rawAnalog / 1023.0) * 25.0;
}

void setup() {
    Serial.begin(115200);
    pinMode(PIN_LASER_TRIGGER, OUTPUT);
    pinMode(PIN_GALVO_SYNC, INPUT);
    pinMode(PIN_GAS_VALVE, OUTPUT);
    
    digitalWrite(PIN_LASER_TRIGGER, LOW);
    digitalWrite(PIN_GAS_VALVE, HIGH); // Open Argon gas valve to purge chamber
}

void loop() {
    float currentO2 = readOxygenLevel();
    
    switch(currentState) {
        case PURGING:
            if (currentO2 <= MAX_O2_PERCENTAGE) {
                currentState = READY;
                Serial.println("[STATE] Chamber inert. System ready.");
            }
            break;
            
        case READY:
            if (digitalRead(PIN_GALVO_SYNC) == HIGH) {
                currentState = PRINTING;
                digitalWrite(PIN_LASER_TRIGGER, HIGH);
                Serial.println("[STATE] Sintering layer active.");
            }
            if (currentO2 > MAX_O2_PERCENTAGE) {
                currentState = ERROR_HALT;
            }
            break;
            
        case PRINTING:
            if (currentO2 > MAX_O2_PERCENTAGE) {
                currentState = ERROR_HALT;
                digitalWrite(PIN_LASER_TRIGGER, LOW);
                Serial.println("[CRITICAL] O2 spike detected! Laser killed.");
            }
            if (digitalRead(PIN_GALVO_SYNC) == LOW) {
                currentState = READY;
                digitalWrite(PIN_LASER_TRIGGER, LOW);
            }
            break;
            
        case ERROR_HALT:
            digitalWrite(PIN_LASER_TRIGGER, LOW);
            digitalWrite(PIN_GAS_VALVE, HIGH); // Flood chamber with shielding gas
            Serial.println("[ALERT] System E-Stop active. Purging chamber.");
            delay(1000);
            break;
    }
    delay(REFRESH_RATE_MS);
}

