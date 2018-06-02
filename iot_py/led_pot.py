import spidev
import time
from libsoc import gpio

from gpio_96boards import GPIO

# POT = variavel com valor do potenciometro

POT = GPIO.gpio_id('GPIO_CS') 
LED = GPIO.gpio_id('GPIO_A')

pins = ((POT, 'out'), (LED, 'out'),)

base = 500

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 10000
spi.mode = 0b00
spi.bits_per_word = 8

def lerpot(gpio):

	gpio.digital_write(GPIO_CS, GPIO.HIGH)
	time.sleep(0.0002)
	gpio.digital_write(GPIO_CS, GPIO.LOW)
	r = spi.xfer2([0x01, 0xA0, 0x00])
	gpio.digital_write(GPIO_CS, GPIO.HIGH)
	ptvalor = (r[1] << 8) & 0b1100000000
	ptvalor = ptvalor | (r[2] & 0xff)		
	print ("Valor do Potenciometro.:%d" %ptvalor)
	
    if ptvalor > base:
        gpio.digital_write(LED, GPIO.HIGH)
        led_status = "Ligado"
    else:
        gpio.digital_write(LED, GPIO.LOW)	
        led_status = "Apagado"
    
    return ptvalor

while True:
	with GPIO(pins) as gpio:
		value = lerpot(gpio)
		time.sleep(0.5)


