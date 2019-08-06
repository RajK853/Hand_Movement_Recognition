import os
import sys
import radio
from micropython import const
from microbit import display, Image, sleep, button_a, button_b, running_time, uart

# Global constants
CHANNEL = const(25)

def main():
	data_received = 0
	display.show(Image.HAPPY)
	while True:
		response = radio.receive()
		if response is not None:							# Some data received
			uart.write(response+"\n")						# Write received data with line break on serial bus
			if data_received == 0:
				display.clear()								# Clear Microbit LEDs
			if "," in response:								# "(x,y,z)" data received
				cy, cx = divmod(data_received, 5)
				display.set_pixel(cx, cy, 9)
				# Increase and limit data_received value within 0-24 range
				data_received = 0 if data_received >= 24 else data_received+1
			elif response == "done":
				data_received = 0
				display.show(Image.YES)
			elif response == "exit":
				display.show(Image.HAPPY)
				sleep(2000)
				display.clear()
				break
        else:
			sleep(100)

if __name__ == "__main__":
	try:
		uart.init(baudrate=115200, bits=8, parity=None, stop=1)
		radio.config(channel=CHANNEL, data_rate=radio.RATE_2MBIT, power=7, queue=150)
		radio.on()
		main()
	finally:
		uart.close()
		radio.off()