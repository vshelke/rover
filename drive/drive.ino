float filter = 0.5;                           //filter       
int ch[3] = {A1, A3, A4};                         //fb, rl, shift
int mapper[2] = {}, f_map[2] = {}, pulse[2] = {};
int rcmax[2] = { 1883, 1883 };                //rc values maxfb maxrl               
int rcmin[2] = { 1033, 1033 };                //rc values minfb minrl
int sensi = 50;                              // sensitivity
int left = 0 , right = 0;

void setup() {
  Serial.begin(38400);
  Serial1.begin(9600);
  Serial2.begin(9600);
  Serial3.begin(9600);
  for (int i = 0; i < 2; i++)
    pinMode(ch[i], INPUT);             
}
void loop() {
  rc();                                      //initialize and map rc values  
  if (pulse[2] > 1888)
    alg();                                    //run drive code            
  else 
    autobot_run();
}
void rc() {
  for (int i = 0 ; i < 3; i++)          
    pulse[i] = pulseIn(ch[i], HIGH);    
    
  mapper[0] = map( pulse[0], rcmin[0], rcmax[0], sensi, -sensi);   //front-back
  mapper[0] = safe(mapper[0]);

  mapper[1] = map( pulse[1], rcmin[1], rcmax[1], sensi, -sensi);  //left-right
  mapper[1] = safe(mapper[1]);
}
int safe(int y) {                           //checks for the stop condition range (-10 - 10)
  return (y < 10 && y > -10) ? 0 : y;
}
void autobot_run() {
  if (Serial3.available() > 0) {
    if (Serial3.read() == 174) {              delay(1);
      left = Serial3.read();                  delay(1);
      int tmp = Serial3.read();
      right = map(tmp, 1, 127, 129, 255);     delay(1);
      if (Serial3.read() != 175) {
        left = 0;
        right = 0; 
      }
    }
  }
  delay(1);
  motors(left);
  motors(right);
}
void alg() {                                                 
  f_map[0] = f_map[0] * filter + (1 - filter) * mapper[0];  
  f_map[1] = f_map[1] * filter + (1 - filter) * mapper[1];
  left = map(f_map[0] + f_map[1], -100, 100, 1, 127);
  right = map(f_map[0] - f_map[1], -100, 100, 129, 255);
  motors( left );
  motors( right );
}
void motors(int t) {  
  Serial1.write(t);                                
  delay(5);
  Serial2.write(t);                                     
  delay(5);
  Serial3.write(t);
  delay(5);
}

