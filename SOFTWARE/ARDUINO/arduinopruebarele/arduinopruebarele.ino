int reed = 4;


void setup() {
pinMode(reed, INPUT_PULLUP);
Serial.begin(9600);

}

void loop() {
  if (digitalRead(reed) == HIGH){
  Serial.println("pipipipi");
  
  } else {
  Serial.println("nada");
}
delay(350);
}