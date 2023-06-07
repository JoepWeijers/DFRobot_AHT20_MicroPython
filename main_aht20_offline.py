import adafruit_ahtx0
import time
from machine import Pin, I2C

onboard = Pin("LED", Pin.OUT, value=0)
i2c = I2C(0, scl=Pin(17), sda=Pin(16))
devices = i2c.scan()
print('Devices: ' + str(devices))
sensor = adafruit_ahtx0.AHTx0(i2c)
print('Ready to go')

def read_sensor(sensor):
    try:
        temperature = sensor.temperature
        humidity = sensor.relative_humidity
        print(f'Temperature: {temperature:3.1f} C')
        print(f'Humidity: {humidity:3.1f} %%')
        return f'{{"temperature": {temperature:3.1f}, "humidity": {humidity:3.1f}}}\r\n'
    except OSError as e:
        print('Failed to read sensor.')

while True:
    print(f'Reading')
    read_sensor(sensor)
    time.sleep(0.5)