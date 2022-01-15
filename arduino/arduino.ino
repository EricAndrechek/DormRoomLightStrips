#include <Adafruit_NeoPixel.h>

#define PIN 6

#define NUMPIXELS 118
#define INPUT_SIZE 5

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
            int n = ((int)data.charAt(0)) - 33;
            int g = ((int)data.charAt(1)) - 33;
            int b = ((int)data.charAt(2)) - 33;
            int r = ((int)data.charAt(3)) - 33;
            int x = ((int)data.charAt(4)) - 33;
            if (x >= 27) n += 59;
            x = x % 27;
            int h = x / 9;
            x = x % 9;
            int i = x / 3;
            x = x % 3;
            int j = x;
            g = g + 86 * h;
            b = b + 86 * i;
            r = r + 86 * j;
            pixels.setPixelColor(n, g, b, r);
            Serial.println(data);
        }
    }
}
