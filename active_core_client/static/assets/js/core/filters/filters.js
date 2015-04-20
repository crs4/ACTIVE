angular.module("coreFilters", [])
.filter("bytype", function(){
	
	return function(input, selectedType){
		var ret = [];
		for(var i = 0; i < input.length; i++){
			var type = input[i].item_type;
			if(type == selectedType || type == "all")
				ret.push(input[i]);
		}
		return ret;
	}
	
});
