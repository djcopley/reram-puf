#include "sha256.h"

const int wordLines[] = {10, 11};
const int bitLines[] = {0, 1};
const int resistance = 30000; // Resistance of current sensing resistor
const int rcDelay = 100; // time in ms to delay

byte getAddress(byte value)
{
    return value >> 6;
}

byte getVoltage(byte value)
{
    return (value & 0x3F) << 2; // Mask bottom 6 bits and SHL 2 for 1 byte value
}

float scaleVoltage(int voltage)
{
    return (voltage) * (5 / 1024);
}

void serialWriteFloat(float *value)
{
    Serial.write(value, 4)
}

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
        byte address = getAddress(readByte);
        byte voltage = getVoltage(readByte);
        analogWrite(wordLines[address & 2 >> 1], voltage); // Write voltage to pin stored at top addr bit
        delay(rcDelay);
        float current = scaleVoltage(analogRead(bitLines[address & 1])) / resistance;
        serialWriteFloat(current); // Write the current as a floating point number
    }
}