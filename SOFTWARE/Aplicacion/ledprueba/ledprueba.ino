#include <FastLED.h>

#define NUM_LEDS 64
#define DATA_PIN 6       // Pin de datos de tu tira
#define BAUD_RATE 115200

CRGB leds[NUM_LEDS];

void setup() {
    FastLED.addLeds<WS2812B, DATA_PIN, GRB>(leds, NUM_LEDS);
    FastLED.setBrightness(80);
    Serial.begin(BAUD_RATE);
}

void loop() {
    // Esperar exactamente 192 bytes (64 LEDs × R,G,B)
    if (Serial.available() >= 192) {
        for (int i = 0; i < NUM_LEDS; i++) {
            uint8_t r = Serial.read();
            uint8_t g = Serial.read();
            uint8_t b = Serial.read();
            leds[i] = CRGB(r, g, b);
        }
        FastLED.show();
        
        // Limpiar cualquier byte extra que haya llegado
        while (Serial.available()) Serial.read();
    }
}
