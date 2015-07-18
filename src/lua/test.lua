
local rpc = require "rpc"

handlers = {}

function handlers:echo(s)
	print(s)
	self._proxy.printf("echo:"..s)
end

function cb_close()
	print("closed...")
end

proxy = rpc.connect("127.0.0.1",12345,handlers,cb_close)

while true do
	proxy:tick_loop()
end