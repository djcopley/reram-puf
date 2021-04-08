const int wordLines[] = {10, 11};
const int bitLines[] = {A0, A1};
const int resistance = 5000; // Resistance of current sensing resistor
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

void serialWriteFloat(float buf)
{
    Serial.write((char *) &buf, 4); // Write the float to the serial port
}

void setup()
{
    Serial.begin(115200);
    for (int line = 0; line < 2; line++)
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
        analogWrite(wordLines[address >> 1], voltage); // Write voltage to pin stored at top addr bit
        delay(rcDelay);
        float current_in_amps = scaleVoltage(analogRead(bitLines[address & 1])) / resistance;
        int current_in_uamps = (int) (current_in_amps * 1000000);
        serialWriteInt(current_in_uamps); // Write the current as an integer
    }
}
