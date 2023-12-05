####################################################
#  Network Programming - Unit 8 Non-blocking Socket         
#  Program Name: 1-NonblockingClient.py                                      			
#  The program is a simple non-blocking TCP client.            		
#  2021.07.29                              
#python 1-NonblockingClient.py 127.0.0.1                    									
####################################################
import sys
import socket
import time

PORT = 6666
recv_buff_size = 1024			# Receive buffer size

def main():
	if(len(sys.argv) < 2):
		print("Usage: python3 1-NonblockingClient.py ServerIP")
		exit(1)

	# Connect to server
	serverIP = socket.gethostbyname(sys.argv[1])
	cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print('Connecting to %s port %s' % (serverIP, PORT))
	cSocket.connect((serverIP, PORT))

	# Send message to server
	msg = "Client hello!!"
	cSocket.send(msg.encode('utf-8'))
	
	# Set socket non-blocking
	cSocket.setblocking(False)
	
	while True:
		try:
			# Receive server reply, buffer size = recv_buff_size
			server_reply = cSocket.recv(recv_buff_size)
			break
		except BlockingIOError:
			# if no message, an exception occurs
			pass
		# do something here		
		print('+')
		time.sleep(0.2)
		# end do something here
	# end while

	print(server_reply.decode('utf-8'))
	print('Closing connection.')
	# Close the TCP socket
	cSocket.close()
# end of main


if __name__ == '__main__':
	main()
