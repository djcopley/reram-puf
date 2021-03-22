#include "crypto.h"


void setup()
{
    Serial.begin(115200);
}

void loop()
{
    while(Serial.available() > 0)
    {
    }
    // Serial message available?
    // First byte: Instruction
        // Enroll (0xFF 0x00)
            // Send common password
            // Return PUF LUT (How long?)

        // Encrypt (0xFF 0x01) TO BE CONTINUED
            // Handshake
            // User inputs common password (NULL terminated)
            // User inputs plaintext message (NULL terminated)
            // Break message into 2-bit grousp
            // Uses circuit to generate cipher text
            // Returns cipher text to host

            // NOT COMPLETE //

        // Decrypt (0xFF 0x02)
            // Handshake
            // Recieve random number
            // Hash with password
            // Concat salt and password
            // Hash
            // Extract
        // Else, Error
}