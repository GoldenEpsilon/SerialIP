import threading
import socket
import serial
import sys

localBoard = [];
for i in range(10):
	localBoard.append([]);
	for j in range(6):
		localBoard[i].append(0);

baud = 115200
timeout = 0.25
def serialIn(serialPort, sock):
	print('Starting up! Waiting for first message.')
	while(True):
		x = sock.recv(8)
		if(x == b'$'):
			print("RECV: ", end="")
		print(x.decode('utf-8'), end="")
		if(x[1:4] == "RES"):
			temp = x[4:].split("*")[0].split(",");
			localboard[temp[0]][temp[1]] = temp[2];
		for j in range(6):
			for i in range(10):
				print(localBoard[i][j], end="");
			print("");
		serialPort.write(x)

def serialOut(serialPort, client):
	while(True):
		x = serialPort.read()
		if(x == b'$'):
			print("SEND: ", end="")
		print(x.decode('utf-8'), end="")
		client.send(x)

# port = int(input("Port?: "))

# remotePort = int(input("Remote port?: "))
port = 5000
x = input("Server? (y/n): ")
while(x != 'y' and x != 'n'):
	x = input("Server? (y/n): ")

if(x == 'y'):
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind(("", port))
	server.listen(1)
	sock, _ = server.accept()
else:
	ip = input("Remote IP?: ")
	sock = socket.create_connection((ip, port))

userInput = input("Serial port?: ")
x = True
while(x):
	try:
		serialPort = serial.Serial(userInput, baud, timeout=timeout)
		x = False
	except serial.SerialException:
		print("Invalid serial port. This may require elevated privileges.")
		userInput = input("Serial port?: ")



sys.stdout.flush()
send = threading.Thread(target=serialOut, args=(serialPort, sock))
receive = threading.Thread(target=serialIn, args=(serialPort, sock))
# serialIn(serialPort, sock)
# serialOut(serialPort, sock)
send.start()
receive.start()
