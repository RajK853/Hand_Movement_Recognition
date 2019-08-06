from microbit import display, Image, sleep, button_a, button_b, running_time, accelerometer
from micropython import const
import radio
# States
READY           = const(1)
SAMPLE_DATA     = const(2)
SEND_DATA       = const(3)
EXIT            = const(-1)
# Global constants
CHANNEL         = const(25)
MAX_ATTEMPT     = const(1)
SAMPLE_INTERVAL = const(10)                                                 # Sample period in ms
SAMPLE_DURATION = const(1500)                                               # Total sample time in ms
ACK             = const(b"0")
NACK            = const(b"1")
# LED Numbers (3,2,1) rotated 90 degrees clockwise
NUM_IMGS = const([Image("90909:90909:90909:99999:99999"),
				  Image("99909:90909:90909:90909:90999"),
				  Image("00000:00090:99999:99999:00000")])

def retry(attempts=MAX_ATTEMPT, retry_interval=100, valid_responses=None, invalid_responses=None, invalid_msg=None):
	"""
	Decorator to call a function for multiple times depending on its return value
	@param attempts		    : Maximum number of attempts
	@param retry_interval   : Wait time (in milliseconds) between each retry
	@param valid_responses  : Valid responses as list/tuple
	@param invalid_responses: Invalid responses as list/tuple
	@param invalid_msg      : Message to display when invalid response received
	@returns                : Decorator function
	"""
	def decorator(func):
		def wrapper(*args, **kwargs):
			for attempt in range(attempts):
				res = func(*args, **kwargs)									# Call the function
				if valid_responses is None and invalid_responses is None:
					return res 												# Return reponse
				else:
					if valid_responses is not None and res in valid_responses:
						return res 											# Return received valid response
					elif invalid_responses is not None and res not in invalid_responses:
						return res 											# Return received response which was not invalid
					if invalid_msg is not None:
						print(invalid_msg)
				sleep(retry_interval)
			return res
		return wrapper
	return decorator

def countdown(t=3):
	"""
	Display countdown animation of given second(s)
	@param t : Time (in seconds)
	@returns : Nothing
	"""
	max_t = len(NUM_IMGS)
	if (t > max_t):
		t = max_t
	elif (t <= 0):
		t = 1
	display.show(NUM_IMGS[-t:], loop=False, delay=1000)

def waitForACK(timer=2000, pooling_interval=10):
	"""
	Waits for acknowledgement for given amount of time
	@param timer            : Maximum waiting time for the acknowledgement
	@param pooling_interval : Interval to check for acknowledgement
	@returns                : Received acknowledgement
							  NACK for timeout
	"""
	initial_time = running_time()
	while (running_time() - initial_time) < timer:
		response = radio.receive()
		if response is not None:
			return response
		sleep(pooling_interval)
	return NACK

@retry(attempts=MAX_ATTEMPT, valid_responses=(ACK,), invalid_responses=(NACK,))
def sendMsg(data, wait_time=1000, pooling_interval=10):
	"""
	Sends given data and waits for acknowledgement
	@param data             : Data as string or bytes
	@param wait_time        : Maximum waiting time for the acknowledgement
	@param pooling_interval : Interval to check for acknowledgement
	@returns                : Received acknowledgement
	"""
	radio.send(data)
	response = waitForACK(timer=wait_time, pooling_interval=pooling_interval)
	return response

def main():
	state = READY
	while True:
		# Ready state
		if state == READY:
			while True:
				if button_a.is_pressed():			
					state = SAMPLE_DATA
					break
				elif button_b.is_pressed():
					radio.on()
					radio.send("done")
					radio.off()
				else:
					display.show(Image.ARROW_W)
				sleep(100)
		# Sample Data state
		elif state == SAMPLE_DATA:
			data_sent = 0															# Reset data sent value
			countdown(3)															# Show countdown on the Microbit LED	
			display.show(Image.TARGET)
			radio.on()
			initial_time = running_time()
			while (running_time()-initial_time) < SAMPLE_DURATION:
				t0 = running_time()
				if data_sent == 0:													# Turn off all Microbit LEDs
					display.clear()
				cx, cy = divmod(data_sent, 5)										# Get current LED pixel coordinate of the BBC Microbit
				radio.send(str(accelerometer.get_values()))
				display.set_pixel(4-cx, cy, 9)
				data_sent = 0 if data_sent >= 24 else data_sent+1					# Increase and limit data_sent value within 0-24 range
				wait_t = SAMPLE_INTERVAL-(running_time()-t0)						# Time till next sample
				if (wait_t > 0):
					sleep(wait_t)
			radio.send("done")
			radio.off()
			state = READY
		# Exit state
		elif state == EXIT:
			display.show(Image.HAPPY)
			return 0
		sleep(100)

if __name__ == "__main__":
	try:
		radio.config(channel=CHANNEL, data_rate=radio.RATE_2MBIT, power=7, queue=20)
		main()
	finally:
		radio.off()