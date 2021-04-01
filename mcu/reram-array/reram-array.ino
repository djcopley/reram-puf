#include "sha256.h"

const int wordLines[] = {10, 11};
const int bitLines[] = {0, 1}

void setup()
{
    Serial.begin(115200);
    for (int line = 0; line < sizeof(wordLines); line++)
    {
        pinMode(wordLines[line], OUTPUT);
    }
}

void loop()
{
    // Is there a byte available to read
    if(Serial.available() > 0)
    {
        byte readByte = Serial.read();

    }
}