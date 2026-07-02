#include <FastLED.h>

#define NUM_LEDS 64
#define DATA_PIN 4

CRGB leds[NUM_LEDS];

void setup() {

  Serial.begin(115200);

  FastLED.addLeds<WS2812B, DATA_PIN, GRB>(leds, NUM_LEDS);

  fill_solid(leds, NUM_LEDS, CRGB::Blue);
  FastLED.show();
}

void loop() {

  if (Serial.available()) {

    for (int i = 0; i < NUM_LEDS; i++) {

      while (Serial.available() < 3);

      byte r = Serial.read();
      byte g = Serial.read();
      byte b = Serial.read();

      leds[i].r = r;
      leds[i].g = g;
      leds[i].b = b;
    }

    FastLED.show();
  }
}