from __future__ import print_function
import time
import serial
from threading import Thread

COM_PORT = 'COM6'

def to_bytes(n, length, endianess='big'):
	h = '%x' % n
	s = ('0'*(len(h) % 2) + h).zfill(length*2).decode('hex')
	return s if endianess == 'big' else s[::-1]

def writeAdd(input):
	ser.write(b'U')
	#time.sleep(.100)
	DecAdd = int(input, 0)
	#print(DecAdd)
	print("DecAdd:",DecAdd)
	Bytes = to_bytes(DecAdd,2, endianess='little')
	print("Bytes:",Bytes)
	ser.write(Bytes)
	ser.write(' ')
	
def writeEE(input):
	ser.write(b'd')
	#time.sleep(.100)
	DecLen = len(input)
	Bytes = to_bytes(DecLen,2, endianess='big')
	ser.write(Bytes)
	ser.write('E')
	ByteLen = len(input)
	for i in range(len(input)):
		Bytes = to_bytes(int(input[i],16),1,endianess='big')
		ser.write(Bytes)
	ser.write(' ')
def writeFF(input):
	ser.write(b'd')
	#time.sleep(.100)
	DecLen = len(input)/2
	print("DecLen:",DecLen)
	Bytes = to_bytes(DecLen,2, endianess='big')
	ser.write(Bytes)
	ser.write('F')
	for i in range(0,len(input),2):
		Bytes = to_bytes((int(input[i],16)*16)+(int(input[i+1],16)),1,endianess='big')
		ser.write(Bytes)
		print("Written = "+input[i])
		#ser.write(input[i])
		#ser.write(b'9')
	ser.write(' ')
	
def SerialRead():
	out = ''
	while 1:
		global ser
		try:
			while ser.inWaiting() > 0:
				out += ser.read(1)
		except:
			print("exiting ..")
			exit()

		if '\n' in out:
			#print(out[0].encode("hex"))
			print (out + ">> ",end = '')
			out =''
		if '10' in out.encode("hex"):
			#print(hex(out[0]))
			print (out)
			print (">> ",end = '')
			out =''
	
def SerialWrite():
	#global t
	while 1:
		# get keyboard input
		input = raw_input(">> ")
			# Python 3 users
			# input = input(">> ")
		if input == 'exit':
			#t.terminate()
			ser.close()
			exit()
		else:
			# send the character to the device
			# (note that I happend a \r\n carriage return and line feed to the characters - this is requested by my device)
			if(input != 1):
				#print(input)
				if input.startswith('E'):
					writeEE(input[1:])
				elif input.startswith('U'):
					writeAdd(input[1:])
				elif input.startswith('F'):
					writeFF(input[1:])
				else:
					ser.write(input)
		#print("two printed")
		
try:
	# configure the serial connections (the parameters differs on the device you are connecting to)
	ser = serial.Serial(
		port=COM_PORT,
		baudrate=19200,
		parity = serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS
		)
	ser.isOpen()
	print('Enter your commands below.\r\nInsert "exit" to leave the application.')

	input=1
	t = Thread(target=SerialRead)
	t.start()
	t2 = Thread(target = SerialWrite)
	t2.start()
except:
	print("Couldn't open serial port "+COM_PORT+'\r\n'+"Please change COM_PORT Number in Serial.py\r\n")
	print ("Exiting ..")


