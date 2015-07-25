from wsgiref.simple_server import make_server
from ws4py.websocket import EchoWebSocket, WebSocket
from ws4py.server.wsgirefserver import WSGIServer, WebSocketWSGIRequestHandler
from ws4py.server.wsgiutils import WebSocketWSGIApplication

import rpc,struct


class test_web_socket(WebSocket):
	def received_message(self,message):
		print "get a msg:",[message.data]
		#self.send(message.data, message.is_binary)
		data = message.data


		print "unpack:",rpc.unpack(message.data)
		json_data = {"method":"log","params":["hi~~~"]}
		self.send(rpc.pack(json_data),True)


server = make_server('', 9000, server_class=WSGIServer,
                     handler_class=WebSocketWSGIRequestHandler,
                     app=WebSocketWSGIApplication(handler_cls=test_web_socket))

server.initialize_websockets_manager()
server.serve_forever()