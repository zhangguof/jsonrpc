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
		proxy = rpc.RpcProxy(self.request)
		while 1:
			proxy.serve_forever()




class ThreadServer(SocketServer.ThreadingMixIn,SocketServer.TCPServer):
	pass


class MixServer(object):
	def __init__(self,make_rpc_server,make_ws_server):
		pass


	def start(self,rpc_host,ws_host):
		pass






if __name__ == "__main__":
	address = ('localhost', 12345)
	server = ThreadServer(address, rpcRequestHandler)
	server.serve_forever()

		






