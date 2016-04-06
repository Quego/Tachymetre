#include <FreqMeasure.h>

float frequence = 0;
int tension = 0;

int countPlus60 = 0;
int countMoins60 = 0;
double sum = 0;
double tmp = 0;

bool coherence = false;

void setup() {  
  Serial.begin(9600);
  pinMode(A0, INPUT);
  FreqMeasure.begin();
}

void loop() { 
  if (!coherence) {
    Serial.println(-1);
    delay(500);
    Serial.println(-2);
    delay(500);
    char c = Serial.read();
    if (c == 'T') coherence = true;
  } else {
    if (FreqMeasure.available()) {
      tmp = FreqMeasure.read();
      if (FreqMeasure.countToFrequency(tmp) > 60) {
        sum += tmp;
        countPlus60++;
        if (countPlus60 > 20) {
          frequence = FreqMeasure.countToFrequency(sum / countPlus60);
          //float v = abs(frequence / (2 * 10525000000 * cos(radians(0)) / 300000000)) * 3.6;
          //Serial.println(v);
          Serial.println(frequence);
          tension = analogRead(A0);
          Serial.println(tension);
          sum = 0;
          countPlus60 = 0;
          countMoins60 = 0;
        }
      } else {
        countMoins60++;
        if (countMoins60 > 20) {
          Serial.println(0);
          Serial.println(0);
          countMoins60 = 0;
          countPlus60 = 0;
          sum = 0;
        }
      }
    }
  }
}
