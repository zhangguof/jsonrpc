
local M = {}
local serpent = require "serpent"
function M.print_table(t)
	print (serpent.block(t))
end


return M