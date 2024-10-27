
#include <AccelStepper.h>

AccelStepper stepperCamera(AccelStepper::FULL4WIRE, 2, 4, 3, 5);  // Stepper motor for camera rotation
AccelStepper stepperLeft(AccelStepper::FULL4WIRE, 6, 8, 7, 9);  // Stepper motor for left movement
AccelStepper stepperRight(AccelStepper::FULL4WIRE, 10, 12, 11, 13); // Stepper motor for right movement
AccelStepper stepperForward(AccelStepper::FULL4WIRE, 14, 16, 15, 17); // Stepper motor for forward movement

int ledPin = 18; // Pin for LED

void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);

  stepperCamera.setMaxSpeed(1000);
  stepperCamera.setAcceleration(500);

  stepperLeft.setMaxSpeed(1000);
  stepperLeft.setAcceleration(500);

  stepperRight.setMaxSpeed(1000);
  stepperRight.setAcceleration(500);

  stepperForward.setMaxSpeed(1000);
  stepperForward.setAcceleration(500);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    if (command.startsWith("X") && command.indexOf("Y") != -1 && command.indexOf("D") != -1) {
      int x = command.substring(1, command.indexOf("Y")).toInt();
      int y = command.substring(command.indexOf("Y") + 1, command.indexOf("D")).toInt();
      int distance = command.substring(command.indexOf("D") + 1).toInt();

      // Move camera to specific step position
      stepperCamera.moveTo(x);
      while (stepperCamera.isRunning()) {
        stepperCamera.run();
      }

      // Calculate movement logic based on x and distance values
      if (x < 300) {
        moveLeft();
      } else if (x > 340) {
        moveRight();
      } else {
        moveForward();
      }

      // Blink LED faster as it gets closer
      if (distance < 50) {
        blinkLed(100);
      } else {
        blinkLed(500);
      }
    }
  }
}

void moveLeft() {
  // Logic to move hexapod left
  stepperLeft.move(200); // Move stepper motor left by 200 steps
  while (stepperLeft.isRunning()) {
    stepperLeft.run();
  }
}

void moveRight() {
  // Logic to move hexapod right
  stepperRight.move(200); // Move stepper motor right by 200 steps
  while (stepperRight.isRunning()) {
    stepperRight.run();
  }
}

void moveForward() {
  // Logic to move hexapod forward
  stepperForward.move(200); // Move stepper motor forward by 200 steps
  while (stepperForward.isRunning()) {
    stepperForward.run();
  }
}

void blinkLed(int interval) {
  digitalWrite(ledPin, HIGH);
  delay(interval);
  digitalWrite(ledPin, LOW);
  delay(interval);
}
