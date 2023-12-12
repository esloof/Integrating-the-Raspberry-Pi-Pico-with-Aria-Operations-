from microdot import Microdot
import mm_wlan
import secrets
import gc
import json
from machine import Pin,ADC
from time import sleep

ssid = secrets.SSID
password = secrets.PASSWORD

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
GP12 = Pin(15, Pin.IN, Pin.PULL_DOWN)
GP13 = Pin(16, Pin.IN, Pin.PULL_DOWN)
GP14 = Pin(19, Pin.IN, Pin.PULL_DOWN)
GP15 = Pin(20, Pin.IN, Pin.PULL_DOWN)

GP26 = ADC(0) #ADC0: Mapped to GP26
GP27 = ADC(1) #ADC1: Mapped to GP27
GP28 = ADC(2) #ADC2: Mapped to GP28 



pot = ADC(0) #pot input (knob potentiometer) connected to A0
mic = ADC(1) #mic input (microphine) connected to A1
button = Pin(16, Pin.IN, Pin.PULL_UP) #Button connected to D16
pir = Pin(18, Pin.IN, Pin.PULL_UP) #PIR connectec to D18
sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)

app = Microdot()  
mm_wlan.connect_to_network(ssid, password)

@app.route('/api')
def index(request):
    msg = {"identifier": "Eric's Pi Pico"}
    print (msg)
    response = json.dumps(msg)
    return response, {'Content-Type': 'application/json'} 

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
    reading = sensor_temp.read_u16() * conversion_factor 
    temperature = 27 - (reading - 0.706)/0.001721
    msg = {"temperature":temperature}
    print (msg)
    response = json.dumps(msg)
    return response, {'Content-Type': 'application/json'}   

@app.route('/api/analog')
def index(request):
    potval = pot.read_u16()
    micval = mic.read_u16()
    msg = {"pot":potval,"mic":micval}
    print (msg)
    response = json.dumps(msg)
    return response, {'Content-Type': 'application/json'}    
    
@app.route('/api/digital')
def index(request):
    buttonval = button.value()
    pirval = pir.value()
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

@app.post('api/testpost')
def create_user(request):
    response = "Hello"
    return response, {'Content-Type': 'application/json'}

app.run(port=80)

    
    