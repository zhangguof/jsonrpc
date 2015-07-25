#-*- coding:utf-8 -*-

import json
import struct
import socket,SocketServer,select
import traceback

#proxy = RpcProxy.server.print("xxxx")


def pack(json_data):
	d = json.dumps(json_data)
	s = len(d)
	packer = struct.Struct("I %ds"%s)
	data = packer.pack(s,d)
	return data

def unpack(data):
	s_struct = struct.Struct("I")
	size = s_struct.unpack(data[:4])[0]

	d_struct = struct.Struct("%ds"%size)
	json_str = d_struct.unpack(data[4:])[0]
	return json.loads(json_str)

class Service(object):
	def __init__(self,rpc):
		self.rpc = rpc

	def exposed_echo(self,s):
		self.rpc.remote.printf("echo:%s"%s)

	def exposed_printf(self,s):
		print s

	def get(self,method_name):
		if method_name.startswith("exposed_"):
			return getattr(self,method_name,None)
		method_name = "exposed_"+method_name
		return getattr(self,method_name,None)


class RpcProxy(object):
	def __init__(self,s,Service=Service):
		self.socket = s
		self.service = Service(self)

		sender = self.socket.send

		class Method(object):
			def __init__(self,name):
				self.name = name

			def __call__(self,*args):
				json_data = {"method":self.name,"params":args}
				sender(pack(json_data))

		class Proxy(object):
			def __init__(self):
				self.methods = {}
			def __getattr__(self,key):
				if key not in self.methods:
					self.methods[key] = Method(key)
				return self.methods[key] 

		self.remote = Proxy()

	def handler(self,data):
		method_name = data['method']
		params = data['params']

		method = self.service.get(method_name)
		if method:
			method(*params)

	def on_handler(self):
		s_struct = struct.Struct("I")
		size = self.socket.recv(4)
		if not size:
			self.close()
			return
		size = s_struct.unpack(size)[0]

		d_struct = struct.Struct("%ds"%size)
		data = self.socket.recv(size)

		if not data:
			self.close()
			return
		data = d_struct.unpack(data)[0]

		json_dict = json.loads(data)
		self.handler(json_dict)

	def one_tick(self):
		rs, _, _ = select.select([self.socket],[],[],0.1)
		if rs:
			self.on_handler()

	def serve_forever(self):
		print "start proxy server."
		try:
			while 1:
				self.one_tick()
		except:
			print traceback.format_exc()
			raise




	def close(self):
		self.socket.close()
		raise Exception("socket Closed.")





if __name__ == "__main__":

	import struct, socket
	import threading

	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect(('localhost',12345))


	proxy = RpcProxy(s,Service)
	t = threading.Thread(target=proxy.serve_forever)
	t.start()

	proxy.remote.echo("hdddd")
	proxy.remote.echo("12111111")
	#proxy.remote.test(123,'123',[1,2,'abc'])
	t.join()



	


		
