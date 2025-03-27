#include <Arduino.h>
#include <DHT.h>

// Define DHT11 Sensor
#define DHTPIN 4        // GPIO4 for DHT11
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

// Define MQ135 Sensor
#define MQ135_PIN A0   // Analog pin for MQ135

void setup() {
    Serial.begin(115200);  // Initialize Serial Communication
    dht.begin();           // Start DHT11 Sensor
}

void loop() {
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();
    int airQuality = analogRead(MQ135_PIN);  // Read air quality value from MQ135

    if (isnan(temperature) || isnan(humidity)) {
        Serial.println("{\"error\":\"DHT11 Read Failed\"}");
    } else {
        // Format Data as JSON and Send via Serial
        Serial.print("{\"temperature\":");
        Serial.print(temperature);
        Serial.print(",\"humidity\":");
        Serial.print(humidity);
        Serial.print(",\"airQuality\":");
        Serial.print(airQuality);
        Serial.println("}");
    }

    delay(5000);  // Send data every 5 seconds
}
