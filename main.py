import DFRobot_AHT20
import time
import sys
from machine import Pin, I2C

onboard = Pin("LED", Pin.OUT, value=0)
i2c = I2C(0, scl=Pin(17), sda=Pin(16))
sensor = DFRobot_AHT20.DFRobot_AHT20(i2c)
sensor.begin()

def read_sensor(sensor):
    try:
        if sensor.begin() != True:
            print("Failed to start sensor")
            sys.exit(1)
        
        sensor.start_measurement_ready()
        temperature = sensor.get_temperature_C()
        humidity = sensor.get_humidity_RH()
        print(f'Temperature: {temperature:3.1f} C')
        print(f'Humidity: {humidity:3.1f} %')
        return f'{{"temperature": {temperature:3.1f}, "humidity": {humidity:3.1f}}}\r\n'
    except OSError as e:
        print('Failed to read sensor.')

while True:
    read_sensor(sensor)
    time.sleep(1)