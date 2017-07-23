#include <Servo.h>
#include "SnapFilter.h"
SnapFilter s1(0.007,4,1923); 
SnapFilter s2(0.007,4,1895);
SnapFilter s3(0.007,4,1890);

int GRP1[] = { 36, 38, 2};
int GRP2[] = { 22, 24, 3};                        // A, B, PWM Griper pins
int LA1[] =  { 28, 26, 4};                        // A, B, PWM long 0-1 up
int LA2[] =  { 34, 32, 5};                        // A, B, PWM short 1-0 up

int CH[] = { A9, A8, A7, A6, A5, A4, A3 };     //la,la,pitch,tt,grp,roll,yaw
float a = 0.5;
int pulse[7] = {};
int mapper[7] = {},py;

Servo yaw, pitch, roll;
int i = 0;
void setup() {
  for (i = 0; i < 7; i++)   // RC INPUT
    pinMode(CH[i], INPUT);
  for (i = 0; i < 3; i++) {  // LA outputs
    pinMode(LA1[i], OUTPUT);
    pinMode(LA2[i], OUTPUT);
    pinMode(GRP1[i], OUTPUT);
    pinMode(GRP2[i], OUTPUT);
  }
  yaw.attach(6);
  pitch.attach(8);
  roll.attach(7);
  //Serial.begin(9600);   //Debug
  Serial3.begin(9600);  // Turn Table
}

void loop() {
  rc();
    
 control(mapper[0], 20, LA1, abs(mapper[0]));
 control(mapper[1], 20, LA2, abs(mapper[1]));
 
  control(mapper[6], 20, GRP2, abs(mapper[6]));
  control(mapper[6], 20, GRP1, abs(mapper[6]));

  turntable(mapper[3]);

  pitch.writeMicroseconds(mapper[2]);
  yaw.writeMicroseconds(mapper[4]);
  roll.writeMicroseconds(mapper[5]);
}
void rc() {
  for (i = 0; i < 7; i++) 
    pulse[i] = pulseIn(CH[i], HIGH);
     
  pulse[2] = s1.Smooth(pulse[2]);
  pulse[4] = s2.Smooth(pulse[4]);
  pulse[5] = s3.Smooth(pulse[5]);
//  Serial.print(pulse[2]);
//  Serial.print(" ");
//  Serial.print(pulse[4]);
//  Serial.print(" ");
//  Serial.println(pulse[5]);
//  
  
  mapper[0] = map(pulse[0], 1058, 1890, 200, -200);   // short LA
  mapper[1] = map(pulse[1], 1152, 1973, 200, -200);   // long LA
  mapper[2] = map(pulse[2], 1098, 1923, 1200, 1800);  // pitch 1800 - 1100
  mapper[3] = map(pulse[3], 1158, 1974, 40, -40);     // TT
  mapper[4] = map(pulse[4], 1054, 1895, 1200, 1800);   // yaw
  mapper[5] = map(pulse[5], 1068, 1890, 1200, 1800);  // roll
  mapper[6] = map(pulse[6], 1055, 1880, -200, 200);   // grp
  mapper[3] = (mapper[3] < 10 && mapper[3] > -10) ? 0 : mapper[3];
}
void turntable(int x) {
  int y = map(x, -100, 100, 1, 127); 
  py = py * a + (1 - a) * y;
  Serial3.write(py);
  delay(5);
}
void control(int input, int limit, int M[], int pwm) {
  if (abs(input) <= limit)  action(M, 0, 0, 0);
  else if (input >  limit)  action(M, 0, 1, pwm);
  else if (input < -limit)  action(M, 1, 0, pwm);
  else action(M, 0, 0, 0);
}
void action(int motor[], boolean A, boolean B, int pwm) {
  digitalWrite(motor[0], A);
  digitalWrite(motor[1], B);
  analogWrite(motor[2], pwm);
}
