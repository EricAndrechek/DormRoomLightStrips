#include <Adafruit_NeoPixel.h>

#define PIN 6

#define NUMPIXELS 118
#define INPUT_SIZE 4

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

#define DELAYVAL 500 // Time (in milliseconds) to pause between pixels

void setup() {
    Serial.begin(9600);
    pixels.begin();
    pixels.clear();
}

void loop() {
    if (Serial.available() > 0) {
        // char input[INPUT_SIZE + 1];
        // byte size = Serial.readBytes(input, INPUT_SIZE);
        // input[size] = 0;
        // if (strcmp(input, "comm") == 0) {
        //     Serial.println("good");
        // }
        // else if (strcmp(input, "show") == 0) {
        //     pixels.show();
        //     Serial.println("data");
        // }
        // else {
        //     int pixel = (int)input[0];
        //     int g = (int)input[1];
        //     int b = (int)input[2];
        //     int r = (int)input[3];
        //     pixels.setPixelColor(pixel, g, b, r);
        //     Serial.println(input);
        // }
        String data = Serial.readStringUntil('\n');
        if (data == "comm") {
            Serial.println("good");
        }
        else if (data == "show") {
            pixels.show();
            Serial.println("data");
        }
        else {
            int pixel = data.charAt(0);
            int g = data.charAt(1);
            int b = data.charAt(2);
            int r = data.charAt(3);
            pixels.setPixelColor(pixel, g, b, r);
            Serial.println(data);
        }
    }
}
