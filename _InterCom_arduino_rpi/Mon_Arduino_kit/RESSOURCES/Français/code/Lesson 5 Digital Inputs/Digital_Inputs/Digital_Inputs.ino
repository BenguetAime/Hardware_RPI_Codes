//www.elegoo.com
//2016.12.08

int ledPin = 5;
int buttonApin = 9;
int buttonBpin = 8;
bool state=1;
bool prevA=1;
bool prevB=1;

byte leds = 0;

void setup() 
{
  pinMode(ledPin, OUTPUT);
  pinMode(buttonApin, INPUT_PULLUP);  
  pinMode(buttonBpin, INPUT_PULLUP); 
  Serial.begin(9600); 
}

void loop() 
{
  if(state==1){digitalWrite(ledPin, HIGH); delay(10);}
  else {digitalWrite(ledPin, LOW); delay(10);}

  if (digitalRead(buttonApin) == LOW ){prevA=0;}
  else{prevA=1;}
  if (digitalRead(buttonBpin) == LOW ){prevB=0;}
  else{prevB=1;}

  if(prevA==0){state= !state;}
}
