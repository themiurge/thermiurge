/********************************************************************/
// First we include the libraries
#include <OneWire.h> 
#include <DallasTemperature.h>

#define ONE_WIRE_BUS 2 
#define REQUEST_TEMP "REQ_TEMP"
#define RESPONSE_TEMP "RES_TEMP"

OneWire oneWire(ONE_WIRE_BUS); 

DallasTemperature sensors(&oneWire);

char c = 'a';

void setup(void) 
{ 
  Serial.begin(19200); 
  sensors.begin(); 
} 
void loop(void) 
{ 
    String str;
    if(Serial.available() > 0)
    {
        str = Serial.readString();
        //Serial.println(str);
        if (str == REQUEST_TEMP)
        {
            sensors.requestTemperatures();
            Serial.print(RESPONSE_TEMP);
            Serial.print(sensors.getTempCByIndex(0));
        }
    }

  //sensors.requestTemperatures();
  //Serial.print(sensors.getTempCByIndex(0));
  //delay(1000); 
} 
