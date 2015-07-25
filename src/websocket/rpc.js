/*json rpc for websocket */


function rpc_message(msg){
	alert(msg);
}

function rpc_pack(json_data){
	//return a ArrayBuffer obj
	var json_str = JSON.stringify(json_data)
	var size = json_str.length
	var ab = new ArrayBuffer(4+size)
	var head = new Int32Array(ab,0,4)
	var data = new Uint8Array(ab,4)

	head[0] = size
	for(i=0;i<size;i++){
		data[i] = json_str.charCodeAt(i)
	}
	return ab
}

function rpc_unpack(buffer){
	//return json obj
	var head  = new Int32Array(buffer,0,4)
	var data = new Uint8Array(buffer,4)
	var json_str = String.fromCharCode.apply(null,data)
	return JSON.parse(json_str)

}


//handers= {'method_name':func}

function rpc_connect(host,handlers,message){
	var socket;
	if(!message)
	{
		message = rpc_message;
	}
	function on_open(){
		socket.binaryType = "arraybuffer"
		//alert("on open");

	}
	function on_close(){
		alert("on close");

	}

	function do_handler(method,args){
		return method.apply(null,args);
	}
	function call_remote(method_name,args){
		send_obj = {"method":method_name,"params":args}
		// send_str = JSON.stringify(send_obj)
		send_bin = rpc_pack(send_obj)
		socket.send(send_bin);
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

	function on_wsMessage(event)
	{
		console.debug(event)
		var data = rpc_unpack(event.data)

		var method_name = data['method']
		var args = data['params'] || []
		if(method_name ){
			var method = handlers[method_name]
			if(method)
			{
				do_handler(method,args);
			}
			else{
			console.error("Can't find method named:"+method_name)
			}
			
		}


	}


	try{
		socket = new WebSocket(host);
		socket.onopen = on_open;
		socket.onmessage = on_wsMessage;
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