/*
 * Custom Joystick Mouse Controller
 * Authors: Nitish Matta & Jash Chirag Monani
 * LNMIIT - 24UEC217 & 24UEC206
 *
 * Hardware Connections:
 *   Joystick GND  -> Arduino GND
 *   Joystick +5V  -> Arduino 5V
 *   Joystick VRx  -> Arduino A0
 *   Joystick VRy  -> Arduino A1
 *   Joystick SW   -> Arduino D8
 */

// --- Pin Definitions ---
const int PIN_JOYSTICK_X   = A0;
const int PIN_JOYSTICK_Y   = A1;
const int PIN_BUTTON       = 8;

// --- Tuning Parameters ---
const int   JOYSTICK_CENTER  = 512;   // Ideal center value of ADC (0–1023)
const int   DEADZONE         = 20;    // Ignore movements within this radius of center
const float MAX_SPEED        = 20.0;  // Maximum pixels to move per update cycle

void setup() {
  Serial.begin(9600);
  pinMode(PIN_BUTTON, INPUT_PULLUP);  // Internal pull-up; button press = LOW
}

void loop() {
  // --- 1. Read raw joystick values (0 to 1023) ---
  int rawX = analogRead(PIN_JOYSTICK_X);
  int rawY = analogRead(PIN_JOYSTICK_Y);

  // --- 2. Center the values around zero (-512 to +511) ---
  int centeredX = rawX - JOYSTICK_CENTER;
  int centeredY = rawY - JOYSTICK_CENTER;

  // --- 3. Apply deadzone ---
  int deltaX = 0;
  int deltaY = 0;

  if (abs(centeredX) > DEADZONE) {
    // Normalize to range -1.0 to +1.0 after removing deadzone
    float normalizedX = (float)(centeredX - (centeredX > 0 ? DEADZONE : -DEADZONE))
                        / (JOYSTICK_CENTER - DEADZONE);

    // Apply squared curve for acceleration (preserving sign)
    // Small deflections -> fine control | Large deflections -> fast movement
    deltaX = (int)(normalizedX * abs(normalizedX) * MAX_SPEED);
  }

  if (abs(centeredY) > DEADZONE) {
    float normalizedY = (float)(centeredY - (centeredY > 0 ? DEADZONE : -DEADZONE))
                        / (JOYSTICK_CENTER - DEADZONE);

    // Y-axis is typically inverted on screen (joystick up = cursor up)
    deltaY = (int)(normalizedY * abs(normalizedY) * MAX_SPEED);
  }

  // --- 4. Read button state ---
  // INPUT_PULLUP means LOW = pressed
  char clickStatus = (digitalRead(PIN_BUTTON) == LOW) ? 'c' : 'z';

  // --- 5. Send formatted string over serial ---
  // Protocol: "<click_status> <deltaX> <deltaY> m"
  // Example:  "z 5 -3 m"  (no click, move right 5, up 3)
  //           "c 0 0 m"   (click, no movement)
  Serial.print(clickStatus);
  Serial.print(" ");
  Serial.print(deltaX);
  Serial.print(" ");
  Serial.print(deltaY);
  Serial.println(" m");

  delay(5);  // ~200 Hz update rate
}
