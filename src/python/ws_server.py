from wsgiref.simple_server import make_server
from ws4py.websocket import EchoWebSocket, WebSocket
from ws4py.server.wsgirefserver import WSGIServer, WebSocketWSGIRequestHandler
from ws4py.server.wsgiutils import WebSocketWSGIApplication

import rpc






class test_web_socket(WebSocket):
	def received_message(self,message):
		print "get a msg:",message
		self.send(message.data, message.is_binary)


class RpcWebSocket(WebSocket):
	def opened(self):
		def sender(message):
			self.send(message,True)
		self.proxy = rpc.RpcProxy(None,_sender=sender)


	def received_message(self,message):
		json_data = rpc.unpack(message.data)
		self.proxy.handler(json_data)




# server = make_server('', 9000, server_class=WSGIServer,
#                      handler_class=WebSocketWSGIRequestHandler,
#                      app=WebSocketWSGIApplication(handler_cls=test_web_socket))

# server.initialize_websockets_manager()
# server.serve_forever()


def make_ws_server(host="localhost",port=9000):
	server = make_server(host, port,
					 server_class =  WSGIServer,
		             handler_class=WebSocketWSGIRequestHandler,
                     app=WebSocketWSGIApplication(handler_cls=RpcWebSocket)
                     )

	server.initialize_websockets_manager()
	return server

if __name__ == "__main__":
	server = make_ws_server()
	server.serve_forever()