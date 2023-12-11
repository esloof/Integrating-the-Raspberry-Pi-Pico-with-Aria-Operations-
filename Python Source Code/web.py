from microdot import Microdot
import mm_wlan
import secrets
import gc
import json
from machine import Pin,ADC
from time import sleep

ssid = secrets.SSID
password = secrets.PASSWORD

pot = ADC(0) #pot input (knob potentiometer) connected to A0
mic = ADC(1) #mic input (microphine) connected to A1
button = Pin(16, Pin.IN, Pin.PULL_UP) #Button connected to D16
pir = Pin(18, Pin.IN, Pin.PULL_UP) #PIR connectec to D18
sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)

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

@app.post('/users')
def create_user(request):
    print ("hallo")
    response = "Hall0"
    return response, {'Content-Type': 'application/json'}

app.run(port=80)



#    potval = pot.read_u16()#Read A0 port pot value (65535~0)
#    micval = mic.read_u16()#Read A1 port mic valua (53000
#    buttonval = button.value()
#    pirval = pir.value()
#    print(potval)
#    print(buttonval)
#    print(pirval)
#    print(micval)
#    reading = sensor_temp.read_u16() * conversion_factor 
#    temperature = 27 - (reading - 0.706)/0.001721
#    print(temperature)
    
    