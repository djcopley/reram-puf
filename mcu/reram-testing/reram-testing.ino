const int wordLines[] = {10, 11};
const int bitLines[] = {A0, A1};
const int resistance = 5000; // Resistance of current sensing resistor
const int rcDelay = 100; // time in ms to delay

const byte numChars = 32;
char receivedChars[numChars];
bool newData = false;

byte getAddress(word value)
{
    return (value >> 10) & 3;
}

word getInputData(word value)
{
    return value & 1023; // Mask top 6 bits to get lower 10 bits for voltage/current
}

float scaleVoltage(int voltage)
{
    return (voltage) * (5.0 / 1024.0);
}

void serialWriteFloat(float *buf)
{
    Serial.write((uint8_t *) buf, 4); // Write the float to the serial port
    //Serial.println(*buf);
}

byte getInstruction(word value)
{
    return (value >> 12) & 1;
}

int readBinaryString(char *s) 
{
    int result = 0;
    while(*s) 
    {
        result <<= 1;
        if(*s++ == '1') result |= 1;
    }
    return result;
}

char * recvWithStartEndMarkers()
{
    static boolean inProgress = false;
    static byte index = 0;
    char startMarker = '<';
    char endMarker = '>';
    char recvChar;

    while (Serial.available() > 0 && newData == false)
    {
        recvChar = Serial.read();

        if (inProgress)
        {
            if (recvChar != endMarker)
            {
                receivedChars[index] = recvChar;
                index++;

                if (index >= numChars)
                {
                    index = numChars - 1;
                }
            }
            else
            {
                receivedChars[index] = '\0'; //terminate string
                inProgress = false;
                index = 0;
                newData = true;
            }
        }

        else if (recvChar == startMarker)
        {
            inProgress = true;
        }
    }
    return receivedChars;
}

void showNewData()
{
    if (newData) 
    {
        //Serial.print(receivedChars);
        newData = false;
    }
}

float get_current_from_voltage(byte address, byte voltage)
{
    analogWrite(wordLines[address >> 1], voltage); // Write voltage to pin stored at top addr bit
    delay(rcDelay);
    int analog_raw = analogRead(bitLines[address & 1]);
    //Serial.print("Analog Raw: ");
    //Serial.println(analog_raw);
    float current_in_amps = scaleVoltage(analog_raw) / resistance;
    float current_in_uamps = current_in_amps * 1000000;
    analogWrite(wordLines[address & 1], 0);
    return current_in_uamps;
}

float get_voltage_from_current(byte address, word current)
{
    int current_threshold = 10;
    for (int voltage = 0; voltage < 255; voltage++)
    {
        float current_out = get_current_from_voltage(address, voltage);
        if (abs(current_out - current) < current_threshold)
        {
            return voltage * 5.0 / 255.0;
        }
    }
    return 5.0;
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
    recvWithStartEndMarkers();
    if (newData)
    {
        //String instr_str = receivedChars;
        // Serial.print("Instruction: ");
        // Serial.println(receivedChars);

        //byte instr_word = atoi(receivedChars);
        word input_raw = readBinaryString(receivedChars);
        byte instr_byte = getInstruction(input_raw);
        byte address = getAddress(input_raw);
        word data_word = getInputData(input_raw);
        // Serial.print("Integer data: ");
        // Serial.println(data_word);

        // Serial.print("Instruction bit: ");
        // Serial.println(instr_byte);

        if (!instr_byte)
        {
            // Serial.print("Address: ");
            // Serial.println(address);
            // Serial.print("Voltage to WL: ");
            float voltage = data_word / 255.0 * 5.0;
            // Serial.println(voltage);

            float current_in_uamps = get_current_from_voltage(address, (byte)data_word);
            // Serial.println("Current in uA: ");
            Serial.println(current_in_uamps);
        }
        else
        {
            float voltage_out = get_voltage_from_current(address, data_word);
            // Serial.println("Output Voltage: ");
            Serial.println(voltage_out);
        }
        newData = false;
    }
}
