from deohttp import HttpClient
from machine import Pin
import time

# pin 12 is output - connects led in series with 
# 39E resistance

# pin 5 is input pin - in series with a 1k resistor
# in series with 10k resistor which is grounded

# 3.3V output from wemos goes to the switch
# which connects parallel to the two resistors

led12 = Pin(12, Pin.OUT)
led12.off()

iPin5 = Pin(5, Pin.IN)

def debounce_wrap(fn, p, interval=20):
	def callback(*arg, **kwargs):
		count = 0
		hits = 0
		value = p.value()
		while count < interval:
			if p.value() == value:
				hits = hits + 1
			count = count + 1
			time.sleep(0.001)
		if hits == interval:
			fn(value)

	return callback

def change_state(value):
	led12.value(value)
	if value:
		signal_on()
	else:
		signal_off()

iPin5.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, \
	handler=debounce_wrap(change_state, iPin5, 20) )

def signal_on():
	client = HttpClient('http://192.168.4.1/on')
	client.do_request()

def signal_off():
	client = HttpClient('http://192.168.4.1/off')
	client.do_request()


while True:
	time.sleep(1)