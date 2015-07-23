#-*- coding:utf-8 -*- 
import socket
import SocketServer
import threading,logging
import struct

import rpc

logging.basicConfig(level=logging.DEBUG,
	format="%(name)s: %(message)s",
	)



class ThreadTcpRequestHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		data = self.request.recv(1024)


class rpcRequestHandler(SocketServer.StreamRequestHandler):
	def setup(self):
		pass

	def handle(self):
		print "new connect:",self.client_address
		# while 1:
		# 	s_struct = struct.Struct("I")
		# 	size = self.request.recv(4)
		# 	if not size:
		# 		print "no size data:closing.."
		# 		break
		# 	size = s_struct.unpack(size)[0]
		# 	print "recv size:%s"%size

		# 	d_struct = struct.Struct("%ds"%size)
		# 	data = self.request.recv(size)
		# 	if not data:
		# 		print "no data closing..."
		# 		break

		# 	data = d_struct.unpack(data)[0]
		# 	print "data:%s"%data
		proxy = rpc.RpcProxy(self.request)
		while 1:
			proxy.serve_forever()





class ThreadServer(SocketServer.ThreadingMixIn,SocketServer.TCPServer):
	pass



if __name__ == "__main__":
	address = ('localhost', 12345)
	server = ThreadServer(address, rpcRequestHandler)
	server.serve_forever()

		






