/*json rpc for websocket */


function rpc_message(msg){
	alert(msg);
}

//handers= {'method_name':func}

function rpc_connect(host,handlers,message){
	var socket;
	if(!message)
	{
		message = rpc_message;
	}
	function on_open(){
		alert("on open");

	}
	function on_close(){
		alert("on close");

	}

	function do_handler(method,args){
		return method.apply(null,args);
	}
	function call_remote(method_name,args){
		send_obj = {"method":method_name,"params":args}
		send_str = JSON.stringify(send_obj)
		socket.send(send_str);
	}


	function on_message(msg){
		var data = JSON.parse(msg);

		var method_name = data['method']
		var args = data['params'] || []
		if(method_name ){
			var method = handlers[method_name]
			if(method)
			{
				do_handler(method,args);
			}
			
		}



	}


	try{
		socket = new WebSocket(host);
		socket.onopen = on_open;
		socket.onmessage = on_message;
		socket.onclose = on_close;
	}
	catch(exception){
		message(exception);
	}

	function rpc_call(method_name){
		var args = []
		if(arguments.length > 1){
			for(var i=1;i<arguments.length;i++)
			{
				args.push(arguments[i]);
			}
		}
		call_remote(method_name,args);

	}

	return rpc_call

}