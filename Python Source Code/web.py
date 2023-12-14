from microdot import Microdot # Taken from https://github.com/monkmakes/pmon/tree/main/raspberry_pi_pico
from lcd1602 import LCD1602 # Taken from https://wiki.seeedstudio.com/Grove-Starter-Kit-for-Raspberry-Pi-Pico/
from dht20 import DHT20 # Taken from https://github.com/flrrth/pico-dht20/blob/main/dht20/dht20.py
import mm_wlan # Taken from https://github.com/monkmakes/pmon/tree/main/raspberry_pi_pico
import secrets # File used to store the WiFi Username and password eg SSID = 'YOUR WI-FI AP NAME' PASSWORD = 'YOUR WI-FI PASSWORD'
import gc # Garbage Collector interface for reteiving free memeory
import json # Python's built-in package used to work with JSON data
from machine import I2C,Pin,ADC # Interface to the I2C but, Pins and GPIOs
from time import sleep # Add Time Delays to Your Code

ssid = secrets.SSID # WiFi SSID
password = secrets.PASSWORD # WiFi Password

GP0 = Pin(1, Pin.IN, Pin.PULL_DOWN)
GP1 = Pin(2, Pin.IN, Pin.PULL_DOWN)
GP2 = Pin(4, Pin.IN, Pin.PULL_DOWN)
GP3 = Pin(5, Pin.IN, Pin.PULL_DOWN)
GP4 = Pin(6, Pin.IN, Pin.PULL_DOWN)
GP5 = Pin(7, Pin.IN, Pin.PULL_DOWN)
GP6 = Pin(9, Pin.IN, Pin.PULL_DOWN)
GP7 = Pin(10, Pin.IN, Pin.PULL_DOWN)
GP8 = Pin(11, Pin.IN, Pin.PULL_DOWN)
GP9 = Pin(12, Pin.IN, Pin.PULL_DOWN)
GP10 = Pin(14, Pin.IN, Pin.PULL_DOWN)
GP11 = Pin(15, Pin.IN, Pin.PULL_DOWN)
GP12 = Pin(16, Pin.IN, Pin.PULL_DOWN) # Grove - Mini PIR motion sensor connected to D16
GP13 = Pin(17, Pin.IN, Pin.PULL_DOWN)
GP14 = Pin(18, Pin.IN, Pin.PULL_DOWN) # Grove - Button connected to D18

GP15 = Pin(20, Pin.OUT) # Grove - LED Pack attached to D20

GP26 = ADC(0) #ADC0: Mapped to GP26 Rotary Angle Sensor
GP27 = ADC(1) #ADC1: Mapped to GP27 Grove - Sound Sensor
GP28 = ADC(2) #ADC2: Mapped to GP28 Grove - Light Sensor

i2c0 = I2C(0, sda=Pin(8), scl=Pin(9))
dht20 = DHT20(0x38, i2c0)
#Decimal address: 56 , Hex address:  0x38

i2c1 = I2C(1,sda=Pin(6), scl=Pin(7), freq=400000)
display = LCD1602(i2c1, 2, 16)
display_i2c_address = i2c1.scan()[0]
#Decimal address: 62 , Hex address:  0x3e

app = Microdot()  
mm_wlan.connect_to_network(ssid, password)

@app.route('/api/id')
def index(request):
    msg = {"identifier": "Eric's Pi Pico"}
    print (msg)
    response = json.dumps(msg)
    return response, {'Content-Type': 'application/json'}  

@app.route('/api/memory')
def index(request):
    msg = {"memory": gc.mem_free()}
    print (msg)
    response = json.dumps(msg)
    return response, {'Content-Type': 'application/json'}  

@app.route('/api/temperature')
def index(request):
    reading = machine.ADC(4).read_u16() * (3.3 / (65535))
    pico_temperature = 27 - (reading - 0.706)/0.001721
    measurements = dht20.measurements
    #print(f"Temperature: {measurements['t']} °C, humidity: {measurements['rh']} %RH")
    temperature = measurements['t']
    humidity = measurements['rh']
    msg = {"pico_temperature":pico_temperature, "temperature":temperature, "humidity":humidity }
    print (msg)
    response = json.dumps(msg)
    return response, {'Content-Type': 'application/json'}   

@app.route('/api/analog')
def index(request):
    potval = GP26.read_u16() # Rotary Angle Sensor
    micval = GP27.read_u16() # Grove - Sound Sensor
    lightval = GP28.read_u16() #Grove - Light Sensor
    msg = {"pot":potval,"mic":micval, "light":lightval}
    print (msg)
    response = json.dumps(msg)
    return response, {'Content-Type': 'application/json'}    
    
@app.route('/api/digital')
def index(request):
    buttonval = GP12.value()
    pirval = GP15.value()
    msg = {"buttonval":buttonval,"pirval":pirval}
    print (msg)
    response = json.dumps(msg)
    return response, {'Content-Type': 'application/json'}

@app.get('/api/gp')
def get_gp(request):
    msg = {"GP0":GP0.value(),
           "GP1":GP1.value(),
           "GP2":GP2.value(),
           "GP3":GP3.value(),
           "GP4":GP4.value(),
           "GP5":GP5.value(),
           "GP6":GP6.value(),
           "GP7":GP7.value(),
           "GP8":GP8.value(),
           "GP9":GP9.value(),
           "GP10":GP10.value(),
           "GP11":GP11.value(),
           "GP12":GP12.value(),
           "GP13":GP13.value(),
           "GP14":GP14.value(),
           "GP26":GP26.read_u16(),
           "GP27":GP27.read_u16(),
           "GP28":GP28.read_u16()}
    print (msg)
    response = json.dumps(msg)
    return response, {'Content-Type': 'application/json'}

@app.get('/api/test')
def get_test(request):
    msg = {"test":"oke"}
    print (msg)
    response = json.dumps(msg)
    return response, {'Content-Type': 'application/json'}

# from postman use POST http://192.168.178.46/api/led
#{
#    "Client Identifier": "Postman",
#    "GPIOS": [
#        {
#            "GP13": 1
#            "GP14": 0
#            "GP15": 0
#        }
#    ]
#}

@app.post('api/led')
def control_led(request):
    body = request.json
    print (body)
    for items in body["GPIOS"]:
        GP13 = items.get('GP13')
        GP14 = items.get('GP14')
        GP15.value(items.get('GP15'))
    return {'success': True}, {'Content-Type': 'application/json'}

#{
#    "Client Identifier": "Postman",
#    "GPIOS": [
#        {
#            "I2C1L1": "This is line one"
#            "I2C1L2": "This is line two"
#        }
#    ]
#}

@app.post('api/display')
def control_display(request):
    body = request.json
    print (body)
    for items in body["GPIOS"]:
        I2C1L1 = items.get('I2C1L1')
        I2C1L2 = items.get('I2C1L2')
    display.home()
    display.print(str(I2C1L1))
    display.setCursor(0, 1)
    display.print(str(I2C1L2))
    return {'success': True}, {'Content-Type': 'application/json'}

app.run(port=80)

    
    
