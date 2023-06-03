// Author : Arthur Van Geersdaele
// Date-time : 23-06-01, 09h03m17s
#include <LiquidCrystal_I2C.h>
#include <Wire.h>

// #######################  _  _  ____  ____  ____      ____  __   __ _  ____  #######################
// ####################### / )( \/ ___)(  __)(  _ \ ___(__  )/  \ (  ( \(  __) #######################
// ####################### ) \/ (\___ \ ) _)  )   /(___)/ _/(  O )/    / ) _)  #######################
// ####################### \____/(____/(____)(__\_)    (____)\__/ \_)__)(____) #######################

// Arduino connexion pins
// - for pump
int Pump1pin = 10; 
// - for valves (from distal band to proximal)
int valvesPins[] = {9, 8, 7};
// - for potentiometers (ID - impulse duration control, DC - duty cycles control)
int PotIDpin = A0; 
int PotDCPins[] = {A1, A2, A3};

// Specifications 
const int n_bands  = sizeof(valvesPins) / sizeof(int);

// Therapy parameters
int impulse_duration; // [ms] (to set with the potentiometer or to force below)
float duty_cycles[n_bands]; // [%] (to set with the potentiometer or to force below) [allows to regulate the inner-pressure]
float impulse_repartition[] = {33.33, 33.33, 33.33}; // [%] (to manually define: size = n_bands, sum = 100) 
int period = 1; // [ms] (to manually define) [period on which the duty cycle is applied]
int end_waiting_time = 5000; // (to manually define) [ms]

// Using potentiometers (set to false override the potentiometers)
bool impulse_duration_pot = true;
bool duty_cycle_pot = true;

if (!impulse_duration_pot) {
  impulse_duration = 15000;
}
if (!duty_cycle_pot) {
  for (int i = 0; i < n_bands; i++) {
    duty_cycles[i] = 100.0;
  }
}

// #######################  ____   __     __ _   __  ____    ____  ____  __  ____  ####################### 
// ####################### (    \ /  \   (  ( \ /  \(_  _)  (  __)(    \(  )(_  _) ####################### 
// #######################  ) D ((  O )  /    /(  O ) )(     ) _)  ) D ( )(   )(   ####################### 
// ####################### (____/ \__/   \_)__) \__/ (__)   (____)(____/(__) (__)  ####################### 

// Time management
unsigned long start_time = 5*60*1000; // you got X seconds to set up the parameters to the desired values before the SCT starts
unsigned long current_time;
unsigned long condition;
unsigned long remaining;
int counter = 1;

// Screen management
LiquidCrystal_I2C lcd(0x27, 2, 1, 0, 4, 5, 6, 7, 3, POSITIVE);  
char buffer[10];

// Conversion management for potentiometers
float readValue1;
float readValue2;
float writeReadConversion=255./1023.;
float writeValue1;
float writeValue2;

// Useful functions for therapy
void contraction(int pin, float onTime, float offTime){
  digitalWrite(pin, HIGH);
  delay(onTime);
  digitalWrite(pin, LOW);
  delay(offTime);
};

void sequence(int i, int pin, float onTime, float offTime){
  digitalWrite(pin, HIGH);
  while (millis() -  start_time - round((float) (impulse_duration + end_waiting_time)*(counter-1)) < impulse_repartition[i] * impulse_duration /100) {
  //while (millis() -  start_time - (impulse_duration + end_waiting_time)*(counter-1) < round((float) impulse_repartition[i] * impulse_duration /100)) {
    contraction(pin, onTime, offTime);
  }
  digitalWrite(pin, LOW);
};

// Useful structural function 
void cumulative(float* tmp, int n_bands) {
  for (int i = 1; i < n_bands; i++) {
    tmp[i] = tmp[i] + tmp[i-1];
  }
}

// TODO : LCD function to light the code

void setup() {
  // Debug and feedbacks
  Serial.begin(9600);
  lcd.begin(20, 4);

  // PinModes
  pinMode(Pump1pin, OUTPUT);
  pinMode(PotIDpin, INPUT);
  for (int i = 0; i < n_bands; i++) {
    pinMode(valvesPins[i], OUTPUT);
    pinMode(PotDCPins[i], INPUT);
  }

  // Data conversion
  cumulative(impulse_repartition, n_bands);

  // For Start confirmation
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);delay(1000);digitalWrite(LED_BUILTIN, LOW);
  delay(1000);
  digitalWrite(LED_BUILTIN, HIGH);delay(1000);digitalWrite(LED_BUILTIN, LOW);
  delay(1000);
  digitalWrite(LED_BUILTIN, HIGH);delay(1000);digitalWrite(LED_BUILTIN, LOW);

  // Settings phase
  lcd.clear();
  // Display setting title
  lcd.setCursor(0, 0);
  lcd.print("[SCT SETTINGS]");     
  // - display impulse duration label
  lcd.setCursor(0, 1);
  lcd.print("ID: "); 
  lcd.setCursor(17, 1);
  lcd.print("[s]"); 
  // - display duty cycles label
  lcd.setCursor(0, 2);
  lcd.print("DC: "); 
  lcd.setCursor(17, 2);
  lcd.print("[%]");
  while(millis() < start_time){  
    // - display impulse duration
    lcd.setCursor(4, 1);
    dtostrf(impulse_duration/1000, 2, 0, buffer);
    lcd.print(buffer);
    // - display duty cycles
    for(int i = 0; i < n_bands; i++){
      lcd.setCursor(3+i*4, 2);
      dtostrf(duty_cycles[i], 3, 0, buffer);
      lcd.print(buffer);
      if(i != n_bands){
        lcd.print("/"); 
      }
    }
    // Potentiometers for period ~ needs selector implementation
  if(impulse_duration_pot){
    readValue1=analogRead(PotIDpin);
    writeValue1=(writeReadConversion)*readValue1/5;
    impulse_duration = writeValue1 * 500;
  }
  // Potentiometers for duty_cycle ~ needs selector implementation
  if(duty_cycle_pot){
    for(int i = 0; i < n_bands; i++){
        readValue2=analogRead(PotDCPins[i]);
        writeValue2= (readValue2/1023.);
        duty_cycles[i] = writeValue2 * 100;
    }
  }
    // - display remaining time before SCT
    lcd.setCursor(0, 3);
    lcd.print("time left: "); 
    lcd.setCursor(10, 3);
    current_time = millis();
    remaining = start_time - current_time;
    dtostrf(remaining/1000.0, 3, 0, buffer);
    lcd.print(buffer); 
    lcd.setCursor(17, 3);
    lcd.print("[s]"); 
    delay(500);
  }
  
  // Display SCT running title
  lcd.setCursor(0, 0);
  lcd.print("[SCT RUNNING] "); 
  // Display total SCT duration
  lcd.setCursor(0, 3);
  lcd.print("time:          "); 
  lcd.setCursor(15, 3);
  lcd.print("[min]");
  // Handling time
  start_time = millis();
  // Pump start
  digitalWrite(Pump1pin, HIGH);
}

void loop() {
  // Display total SCT duration
  lcd.setCursor(5, 3);
  current_time = millis();
  remaining = current_time - start_time;
  dtostrf(remaining/60000.0, 3, 0, buffer); // current time - 5 minutes setting - 5 seconds blink
  lcd.print(buffer); 
  // Straps inflation
  for (int i = 0; i < n_bands; i++) {
    // Duty Cycle
    float onTime = (duty_cycles[i] / 100.0) * period;
    float offTime = period - onTime;
    // Impulse sequence
    sequence(i, valvesPins[i], onTime, offTime);
  }
  delay(end_waiting_time);
  counter = counter+1;
}
