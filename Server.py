####################################################
#  Network Programming - Unit 8 Non-blocking Socket         
#  Program Name: 2-MultiPortServer.py                                      			
#  The program is a simple non-blocking TCP server.            		
#  2021.08.02                   python 2-MultiPortServer.py 8880  8881                               									
####################################################
import sys
import  time
import socket
import select
import queue

BUF_SIZE = 1024

def main():
	if(len(sys.argv) < 2):
		print("Usage python3 2-MultiPortServer.py port1 port2 ...")
		exit(1)

	inputs = []
	srv_list = []
	outputs = []
	qu = [1,2,3]	
	# Create sockets
	for i in range(1, len(sys.argv)):
		port = int(sys.argv[i])
		# Creat a TCP socket
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server.bind(('', port))
		
		# Set socket non blocking
		server.setblocking(False)
		server.listen(5)
		
		# Add to list
		inputs.append(server)
		srv_list.append(server)
		print("Listening on port " + str(port))

	print("Waiting incomming connection ...")
	
	while True:
		#print("!") 	####
		readable, writable, exceptional = select.select(inputs, outputs, inputs)
		#print("*")		###
		for s in readable:
			if s in srv_list:		# new connection
				try:
					# Accept the incomming connection
					#print("!")         ###
					connection, (rip, rport) = s.accept()
					#print("@")			###
					# Set the connection non blocking
					connection.setblocking(False)
					# Add connection to inputs (listen message on the connection)
					laddr = connection.getsockname()
					if int(laddr[1]) == 8880:
						inputs.append(connection)
					elif int(laddr[1]) == 8881:
						outputs.append(connection)
					msg = "Accept connection on port: %d from (%s, %d)" %(laddr[1], str(rip), rport)
					print(msg)
				except BlockingIOError:
					print("NOIO")
					# 没有等待接受的新连接
					pass
			else:
				raddr = s.getpeername()
				laddr = s.getsockname()
				#print("$") 	
				if len(qu) <= 5:	
						try:
							data = s.recv(BUF_SIZE).decode('utf-8') #.recv()
							print("recv data ",data)
							qu.append(data)
							server_reply = 'Sucess'
							s.send(server_reply.encode('utf-8'))
						except BlockingIOError:
							pass
				else:
					try:
						data = s.recv(BUF_SIZE).decode('utf-8')
						server_reply = 'Error message'
						s.send(server_reply.encode('utf-8'))
					except ConnectionAbortedError:
						inputs.remove(s)
		
						print('與%s %s 发生斷連:' %laddr)
		if writable:
			on = 0
			for s in writable:			
				#print("%")		###
				server_reply = ""
				try:
					if qu:
						try:
							server_reply = " " + str(qu[0])
							s.send(server_reply.encode('utf-8'))  # 將數字轉換為字串並傳送
							on += 1
						except BlockingIOError:
							server_reply = ""
							print("收方斷連")						
				except BlockingIOError:
					print("Connection reset by peer")
					pass
			if writable:
				if qu and on != 0:
					qu.pop(0)
			time.sleep(3)
		for s in exceptional:
			print("Close : ", s)
			inputs.remove(s)
			#s.close()
        # end for exceptionsl
	# end for while True
# end of main()
# Close connection
"""print("Close connection from: ", raddr)
inputs.remove(s)   #沒想法
s.close()"""

if __name__ == '__main__':
	main()