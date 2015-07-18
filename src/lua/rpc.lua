
local M = {}
local socket = require("socket.core")
local json = require("dkjson")


local struct = {}
function struct.unpack(format,s)
	local ret = {}
	for _,f in ipairs(format) do
		if f == "i" then
			local a = 0
			for i=4,1,-1 do
				a = a*256 + string.byte(s,i)
			end
			table.insert(ret,a)
			s=string.sub(s,5,-1)
			--print(s)
		else
			local i,j= string.find(f,"(%d+)s")
			if i == 1 then
				local len = tonumber(string.sub(f,1,j-1))
				table.insert(ret,string.sub(s,1,len))
				s = string.sub(len+1,-1)

			end

		end
	end
	return ret
end


function  struct.pack(format,...)
	local ret = ""
	local args = {...}
	for idx, f in ipairs(format) do
		if f == "i" then
			local a={0,0,0,0}
			local num = args[idx]
			for i=1,4 do
				local b = math.floor(num/256)
				a[i] = num - b * 256 --余数
				num = b
			end
			ret = ret .. string.char(table.unpack(a))
		else
			local i,j= string.find(f,"(%d+)s")
			if i == 1 then
				local len = tonumber(string.sub(f,1,j-1))
				ret = ret..string.sub(args[idx],1,len)
			end
		end
	end
	return ret
end

-- print_table(struct.unpack({"i","4s"},"\120\86\52\18abcd"))

-- local a = struct.pack({"i","2s"},305419896,"ab")
-- print(a)
-- print_table(struct.unpack({"i","4s"},a))
-- -- print(string.format("%04x",struct.unpack("i",a)))

-- local handlers = {
-- 	_proxy=nil
-- }
-- function handlers:add(a,b)
-- 	self._proxy.server.printf(a+b)
-- 	-- body
-- end
-- function handlers:echo(s)
-- 	self._proxy.server.printf(s)
-- 	-- body
-- end
-- function handlers:printf(s)
-- 	print(s)
-- end

-- function handlers:do_string(s)
-- 	loadstring(s)()
-- end

function M.connect( ip,port,handlers,cb_close)
	local rpc_client = socket.tcp()
	rpc_client:settimeout(2)
	local state, info = rpc_client:connect(ip,port)
	if state ~= nil then
		-- print("peername:",rpc_client:getpeername())
		-- print("socketname:",rpc_client:getsockname())
		local proxy = M.create_rpc_proxy(rpc_client,handlers,cb_close)
		return proxy
	else
		return nil
	end
end

function M.create_rpc_proxy( sock,handlers, cb_close)
	sock:settimeout(0)
	local proxy = {client=sock,server={}}
	handlers._proxy = proxy.server

	function proxy:call_remote_method(fun_name,...)
		local remote_json = {method=fun_name,params={...}}
		
		local json_str = json.encode(remote_json)
		local json_size = string.len(json_str)
		json_str = struct.pack({"i",tostring(json_size).."s"},json_size,json_str)
		--print("remote_json:",json_str)
		--print("call remote:",json_size,json_str)
		self.client:send(json_str)

		--receive ret.
		-- local ret_size = struct.unpack({"i"},self.client.receive(4))[1]
		-- local ret_data = self.client.receive(ret_size)
		-- local ret = json.decode(ret_data)
		-- return ret['result']
	end

	local function server_index_method(t,key)
		local method = function( ... )
			return proxy:call_remote_method(key,...)
		end
		t[key] = method
		return method
	end
	setmetatable(proxy.server,{__index = server_index_method})
	

	function  proxy:do_handler()
		local function error_handle (err_msg)
			err_msg = debug.traceback (tostring (err_msg), 2)
			return err_msg
		end
		local data, state = self.client:receive(4)
		if state == "closed" then
			cb_close()
			--error("connectClosed")
		end
		local json_size = struct.unpack({"i"},data)[1]

		--print("json_size:",json_size)
		data = self.client:receive(json_size)
		--print("json_data:",data)
		--print(data)
		local json_data = json.decode(data)
		local method = json_data.method
		if method then
			local params = json_data.params
			local status,ret=pcall(
				function ()
				local ret = handlers[method](handlers,table.unpack(params))
				return ret
				end,
				error_handle)
			if status then
				return ret
			else
				proxy.server.error(ret)
			end
		end
		
		--print_table(json_data)
	end

	function proxy:tick_loop()
		local rd = socket.select({self.client},nil,0)
		if #rd > 0 then
			self:do_handler()
		end
	end

	return proxy
end
-- local sock = socket.connect("127.0.0.1",1234)
-- print(sock)
-- print("connect....")
-- print("peername:",sock:getpeername())
-- print("socketname:",sock:getsockname())
-- local proxy = create_rpc_proxy(sock,handlers)
-- handlers._proxy = proxy
-- proxy.server.printf("hello")
-- proxy.server.add(1,2)
-- proxy.server.echo("hello")
-- proxy.server.loop_echo("hhh",10,1)

-- local count = 0
-- print("receive......")
-- while true do
-- 	proxy:tick_loop()
-- 	count = count + 1
-- 	if count > 20 then
-- 		count = 0
-- 		print("count:",count)
-- 	end
-- end


return M