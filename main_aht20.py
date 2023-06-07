import adafruit_ahtx0
import uasyncio as asyncio
from machine import Pin, I2C
from config import config
from wlan import connect_wlan, show_wlan_status

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
        
async def serve_client(reader, writer):
    print("Client connected")
    response = read_sensor(sensor).encode('utf-8')
    writer.write(f'HTTP/1.0 200 OK\r\nContent-type: application/json\r\nContent-length: {len(response)}\r\n\r\n'.encode('utf-8'))
    writer.write(response)
    await writer.drain()
    writer.close()
    
    onboard.on()
    await asyncio.sleep(0.15)
    onboard.off()
    await asyncio.sleep(0.15)
    onboard.on()
    await asyncio.sleep(0.15)
    onboard.off()
    
    await writer.wait_closed()
    print("Client disconnected")
    
async def main():
    print('Connecting to Network...')
    wlan = connect_wlan(config['ssid'], config['pw'])
    show_wlan_status(wlan)

    print('Setting up webserver...')
    asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))
    
    while True:
        show_wlan_status(wlan)
        if not wlan.isconnected():
            wlan.disconnect()
            wlan = connect_wlan(config['ssid'], config['pw'])
        
        await asyncio.sleep(10)

try:
    read_sensor(sensor)
    asyncio.run(main())
finally:
    asyncio.new_event_loop()
