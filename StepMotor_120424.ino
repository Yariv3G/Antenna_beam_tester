#include <Stepper.h>

// Define the number of steps per revolution
const int stepsPerRevolution = 602; // 360 degrees = 604 steps

// Give the motor control pins names
#define pwmA 3
#define pwmB 11
#define brakeA 9
#define brakeB 8
#define dirA 12
#define dirB 13
#define pulseTTLPin 4 // Output pin for Pulse TTL

// Initialize the stepper library on the motor shield
Stepper myStepper(stepsPerRevolution, dirA, dirB);

// Add these global variables
bool echoOn = false; // Default echo setting
int stepDelay = 100; // Default step delay in milliseconds

void setup() {
  // Set the PWM, brake, and Pulse TTL pins
  pinMode(pwmA, OUTPUT);
  pinMode(pwmB, OUTPUT);
  pinMode(brakeA, OUTPUT);
  pinMode(brakeB, OUTPUT);
  pinMode(pulseTTLPin, OUTPUT);
  digitalWrite(pwmA, HIGH);
  digitalWrite(pwmB, HIGH);
  digitalWrite(brakeA, LOW);
  digitalWrite(brakeB, LOW);

  // Set the motor speed (RPMs)
  myStepper.setSpeed(30);

  // Initialize the serial communication
  Serial.begin(9600);
  Serial.println("Stepper Control");
  Serial.println("Implemented Commands:");
  Serial.println("Command: Parameter: Effect: Example:");
  Serial.println("--------|------------|--------------------------------|------------------");
  Serial.println(" l number d Turn left for d degrees l90 ");
  Serial.println(" r number d Turn right for d degrees r90 ");
  Serial.println(" p 1 / 0 Apply / release power to coils p1 (default)");
  Serial.println(" d number n Sets the step delay to n ms d100 (=default)");
  Serial.println(" e1 / 0 Sets the echo on / off e0 (=default)");
  Serial.println(" h - Display this help information h");
  Serial.println(" v - Display the firmware version v");
  Serial.println(" c - Clear screen on VT100 c");
  Serial.println("eee");
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    switch (command) {
      case 'l':
        handleLeftCommand();
        break;
      case 'r':
        handleRightCommand();
        break;
      case 'p':
        handlePowerCommand();
        break;
      case 'd':
        handleDelayCommand();
        break;
      case 'e':
        handleEchoCommand();
        break;
      case 'h':
        printHelp();
        break;
      case 'v':
        printVersion();
        break;
      case 'c':
        clearScreen();
        break;
      default:
        break;
    }
  }
}

void handleLeftCommand() {
  int degrees = Serial.parseInt();
  int steps = map(degrees, 0, 360, 0, stepsPerRevolution);
  for (int i = 0; i < steps; i++) {
    myStepper.step(-1);
    digitalWrite(pulseTTLPin, HIGH);
    delayMicroseconds(100); // Adjust the pulse width as needed
    digitalWrite(pulseTTLPin, LOW);
  }
    
    Serial.print("Turned left for ");
    Serial.print(degrees);
    Serial.println(" degrees.");
  
 
}

void handleRightCommand() {
  int degrees = Serial.parseInt();
  int steps = map(degrees, 0, 360, 0, stepsPerRevolution);
  for (int i = 0; i < steps; i++) {
    myStepper.step(1);
    digitalWrite(pulseTTLPin, HIGH);
    delayMicroseconds(100); // Adjust the pulse width as needed
    digitalWrite(pulseTTLPin, LOW);
  } 
    Serial.print("Turned right for ");
    Serial.print(degrees);
    Serial.println(" degrees.");
  
}



void handlePowerCommand() {
  int power = Serial.parseInt();
  if (power == 1) {
    myStepper.setSpeed(0);
    if (echoOn) {
      Serial.println("Applied power to coils.");
    }
  } else {
    myStepper.setSpeed(0);
    if (echoOn) {
      Serial.println("Released power from coils.");
    }
  }
}

void handleDelayCommand() {
  int newDelay = Serial.parseInt();
  stepDelay = newDelay;
  myStepper.setSpeed(1000 / stepDelay);
  if (echoOn) {
    Serial.print("Step delay set to ");
    Serial.print(stepDelay);
    Serial.println(" ms.");
  }
}

void handleEchoCommand() {
  int newEcho = Serial.parseInt();
  echoOn = (newEcho == 1);
  if (echoOn) {
    Serial.println("Echo turned on.");
  } else {
    Serial.println("Echo turned off.");
  }
}

void printHelp() {
  Serial.println("Implemented Commands:");
  Serial.println("Command: Parameter: Effect: Example:");
  Serial.println("--------|------------|--------------------------------|------------------");
  Serial.println(" l number n Turn left for n steps l10 ");
  Serial.println(" r number n Turn right for n steps r10 ");
  Serial.println(" p 1 / 0 Apply / release power to coils e1 (default)");
  Serial.println(" d number n Sets the step delay to n ms d100 (=default)");
  Serial.println(" e 1 / 0 Sets the echo on / off x0 (=default)");
  Serial.println(" h - Display this help information h");
  Serial.println(" v - Display the firmware version v");
  Serial.println(" c - Clear screen on VT100 c");
  Serial.println("eee");
}

void printVersion() {
  Serial.println("Stepper Control v1.0");
}

void clearScreen() {
  Serial.write(27);       // ESC command
  Serial.print("[2J");    // Clear screen command
  Serial.write(27);
  Serial.print("[H");     // Cursor to home command
}
