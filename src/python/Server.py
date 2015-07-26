#-*- coding:utf-8 -*- 
import socket
import SocketServer
import threading,logging, traceback
import struct

import rpc
import ws_server


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
		proxy = rpc.RpcProxy(self.request)
		while 1:
			proxy.serve_forever()




class ThreadServer(SocketServer.ThreadingMixIn,SocketServer.TCPServer):
	pass


def make_rpc_server(host="localhost",port=9001):
	server = ThreadServer((host,port),rpcRequestHandler)
	return server


class MixServer(object):
	def __init__(self,make_rpc_server,make_ws_server):
		self.make_rpc_server = make_rpc_server
		self.make_ws_server = make_ws_server


	def make_server(self,rpc_host="localhost",rpc_port=9001,
				   ws_host="localhost",ws_port=9000):
		self.rpc_server = self.make_rpc_server(rpc_host,rpc_port)
		self.ws_server = self.make_ws_server(ws_host,ws_port)


	def serve_forever(self):
		def run_in_thread():
			try:
				logging.debug("run rpc server.")
				self.rpc_server.serve_forever()
			except Exception, e:
				print >> sys.stderr, traceback.format_exc()
				raise e

		t = threading.Thread(target=run_in_thread)
		t.start()

		logging.debug("runing web soecket server")
		self.ws_server.serve_forever()

	def close(self):
		self.ws_server.close()
		self.rpc_server.close()


			








if __name__ == "__main__":
	# address = ('localhost', 12345)
	# server = ThreadServer(address, rpcRequestHandler)
	# server.serve_forever()
	s = MixServer(make_rpc_server,ws_server.make_ws_server)
	s.make_server()
	s.serve_forever()

		




