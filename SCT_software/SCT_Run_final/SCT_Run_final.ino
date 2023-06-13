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
unsigned long impulse_duration; // [ms] may be overrided by potentiometer
float duty_cycles[n_bands]; // [%] ~ of a potentiometer and a selector (allows to regulate the inner-pressure)
float impulse_repartition[] = {33.33, 33.33, 33.33}; // [%] (hardcoded: size = n_bands, sum = 100) 
int period = 100; // [ms] (of the duty cycle)
int end_waiting_time = 5000; // [ms]


// #######################  ____   __     __ _   __  ____    ____  ____  __  ____  ####################### 
// ####################### (    \ /  \   (  ( \ /  \(_  _)  (  __)(    \(  )(_  _) ####################### 
// #######################  ) D ((  O )  /    /(  O ) )(     ) _)  ) D ( )(   )(   ####################### 
// ####################### (____/ \__/   \_)__) \__/ (__)   (____)(____/(__) (__)  ####################### 

// Using potentiometers (override precedent parameters if true)
bool impulse_duration_pot = true;
bool duty_cycle_pot = true;

// Time management
unsigned long start_time = 300000; // you got 5 minutes to set up the parameters to the desired values before the SCT starts
unsigned long current_time;
unsigned long condition;
unsigned long remaining;
int counter = 1;

// Screen management
LiquidCrystal_I2C lcd(0x27, 2, 1, 0, 4, 5, 6, 7, 3, POSITIVE);  
char buffer[10];

// Conversion management for potentiometers
int readValue1;
int readValue2;
float writeReadConversion=255./1023.;
unsigned long writeValue1;
unsigned long writeValue2;

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
    
  if (!impulse_duration_pot) {
    impulse_duration = 15000;
  }
  if (!duty_cycle_pot) {
    for (int i = 0; i < n_bands; i++) {
      duty_cycles[i] = 100.0;
    }
  }
  // For Start confirmation
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);delay(1000);digitalWrite(LED_BUILTIN, LOW);
  delay(1000);
  digitalWrite(LED_BUILTIN, HIGH);delay(1000);digitalWrite(LED_BUILTIN, LOW);
  delay(1000);
  digitalWrite(LED_BUILTIN, HIGH);delay(1000);digitalWrite(LED_BUILTIN, LOW);

  // Setting phase
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
  // Starting (setting phase)
  current_time = millis();
  while(current_time < start_time){  
    current_time = millis();
    // - display impulse duration
    lcd.setCursor(4, 1);
    dtostrf(impulse_duration/1000, 2, 0, buffer);
    lcd.print(buffer);
    // - display duty cycles
    for(int i = 0; i < n_bands; i++){
      lcd.setCursor(3+i*4, 2);
      dtostrf(duty_cycles[i], 3, 0, buffer);
      lcd.print(buffer);
      if(i != n_bands-1){
        lcd.print("/"); 
      }
    }
  // Potentiometers for period
  if(impulse_duration_pot){
    readValue1=analogRead(PotIDpin);
    writeValue1 = map(readValue1, 0.0, 1023.0, 6000, 91000) - 500;
    impulse_duration = writeValue1;
  }
  // Potentiometers for duty_cycle
  if(duty_cycle_pot){
    for(int i = 0; i < n_bands; i++){
        readValue2 = analogRead(PotDCPins[i]);
        writeValue2 =  map(readValue2, 0.0, 1023.0, 900, 1001);
        duty_cycles[i] = writeValue2/10;
      }
    }
    // - display remaining time before SCT
    lcd.setCursor(0, 3);
    lcd.print("time left: "); 
    lcd.setCursor(10, 3);
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
  dtostrf(remaining/60000.0, 3, 0, buffer);
  lcd.print(buffer); 
  // Straps inflation
  for (int i = 0; i < n_bands; i++) {
    // Duty Cycle
    float onTime = (duty_cycles[i] / 100.0) * period;
    float offTime = period - onTime;
    Serial.println(duty_cycles[i]);
    // Impulse sequence
    sequence(i, valvesPins[i], onTime, offTime);
  }
  delay(end_waiting_time);
  counter = counter+1;
}
