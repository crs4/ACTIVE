define(["core/module"], function(module){
	
	module.registerFilter("bytype", function(){
		
		return function(input, args){
			var ret = [];
			for(i = 0; i < input.length; i++){
				var type = input[i].item_type;
				if(type.indexOf(args) != -1 || type.indexOf("all") != -1)
					ret.push(input[i]);
			}
			return ret;
		}
	
	});
	
});
