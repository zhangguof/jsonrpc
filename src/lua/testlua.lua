local json = require "dkjson"
local utils = require "utils"

local s = {['a']='xxx',2,3,4,['newtable']={['x']='bbb',2,3,4}}

utils.print_table(s)

local jdata = json.encode(s)
utils.print_table(jdata)

utils.print_table(json.decode(jdata))


local function error_handle (err_msg)
  err_msg = debug.traceback (tostring (err_msg), 2)
  return "error:"..err_msg
end

local status,ret = xpcall(
	function ()
		print("in xxxx")
		local x=a/1
		return "dddd"
	end
	,error_handle
	)

print("ret:"..tostring(status)..":"..tostring(status))

