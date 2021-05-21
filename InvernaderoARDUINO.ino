#include <ArduinoJson.h>
#include <DHT.h>
#define DHTPIN 8
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);
const int sensorSueloPin = A0;
int id = 10000;
int offset = 280;
int ventiladorPin = 9;
int bombaPin = 10;
long tiempoUltimaLectura=0;

void setup() {
  Serial.begin(9600);
  dht.begin();//Se inicializa en sensor
  pinMode(ventiladorPin, OUTPUT);
  pinMode(bombaPin, OUTPUT);  
}

void loop() {
  if (Serial.available()>0){
    char recibe = Serial.read();
    if (recibe == 'a'){
      digitalWrite(ventiladorPin, HIGH);
    }
    else if (recibe == 'b'){
      digitalWrite(ventiladorPin, LOW);   
    }
    else if (recibe == 'c'){
      digitalWrite(bombaPin, HIGH);
    }
    else if (recibe == 'd'){
      digitalWrite(bombaPin, LOW);  
    }
  }
  if(millis() - tiempoUltimaLectura > 1000){
    if (id > 19999){
      id = 10000;
    }
    else{
      id = id + 1;
    }
  
    float entradaA0 = analogRead(sensorSueloPin);
    int humedadSuelo = 100 - ((entradaA0 - offset)/(1023 - offset))*100;
    int humedad = dht.readHumidity();
    int temperatura = dht.readTemperature();
 
    //String envia = "{\"ID\":\"12ABF12\",\"TEMPERATURA\":" + (String)temperatura + ",\"A_HUMEDAD\":" + (String)humedad + ",\"S_HUMEDAD\":" + (String)humedad + "}";
    StaticJsonDocument<32> doc;
    doc["ID"] = id;
    doc["TEMPERATURA"] = temperatura;
    doc["A_HUMEDAD"] = humedad;
    doc["S_HUMEDAD"] = humedadSuelo;
    String envia;
    serializeJson(doc, envia);
    Serial.println(envia); 
    tiempoUltimaLectura = millis();
  }
}
