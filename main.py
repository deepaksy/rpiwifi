# Python Program to control the LED and manage Wi-Fi connection on Raspberry Pi Pico W
# Copyright 2024 @ Deepak Suryawanshi

# Import statements
from machine import Pin
import time
import network

# Constants
SSID = "ssid"  # WiFi SSID
PASSWORD = "pass"  # WiFi PASSWORD
LED_PIN = 'LED'  # GPIO pin number for the onboard LED
LED = Pin(LED_PIN, Pin.OUT)
TIMEOUT = 10  # Connection timeout in seconds
RETRY_LIMIT = 5  # Number of connection attempts before waiting
RETRY_DELAY = 300  # Delay between retry attempts in seconds (5 minutes)

def blink_led(duration=2, interval=2, times=1):
    """Blink the LED for a specified duration and interval."""
    for _ in range(times):
        LED.value(1)
        time.sleep(duration)
        LED.value(0)
        time.sleep(interval)

def connect_wifi():
    """Connect to Wi-Fi with retries and return True if successful, False otherwise."""
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    
    for attempt in range(RETRY_LIMIT):
        wifi.connect(SSID, PASSWORD)
        
        start_time = time.time()
        while not wifi.isconnected():
            if time.time() - start_time > TIMEOUT:
                print(f"Attempt {attempt + 1} failed to connect to Wi-Fi")
                blink_led(duration=0.2, interval=0.2, times=3)
                break
            time.sleep(1)
        else:
            print('Wi-Fi connected')
            return True
        
        # Wait before retrying
        time.sleep(RETRY_DELAY)
    
    print("Failed to connect to Wi-Fi after several attempts")
    blink_led(duration=0.2, interval=0.2, times=3)
    return False

def main():
    """Main function to manage Wi-Fi connection and LED blinking."""
    if connect_wifi():
        while True:
            blink_led()

if __name__ == '__main__':
    main()


