#!/usr/bin/env python3

import quick2wire.i2c as i2c

# Arduino's i2c address
address = 0x04


def send(sendStr):
	byteList = []
	for i in sendStr:
		byteList.append(ord(i))
	byteList.append(0x0A)

	with i2c.I2CMaster() as bus:    
		bus.transaction(
		i2c.writing(address, bytes(byteList)))
		#i2c.writing_bytes(address, 0x01))

send("Hi Kate!")