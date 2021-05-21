import machine
import ujson
import utime
from dht import DHT11, InvalidChecksum

uart = machine.UART(0, baudrate = 9600, timeout = 1)
sensorSuelo = machine.ADC(26)
pinDHT = machine.Pin(5, machine.Pin.OUT, machine.Pin.PULL_DOWN)
ventiladorPin = machine.Pin(13, machine.Pin.OUT)
bombaPin = machine.Pin(12, machine.Pin.OUT)
tiempoUltimaLectura = utime.ticks_ms()
ID = 10000

def envia(doc):
    x = ujson.dumps(doc)
    uart.write(x)
    return

def recibe():
    y = uart.readline()
    return y

def sensorDHT():
    sensor = DHT11(pinDHT)
    temperatura  = sensor.temperature
    humedad = sensor.humidity
    return temperatura, humedad

while True:
    rx = recibe()
    
    if rx == b'a':
        ventiladorPin.value(1)
    elif rx == b'b':
        ventiladorPin.value(0)
    elif rx == b'c':
        bombaPin.value(1)
    elif rx == b'd':
        bombaPin.value(0)
    
    if utime.ticks_diff(utime.ticks_ms(), tiempoUltimaLectura) > 2000:
        
        if ID > 19999:
            ID = 10000
        else:
            ID = ID + 1
        
        entradaA0 = sensorSuelo.read_u16()
        humedadSuelo = 100 - ((entradaA0)/(65535))*100
        lectura = sensorDHT()
        temperatura = lectura[0]
        humedad = lectura[1]
        
        tx = {
            "ID" : ID,
            "TEMPERATURA" : temperatura,
            "A_HUMEDAD" : humedad,
            "S_HUMEDAD" : humedadSuelo  
        }
        
        envia(tx)
        
        tiempoUltimaLectura = utime.ticks_ms()