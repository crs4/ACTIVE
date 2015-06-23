angular.module("coreFilters", [])
.filter("bytype", function(){
	
	return function(input, selectedType){
		var ret = [];
		for(i = 0; i < input.length; i++){
			var type = input[i].type;
			if(type.indexOf(selectedType) != -1 || type.indexOf("all") != -1)
				ret.push(input[i]);
		}
		return ret;
	}
	
});
